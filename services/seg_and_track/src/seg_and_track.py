import os
import pathlib
import json
from typing import List
import math
import datetime
import uuid

import cv2
import numpy as np
import torch
from huggingface_hub import hf_hub_download
from ultralytics import YOLO
import cv2.aruco as aruco

from seg_and_track_api import SegAndTrackResponse, Box, Pose, Graph
from data import test_cases

from masks import get_masks_in_rois, get_masks_rois, scale_image, reconstruct_masks
from visualization import draw_objects
from conversions import to_mask_msg
from depth_map import DepthEvaluator, PlaneDetector


DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
OUTPUT_DIR = pathlib.Path("/data/seg_and_track")
# OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
errors = []

def save_json(data, path: pathlib.Path):
    with path.open("w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def save_output(task_id, image_path, response, img, base_dir=None):
    if base_dir is None:
        base_dir = OUTPUT_DIR
    else:
        base_dir = OUTPUT_DIR / base_dir
    save_dir = base_dir / task_id
    save_dir.mkdir(parents=True, exist_ok=True)
    # Saving the visualization
    cv2.imwrite(str(save_dir / "visualization.png"), img)
    # Saving the response
    save_json(response.dict(), save_dir / "labels.json")
    # Saving the meta
    meta = {"task_id": task_id, "image_path": str(image_path), "timestamp": str(datetime.datetime.now())}
    save_json(meta, save_dir / "meta.json")


class SegAndTrack:
    def __init__(self):
        model_path = hf_hub_download(repo_id="AnzhelikaK/yolo-v-11-new", filename="best.pt")
        self.model = YOLO(model_path)
        self.model.to(DEVICE)
        self.depth_evaluator = DepthEvaluator(device=DEVICE)
        self.colors_palette = {0: (7, 7, 132), 1: (158, 18, 6), 2: (96, 12, 107), 3: (112, 82, 0)}

        # Reference size of the boxes and containers with aruco markers (w x h in meters)
        self.aruco_size_reference = {
            313: (0.2, 0.14),  # box
            998: (0.26, 0.18),  # box
            999: (0.19, 0.16),  # container
            990: (0.30, 0.18),  # container
        }

        # Aruco parameters
        self.aruco_dict = aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_1000)
        self.aruco_params = aruco.DetectorParameters_create()
        self.marker_length = 0.08  # Length of the Aruco marker side
        self.camera_matrix = np.array([[580.77518, 0.0, 724.75002], [0.0, 580.77518, 570.98956], [0.0, 0.0, 1.0]])
        self.dist_coeffs = np.array([0.927077, 0.141438, 0.000196, -8.7e-05, 0.001695, 1.257216, 0.354688, 0.015954])
        self.dist_fish = np.array([0.927077, 0.141438, 0.000196, -8.7e-05])
        self.plane_detector = PlaneDetector(self.camera_matrix)

    def segment_image_(self, img: np.ndarray, h: int, w: int) -> tuple[list[float], list[int], list[list[int]], np.ndarray]:
        results = self.model(img)[0]
        conf = results.boxes.conf.cpu().numpy().astype(np.float32).tolist()
        class_ids = results.boxes.cls.cpu().numpy().astype(np.uint8).tolist()
        boxes = results.boxes.xyxy.cpu().numpy().astype(np.uint32).tolist()
        masks = results.masks if results.masks is not None else None

        if masks is None:
            scaled_masks = np.empty((0, h, w), dtype=np.uint8)
        else:
            masks = masks.data.cpu().numpy().astype(np.uint8)
            mask_height, mask_width = masks.shape[1:]
            masks = masks.transpose(1, 2, 0)
            scaled_masks = scale_image((mask_height, mask_width), masks, (h, w))
            scaled_masks = scaled_masks.transpose(2, 0, 1)

        return conf, class_ids, boxes, scaled_masks

    def detect_aruco(self, img: np.ndarray, 
                     masks_in_rois: np.ndarray, 
                     rois: np.ndarray
                    ) -> tuple[list[int], list[dict], list[np.ndarray], list[int], list[dict], list[np.ndarray]]:
        marker_ids = []
        marker_poses = []
        marker_corners = []
        count_num = 0
        corners_all, ids_all, _ = aruco.detectMarkers(img, self.aruco_dict)
        # Estimating aruco translation and rotation vectors
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
            corners_all, self.marker_length, self.camera_matrix, self.dist_coeffs
        )
        # Searching for aruco markers in ROI
        for i, roi in enumerate(rois):
            x = int(roi[1].start)
            y = int(roi[0].start)
            w_roi = int(roi[1].stop - roi[1].start)
            h_roi = int(roi[0].stop - roi[0].start)

            roi_image = img[y : y + h_roi, x : x + w_roi]

            # Detect Aruco markers
            corners, ids, _ = aruco.detectMarkers(roi_image, self.aruco_dict)

            if ids is not None:
                aruco_mask = np.zeros(roi_image.shape[:2], dtype=np.uint8)
                pts = corners[0][0].astype(np.int32)
                cv2.fillPoly(aruco_mask, [pts], 1)

                if np.any(masks_in_rois[i] * aruco_mask):
                    marker_ids.append(ids[0][0])
                    corners_with_offset = [
                        corner + [x, y]
                        for corner in corners  # coordinates of corners on the initial image
                    ]

                    # Estimating aruco translation and rotation vectors
                    rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
                        corners_with_offset, self.marker_length, self.camera_matrix, self.dist_coeffs
                    )
                    # 6 degrees of freedom
                    pose_6dof = {"rvec": rvecs[0].tolist(), "tvec": tvecs[0].tolist()}

                    marker_poses.append(pose_6dof)
                    marker_corners.append(corners_with_offset[0][0])
                    # Draw the Aruco marker corners
                    cv2.polylines(img, [pts + [x, y]], isClosed=True, color=(0, 255, 255), thickness=3)
                    cv2.putText(
                        img,
                        f"Aruco_id: {ids[0][0]}",
                        (x + pts[0][0], y + pts[0][1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 255),
                        2,
                    )
                else:
                    marker_ids.append(count_num)
                    pose_6dof = {"rvec": [[0, 0, 0]], "tvec": [[0, 0, 0]]}
                    marker_poses.append(pose_6dof)
                    marker_corners.append(None)
                    count_num += 1
            else:
                marker_ids.append(count_num)
                pose_6dof = {"rvec": [[0, 0, 0]], "tvec": [[0, 0, 0]]}
                marker_poses.append(pose_6dof)
                marker_corners.append(None)
                count_num += 1
        # Aruco markers on shelves
        shelf_ids = []
        shelf_corners = []
        shelves = []
        corners_shelf, ids_shelfs, _ = aruco.detectMarkers(img, self.aruco_dict, parameters=self.aruco_params)
        if ids_shelfs is not None:
            rvecs_shelf, tvecs_shelf, _ = cv2.aruco.estimatePoseSingleMarkers(
                corners_shelf, self.marker_length, self.camera_matrix, self.dist_coeffs
            )
            for i in range(len(ids_shelfs)):
                marker_id = ids_shelfs[i][0]
                # Check if aruco id corresponding to shelf
                shelf_id = marker_id - 10 if 10 <= marker_id <= 17 else -1

                if shelf_id != -1:
                    pts_shelves = corners_shelf[i][0].astype(np.int32)
                    cv2.polylines(img, [pts_shelves], isClosed=True, color=(0, 255, 255), thickness=3)
                    cv2.putText(
                        img,
                        f"Aruco_id: {marker_id}",
                        (pts_shelves[0][0], pts_shelves[0][1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 255),
                        2,
                    )

                    pose_6dof_shelf = {"rvec": rvecs_shelf[i].tolist(), "tvec": tvecs_shelf[i].tolist()}
                    marker_x, marker_y = tvecs_shelf[i][0][:2]
                    shelves.append(
                        {
                            "shelf_id": shelf_id,
                            "x": marker_x,
                            "y": marker_y,
                            "pose": pose_6dof_shelf,
                            "occupied_by_box_with_id": -1,
                        }
                    )
                    if shelf_id is not None:
                        shelf_ids.append(shelf_id)
                        shelf_corners.append(corners_shelf[i])


        return marker_ids, marker_poses, marker_corners, shelf_ids, shelves, shelf_corners
    
    def recognize_obstacles(self, boxes_masks: list[np.ndarray], 
                            shelf_masks: list[np.ndarray],
                            class_ids: list[int]) -> tuple[list[bool], bool]:
        # Checking whether box is on the floor
        filtered_flags = []
        for box_mask in boxes_masks:
            on_shelf = False
            for shelf_mask in shelf_masks:
                if np.multiply(box_mask, shelf_mask).sum() > 0:
                    on_shelf = True
                    break
            if not on_shelf:
                filtered_flags.append(True)
            else:
                filtered_flags.append(False)
            
        return filtered_flags, 2 in class_ids

    def check_box_sizes(self, depth_map: np.ndarray, poses: list[dict],
                        marker_ids: list[int], masks: list[np.ndarray]) -> bool:
        right_size_flags = True
        point_cloud = self.plane_detector.get_point_cloud(depth_map)
        # Calculating mean distance to boxes to know current way point
        mean_z = 0
        for pose in poses:
            z = pose["tvec"][0][-1]
            mean_z += z
        if len(poses) == 0:
            mean_z = 0
        else:
            mean_z /= len(poses)
        if mean_z >= 0.6:
            threshold = 0.05
        else:
            threshold = 0.03
        for marker_id, mask_box in zip(marker_ids, masks):
            # Check if aruco id is in reference
            if marker_id in self.aruco_size_reference:
                ref_width, ref_height = self.aruco_size_reference[marker_id]
                detected_width, detected_height = self.plane_detector.get_plane_size(
                    point_cloud, mask_box, threshold=threshold, img=None
                )
                tolerance = 0.3
                is_correct_size = (1 - tolerance) * ref_width <= detected_width <= (1 + tolerance) * ref_width and (
                    1 - tolerance
                ) * ref_height <= detected_height <= (1 + tolerance) * ref_height
                print(detected_width, ref_width, detected_height, ref_height)
                errors.append(min(detected_height / ref_height, ref_height / detected_height))
                errors.append(min(detected_width / ref_width, ref_width / detected_width))
                if not is_correct_size:
                    # If at least one size is incorrect the flag is False
                    right_size_flags = False

        return right_size_flags if len(marker_ids) != 0 else False

    def fuse_mask_aruco(self, marker_corners: list[np.ndarray],
                        boxes: list[list[int]],
                        class_ids: list[int],
                        marker_ids: list[int],
                        filtered_flags: list[bool], shelf_corners: list[np.ndarray],
                        shelf_ids: list[int], shelves: list[dict]) -> tuple[list[dict], list[dict], bool, Graph]:
        # For each box/container associate the closest shelf
        boxes_output = []
        for cur_ind, box_corner in enumerate(marker_corners):
            if box_corner is None or filtered_flags[cur_ind]:
                boxes_output.append({"box_id": 0, "placed_on_shelf_with_id": -1})
                continue
            top_left_box, bottom_right_box = box_corner[0], box_corner[2]
            box_center = (
                int((top_left_box[1] + bottom_right_box[1]) / 2),
                int((top_left_box[0] + bottom_right_box[0]) / 2),
            )
            min_ind = -1
            min_distance = 1e12
            for ind, shelf_corner in enumerate(shelf_corners):
                top_left_shelf, bottom_right_shelf = (shelf_corner[0][0], shelf_corner[0][2])
                shelf_center = (
                    int((top_left_shelf[1] + bottom_right_shelf[1]) / 2),
                    int((top_left_shelf[0] + bottom_right_shelf[0]) / 2),
                )
                distance = math.dist(box_center, shelf_center)
                if distance < min_distance:
                    min_distance = distance
                    min_ind = ind

            if min_ind == -1:
                boxes_output.append({"box_id": marker_ids[cur_ind], "placed_on_shelf_with_id": -1})
            else:
                boxes_output.append(
                    {"box_id": marker_ids[cur_ind], "placed_on_shelf_with_id": shelf_ids[min_ind]}
                )
            if 0 <= min_ind < len(shelves):  # Ensure min_ind is within valid bounds
                shelves[min_ind]["occupied_by_box_with_id"] = marker_ids[cur_ind]

        # Looking for boxes on another boxes
        box_on_box = False
        message = None

        for i, current_box in enumerate(boxes):
            if class_ids[i] == 0:  # only fo boxes
                x_min, y_min, x_max, y_max = current_box
                # The area above box
                top_region_y_max = y_min - 10

                for j, other_box in enumerate(boxes):
                    # Looking for the second box
                    if i != j and class_ids[j] == 0:
                        other_x_min, other_y_min, other_x_max, other_y_max = other_box
                        # Checking if one box is on the another
                        if (
                                other_x_min < x_max
                                and other_x_max > x_min
                                and other_y_max > top_region_y_max
                                and other_y_min < y_min
                        ):
                            box_on_box = True
                            message = Graph(
                                id_1=marker_ids[i],  # id of the first box
                                id_2=marker_ids[j],  # id of the second box
                                rel_id=2,
                                class_name_1="box",
                                rel_name="on_top",
                                class_name_2="box",
                            )
                            break
                if box_on_box:
                    break

        return shelves, boxes_output, box_on_box, message

    def segment_image(self, image_path: str) -> SegAndTrackResponse:
        img = cv2.imread(image_path)
        h, w = img.shape[:2]
        new_matr = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(
            self.camera_matrix, self.dist_fish, (w, h), None
        )
        img = cv2.fisheye.undistortImage(img, K=self.camera_matrix, D=self.dist_fish, Knew=new_matr)
        # Getting depth map of an image before any processing
        depth_map = self.depth_evaluator.get_depth_map(
            img, self.aruco_dict, self.aruco_params, self.camera_matrix, self.dist_coeffs
        )
        # Getting segmentation
        conf, class_ids, boxes, scaled_masks = self.segment_image_(img, h, w)
        # Detecting aruco markers
        rois = get_masks_rois(scaled_masks)
        masks_in_rois = get_masks_in_rois(scaled_masks, rois)
        marker_ids, marker_poses, marker_corners, shelf_ids, shelves, shelf_corners = self.detect_aruco(img, masks_in_rois, rois)
        # Handling duplicates in marker ids
        unique_ids = set(marker_ids)
        for marker_id in unique_ids:
            indices = [i for i, id_ in enumerate(marker_ids) if id_ == marker_id]
            if len(indices) > 1:
                # Leaving only one aruco marker with the biggest area
                areas = [
                    cv2.contourArea(cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0][0])
                    for i, mask in enumerate(masks_in_rois)
                    if i in indices
                ]
                max_area_index = indices[np.argmax(areas)]
                for i in indices:
                    if i != max_area_index:
                        marker_ids.pop(i)
                        conf.pop(i)
                        class_ids.pop(i)
                        boxes.pop(i)
                        np.delete(masks_in_rois, i, axis=0)
                        np.delete(rois, i, axis=0)

        mask_messages = [to_mask_msg(mask_in_roi, roi, w, h) for mask_in_roi, roi in zip(masks_in_rois, rois)]
        masks_in_rois = reconstruct_masks(mask_messages)
        # Getting only boxes and containers
        filtered_indices = [i for i, class_id in enumerate(class_ids) if class_id in [0, 1]]
        shelves_indices = [i for i, class_id in enumerate(class_ids) if class_id == 3]
        filtered_marker_ids = [marker_ids[i] for i in filtered_indices if i < len(marker_ids)]
        filtered_marker_poses = [marker_poses[i] for i in filtered_indices if i < len(marker_poses)]
        filtered_boxes = [boxes[i] for i in filtered_indices if i < len(boxes)]
        filtered_conf = [conf[i] for i in filtered_indices if i < len(conf)]
        filtered_marker_corners = [marker_corners[i] for i in filtered_indices if i < len(marker_corners)]
        filtered_class_ids = [class_ids[i] for i in filtered_indices if i < len(class_ids)]
        filtered_masks_in_rois = [masks_in_rois[i] for i in filtered_indices if i < len(masks_in_rois)]

        # Obstalce recognition
        shelf_masks = [masks_in_rois[i] for i in shelves_indices]
        filtered_flags, man_in_frame = self.recognize_obstacles(filtered_masks_in_rois, shelf_masks, class_ids)
        
        # Checking sizes of boxes and containers
        right_size_flags = self.check_box_sizes(depth_map, filtered_marker_poses, filtered_marker_ids, filtered_masks_in_rois)
        
        # Associating boxes/containers with the shelves
        shelves, boxes_output, box_on_box, message = self.fuse_mask_aruco(
            filtered_marker_corners, filtered_boxes, 
            filtered_class_ids, filtered_marker_ids, 
            filtered_flags, shelf_corners, 
            shelf_ids, shelves
        )
        # Visualization of the results
        img_with_masks = draw_objects(
            img,
            scores=conf,
            objects_ids=class_ids,
            boxes=boxes,
            masks=masks_in_rois,
            draw_scores=True,
            draw_ids=True,
            draw_boxes=False,
            draw_masks=True,
            palette=self.colors_palette,
            color_by_object_id=True,
        )

        # Box or container in the frame
        box_or_container_in_frame = any(cls_id in [0, 1] for cls_id in class_ids)
        # Constructing response
        boxes_response = [
            Box(x_min=int(box[0]), y_min=int(box[1]), x_max=int(box[2]), y_max=int(box[3])) for box in filtered_boxes
        ]
        poses_response = [
            Pose(
                rvec=[[round(elem, 3) for elem in pose["rvec"][0]]], tvec=[[round(elem, 3) for elem in pose["tvec"][0]]]
            )
            if pose is not None
            else Pose(rvec=[0, 0, 0], tvec=[0, 0, 0])
            for pose in filtered_marker_poses
        ]
        # Shelves processing
        for shelve in shelves:
            shelve["x"] = round(shelve["x"], 3)
            shelve["y"] = round(shelve["y"], 3)
            shelve["pose"]["rvec"] = [[round(elem, 3) for elem in shelve["pose"]["rvec"][0]]]
            shelve["pose"]["tvec"] = [[round(elem, 3) for elem in shelve["pose"]["tvec"][0]]]

        response = SegAndTrackResponse(
            count_box_and_containers=len(filtered_conf),
            scores=[round(score, 3) for score in filtered_conf],
            classes_ids=filtered_class_ids,
            tracking_ids=filtered_marker_ids,
            boxes=boxes_response,
            poses=poses_response,
            box_on_box=box_on_box,
            man_in_frame=man_in_frame,
            box_container_on_floor=any(filtered_flags),
            box_or_container_in_frame=box_or_container_in_frame,
            right_size_flags=right_size_flags,
            boxes_output=boxes_output,
            shelves=shelves,
            graph_box_on_box=message,
        )
        print(response.json())
        print(test_cases['test_case_' + image_path.split('/')[-1].split('.')[0]].response.json())
        assert response.json() == test_cases['test_case_' + image_path.split('/')[-1].split('.')[0]].response.json()

        task_id = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S_") + str(uuid.uuid4())
        # save_output(
        #     task_id,
        #     image_path,
        #     response,
        #     img_with_masks,
        #     base_dir=datetime.datetime.now().strftime("%Y-%m-%d"),
        # )
        task_id = "latest"
        # save_output(task_id, image_path, response, img_with_masks)
        # path = '/home/sashadance/python_projects/seg_and_track/seg_and_track_v2/services/seg_and_track/tests/data/output_images'
        # save_json(response.dict(), pathlib.Path(path + f"/{image_path.split('/')[-1].split('.')[0]}.json"))
        # cv2.imwrite(path + f"/{image_path.split('/')[-1]}", img_with_masks)

        return response

if __name__ == '__main__':
    seg = SegAndTrack()
    base_path = '/home/sashadance/python_projects/seg_and_track/seg_and_track_v2/services/seg_and_track/tests/data/images'
    for img_pth in ['wp0.png', 'wp1.png', 'wp1_2box.png', 'wp2.png', 'wp3.png']:
        seg.segment_image(os.path.join(base_path, img_pth))
    print(np.array(errors).mean())



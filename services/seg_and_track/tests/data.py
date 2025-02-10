from pathlib import Path
from pydantic.v1 import BaseModel
from services_api.seg_and_track import SegAndTrackRequest, SegAndTrackResponse

BASE_DIR = Path(__file__).resolve().parent / "data/images"




class TestCase(BaseModel):
    name: str
    request: SegAndTrackRequest
    response: SegAndTrackResponse
    response_comparator: object = lambda checked_response, target_response: checked_response == target_response



test_case_wp0 = {
    "count_box_and_containers": 5,
    "scores": [0.952, 0.94, 0.936, 0.927, 0.763],
    "classes_ids": [1, 0, 0, 1, 0],
    "tracking_ids": [0, 998, 313, 990, 4],
    "boxes": [
        {"x_min": 1132, "y_min": 560, "x_max": 1295, "y_max": 708},
        {"x_min": 262, "y_min": 359, "x_max": 401, "y_max": 466},
        {"x_min": 427, "y_min": 373, "x_max": 537, "y_max": 444},
        {"x_min": 674, "y_min": 355, "x_max": 816, "y_max": 423},
        {"x_min": 1422, "y_min": 89, "x_max": 1439, "y_max": 215},
    ],
    "poses": [
        {"rvec": [[0.0, 0.0, 0.0]], "tvec": [[0.0, 0.0, 0.0]]},
        {"rvec": [[-2.636, 0.217, -1.21]], "tvec": [[-0.703, -0.28, 0.857]]},
        {"rvec": [[-2.787, 0.084, -0.699]], "tvec": [[-0.472, -0.318, 1.064]]},
        {"rvec": [[-2.653, 0.067, -0.725]], "tvec": [[0.122, -0.484, 1.543]]},
        {"rvec": [[0.0, 0.0, 0.0]], "tvec": [[0.0, 0.0, 0.0]]},
    ],
    "box_on_box": False,
    "man_in_frame": True,
    "box_container_on_floor": True,
    "box_or_container_in_frame": True,
    "right_size_flags": True,
    "boxes_output": [
        {"box_id": 0, "placed_on_shelf_with_id": -1},
        {"box_id": 998, "placed_on_shelf_with_id": 1},
        {"box_id": 313, "placed_on_shelf_with_id": 2},
        {"box_id": 990, "placed_on_shelf_with_id": 3},
        {"box_id": 0, "placed_on_shelf_with_id": -1},
    ],
    "shelves": [
        {
            "shelf_id": 3,
            "x": 0.107,
            "y": -0.297,
            "occupied_by_box_with_id": 990,
            "pose": {"rvec": [[-2.759, 0.178, -0.921]], "tvec": [[0.107, -0.297, 1.569]]},
        },
        {
            "shelf_id": 4,
            "x": 0.378,
            "y": -0.357,
            "occupied_by_box_with_id": -1,
            "pose": {"rvec": [[3.188, -0.221, 1.085]], "tvec": [[0.378, -0.357, 1.756]]},
        },
        {
            "shelf_id": 1,
            "x": -0.698,
            "y": -0.101,
            "occupied_by_box_with_id": 998,
            "pose": {"rvec": [[-2.962, 0.307, -0.998]], "tvec": [[-0.698, -0.101, 0.92]]},
        },
        {
            "shelf_id": 2,
            "x": -0.427,
            "y": -0.164,
            "occupied_by_box_with_id": 313,
            "pose": {"rvec": [[-2.711, 0.166, -0.919]], "tvec": [[-0.427, -0.164, 1.126]]},
        },
        {
            "shelf_id": 5,
            "x": 0.878,
            "y": -0.351,
            "occupied_by_box_with_id": -1,
            "pose": {"rvec": [[-2.967, -0.106, -0.009]], "tvec": [[0.878, -0.351, 1.754]]},
        },
    ],
    "graph_box_on_box": None,
}

test_case_wp1 = {
    "count_box_and_containers": 4,
    "scores": [0.948, 0.941, 0.887, 0.679],
    "classes_ids": [0, 1, 1, 1],
    "tracking_ids": [313, 990, 1, 5],
    "boxes": [
        {"x_min": 388, "y_min": 314, "x_max": 706, "y_max": 544},
        {"x_min": 861, "y_min": 242, "x_max": 1346, "y_max": 559},
        {"x_min": 1396, "y_min": 423, "x_max": 1439, "y_max": 551},
        {"x_min": 1310, "y_min": 411, "x_max": 1364, "y_max": 525},
    ],
    "poses": [
        {"rvec": [[-2.833, 0.021, -0.188]], "tvec": [[-0.112, -0.079, 0.333]]},
        {"rvec": [[-2.739, 0.01, 0.004]], "tvec": [[0.327, -0.081, 0.277]]},
        {"rvec": [[0.0, 0.0, 0.0]], "tvec": [[0.0, 0.0, 0.0]]},
        {"rvec": [[0.0, 0.0, 0.0]], "tvec": [[0.0, 0.0, 0.0]]},
    ],
    "box_on_box": False,
    "man_in_frame": True,
    "box_container_on_floor": False,
    "box_or_container_in_frame": True,
    "right_size_flags": True,
    "boxes_output": [
        {"box_id": 313, "placed_on_shelf_with_id": 1},
        {"box_id": 990, "placed_on_shelf_with_id": 2},
        {"box_id": 0, "placed_on_shelf_with_id": -1},
        {"box_id": 0, "placed_on_shelf_with_id": -1},
    ],
    "shelves": [
        {
            "shelf_id": 1,
            "x": -0.068,
            "y": 0.089,
            "occupied_by_box_with_id": 313,
            "pose": {"rvec": [[-2.874, 0.009, -0.023]], "tvec": [[-0.068, 0.089, 0.336]]},
        },
        {
            "shelf_id": 2,
            "x": 0.273,
            "y": 0.087,
            "occupied_by_box_with_id": 990,
            "pose": {"rvec": [[-2.845, 0.044, -0.004]], "tvec": [[0.273, 0.087, 0.339]]},
        },
    ],
    "graph_box_on_box": None,
}

test_case_wp1_2box = {
    "count_box_and_containers": 5,
    "scores": [0.945, 0.945, 0.944, 0.943, 0.86],
    "classes_ids": [0, 1, 1, 0, 1],
    "tracking_ids": [998, 0, 999, 1, 5],
    "boxes": [
        {"x_min": 408, "y_min": 220, "x_max": 866, "y_max": 556},
        {"x_min": 1236, "y_min": 381, "x_max": 1366, "y_max": 529},
        {"x_min": 887, "y_min": 286, "x_max": 1245, "y_max": 540},
        {"x_min": 512, "y_min": 85, "x_max": 800, "y_max": 233},
        {"x_min": 1396, "y_min": 400, "x_max": 1439, "y_max": 558},
    ],
    "poses": [
        {"rvec": [[-2.869, 0.013, -0.018]], "tvec": [[-0.053, -0.094, 0.29]]},
        {"rvec": [[0.0, 0.0, 0.0]], "tvec": [[0.0, 0.0, 0.0]]},
        {"rvec": [[-2.781, -0.001, -0.019]], "tvec": [[0.278, -0.078, 0.319]]},
        {"rvec": [[0.0, 0.0, 0.0]], "tvec": [[0.0, 0.0, 0.0]]},
        {"rvec": [[0.0, 0.0, 0.0]], "tvec": [[0.0, 0.0, 0.0]]},
    ],
    "box_on_box": True,
    "man_in_frame": True,
    "box_container_on_floor": True,
    "box_or_container_in_frame": True,
    "right_size_flags": True,
    "boxes_output": [
        {"box_id": 998, "placed_on_shelf_with_id": 1},
        {"box_id": 0, "placed_on_shelf_with_id": -1},
        {"box_id": 999, "placed_on_shelf_with_id": 2},
        {"box_id": 0, "placed_on_shelf_with_id": -1},
        {"box_id": 0, "placed_on_shelf_with_id": -1},
    ],
    "shelves": [
        {
            "shelf_id": 1,
            "x": -0.068,
            "y": 0.089,
            "occupied_by_box_with_id": 998,
            "pose": {"rvec": [[-2.874, 0.009, -0.023]], "tvec": [[-0.068, 0.089, 0.336]]},
        },
        {
            "shelf_id": 2,
            "x": 0.272,
            "y": 0.086,
            "occupied_by_box_with_id": 999,
            "pose": {"rvec": [[-2.844, 0.039, 0.003]], "tvec": [[0.272, 0.086, 0.338]]},
        },
    ],
    "graph_box_on_box": {
        "id_1": 998,
        "id_2": 1,
        "rel_id": 2,
        "class_name_1": "box",
        "rel_name": "on_top",
        "class_name_2": "box",
    },
}

test_case_wp2 = {
    "count_box_and_containers": 4,
    "scores": [0.985, 0.942, 0.83, 0.491],
    "classes_ids": [1, 1, 0, 0],
    "tracking_ids": [990, 999, 5, 6],
    "boxes": [
        {"x_min": 215, "y_min": 168, "x_max": 854, "y_max": 578},
        {"x_min": 840, "y_min": 252, "x_max": 1260, "y_max": 568},
        {"x_min": 0, "y_min": 333, "x_max": 39, "y_max": 555},
        {"x_min": 0, "y_min": 419, "x_max": 40, "y_max": 557},
    ],
    "poses": [
        {"rvec": [[-2.771, 0.017, -0.014]], "tvec": [[-0.109, -0.068, 0.235]]},
        {"rvec": [[-2.784, 0.001, -0.037]], "tvec": [[0.223, -0.058, 0.262]]},
        {"rvec": [[0.0, 0.0, 0.0]], "tvec": [[0.0, 0.0, 0.0]]},
        {"rvec": [[0.0, 0.0, 0.0]], "tvec": [[0.0, 0.0, 0.0]]},
    ],
    "box_on_box": True,
    "man_in_frame": False,
    "box_container_on_floor": False,
    "box_or_container_in_frame": True,
    "right_size_flags": True,
    "boxes_output": [
        {"box_id": 990, "placed_on_shelf_with_id": 3},
        {"box_id": 999, "placed_on_shelf_with_id": 4},
        {"box_id": 0, "placed_on_shelf_with_id": -1},
        {"box_id": 0, "placed_on_shelf_with_id": -1},
    ],
    "shelves": [
        {
            "shelf_id": 3,
            "x": -0.105,
            "y": 0.104,
            "occupied_by_box_with_id": 990,
            "pose": {"rvec": [[-2.911, 0.012, -0.048]], "tvec": [[-0.105, 0.104, 0.277]]},
        },
        {
            "shelf_id": 4,
            "x": 0.227,
            "y": 0.102,
            "occupied_by_box_with_id": 999,
            "pose": {"rvec": [[-2.898, 0.013, -0.027]], "tvec": [[0.227, 0.102, 0.29]]},
        },
    ],
    "graph_box_on_box": {
        "id_1": 6,
        "id_2": 5,
        "rel_id": 2,
        "class_name_1": "box",
        "rel_name": "on_top",
        "class_name_2": "box",
    },
}

test_case_wp3 = {
    "count_box_and_containers": 3,
    "scores": [0.95, 0.791, 0.686],
    "classes_ids": [1, 1, 1],
    "tracking_ids": [1, 4, 5],
    "boxes": [
        {"x_min": 954, "y_min": 614, "x_max": 1160, "y_max": 813},
        {"x_min": 911, "y_min": 618, "x_max": 946, "y_max": 713},
        {"x_min": 1392, "y_min": 687, "x_max": 1439, "y_max": 866},
    ],
    "poses": [
        {"rvec": [[0.0, 0.0, 0.0]], "tvec": [[0.0, 0.0, 0.0]]},
        {"rvec": [[0.0, 0.0, 0.0]], "tvec": [[0.0, 0.0, 0.0]]},
        {"rvec": [[0.0, 0.0, 0.0]], "tvec": [[0.0, 0.0, 0.0]]},
    ],
    "box_on_box": False,
    "man_in_frame": False,
    "box_container_on_floor": True,
    "box_or_container_in_frame": True,
    "right_size_flags": True,
    "boxes_output": [
        {"box_id": 0, "placed_on_shelf_with_id": -1},
        {"box_id": 0, "placed_on_shelf_with_id": -1},
        {"box_id": 0, "placed_on_shelf_with_id": -1},
    ],
    "shelves": [
        {
            "shelf_id": 5,
            "x": 0.042,
            "y": 0.076,
            "occupied_by_box_with_id": -1,
            "pose": {"rvec": [[-2.822, 0.003, -0.014]], "tvec": [[0.042, 0.076, 0.363]]},
        }
    ],
    "graph_box_on_box": None,
}

test_case_head_person_two_boxes = {
    "count_box_and_containers": 2,
    "scores": [0.945, 0.941],
    "classes_ids": [1, 0],
    "tracking_ids": [990, 998],
    "boxes": [
        {"x_min": 595, "y_min": 300, "x_max": 901, "y_max": 583},
        {"x_min": 871, "y_min": 357,"x_max": 1114, "y_max": 649},
    ],
    "poses": [
        {"rvec": [[-2.187, -0.27, 0.382]], "tvec": [[-0.01,-0.077, 0.74]]},
        {"rvec": [[-2.306, -0.324, 0.369]], "tvec": [[0.316, 0.002, 0.656]]},
    ],
    "box_on_box": False,
    "man_in_frame": True,
    "box_container_on_floor": False,
    "box_or_container_in_frame": True,
    "right_size_flags": False,
    "boxes_output": [
        {"box_id": 990, "placed_on_shelf_with_id": 2},
        {"box_id": 998, "placed_on_shelf_with_id": 2},
    ],
    "shelves": [
        {
            "shelf_id": 2,
            "x": 0.264,
            "y": 0.135,
            "occupied_by_box_with_id": 998,
            "pose": {"rvec": [[-2.281, -0.278, 0.371]], "tvec": [[0.264, 0.135, 0.8]]},
        },
    ],
    "graph_box_on_box": None,
}

test_case_head_with_box = {
    "count_box_and_containers": 2,
    "scores": [0.953, 0.439],
    "classes_ids": [1, 0],
    "tracking_ids": [999, 5],
    "boxes": [
        {"x_min": 1110, "y_min": 507, "x_max": 1286, "y_max": 740},
        {"x_min": 1273, "y_min": 637, "x_max": 1287, "y_max": 732},
    ],
    "poses": [
        {"rvec": [[-2.232, -0.627, 0.899]], "tvec": [[0.616, 0.15, 0.62]]},
        {"rvec": [[0.0, 0.0, 0.0]], "tvec": [[0.0, 0.0, 0.0]]},
    ],
    "box_on_box": False,
    "man_in_frame": False,
    "box_container_on_floor": False,
    "box_or_container_in_frame": True,
    "right_size_flags": False,
    "boxes_output": [
        {"box_id": 999, "placed_on_shelf_with_id": 5},
        {"box_id": 0, "placed_on_shelf_with_id": -1},
    ],
    "shelves": [
        {
            "shelf_id": 5,
            "x": 0.556,
            "y": 0.41,
            "occupied_by_box_with_id": 999,
            "pose": {"rvec": [[-1.908, -0.919, 1.593]], "tvec": [[0.556, 0.41, 0.612]]},
        },
    ],
    "graph_box_on_box": None,
}

test_case_several_shelf_places = {
    "count_box_and_containers": 3,
    "scores": [0.954, 0.95, 0.915],
    "classes_ids": [1, 1, 0],
    "tracking_ids": [990, 999, 998],
    "boxes": [
        {"x_min": 464, "y_min": 281, "x_max": 730, "y_max": 504},
        {"x_min": 769, "y_min": 310, "x_max": 934, "y_max": 501},
        {"x_min": 118, "y_min": 299, "x_max": 297, "y_max": 457},
    ],
    "poses": [
        {"rvec": [[-2.213, -0.136, -0.004]], "tvec": [[-0.172, -0.154, 0.747]]},
        {"rvec": [[-2.249, -0.154, 0.052]], "tvec": [[0.167, -0.158, 0.818]]},
        {"rvec": [[-2.3, -0.174, 0.103]], "tvec": [[-1.168, -0.314, 0.772]]},
    ],
    "box_on_box": False,
    "man_in_frame": False,
    "box_container_on_floor": False,
    "box_or_container_in_frame": True,
    "right_size_flags": False,
    "boxes_output": [
        {"box_id": 990, "placed_on_shelf_with_id": 3},
        {"box_id": 999, "placed_on_shelf_with_id": 4},
        {"box_id": 998, "placed_on_shelf_with_id": 1},
    ],
    "shelves": [
        {
            "shelf_id": 4,
            "x": 0.197,
            "y": -0.036,
            "occupied_by_box_with_id": 999,
            "pose": {"rvec": [[-2.333, -0.105, -0.117]], "tvec": [[0.197, -0.036, 0.924]]},
        },
        {
            "shelf_id": 3,
            "x": -0.139,
            "y": -0.058,
            "occupied_by_box_with_id": 990,
            "pose": {"rvec": [[-2.287, -0.124, -0.052]], "tvec": [[-0.139, -0.058, 0.933]]},
        },
        {
            "shelf_id": 2,
            "x": -0.863,
            "y": -0.136,
            "occupied_by_box_with_id": -1,
            "pose": {"rvec": [[-2.316, -0.139, 0.039]], "tvec": [[-0.863, -0.136, 0.952]]},
        },
        {
            "shelf_id": 1,
            "x": -1.194,
            "y": -0.179,
            "occupied_by_box_with_id": 998,
            "pose": {"rvec": [[-2.309, -0.163, 0.076]], "tvec": [[-1.194, -0.179, 0.918]]},
        },
        {
            "shelf_id": 5,
            "x": 0.57,
            "y": 0.204,
            "occupied_by_box_with_id": -1,
            "pose": {"rvec": [[-1.817, -0.948, 1.709]], "tvec": [[0.57, 0.204, 0.778]]},
        },
    ],
    "graph_box_on_box": None,
}

tests = [
    TestCase(
        name="test_case_wp0",
        request=SegAndTrackRequest(image_path=str(BASE_DIR / "wp0.png")),
        response=SegAndTrackResponse(**test_case_wp0),
    ),
    TestCase(
        name="test_case_wp1",
        request=SegAndTrackRequest(image_path=str(BASE_DIR / "wp1.png")),
        response=SegAndTrackResponse(**test_case_wp1),
    ),
    TestCase(
        name="test_case_wp1_2box",
        request=SegAndTrackRequest(image_path=str(BASE_DIR / "wp1_2box.png")),
        response=SegAndTrackResponse(**test_case_wp1_2box),
    ),
    TestCase(
        name="test_case_wp2",
        request=SegAndTrackRequest(image_path=str(BASE_DIR / "wp2.png")),
        response=SegAndTrackResponse(**test_case_wp2),
    ),
    TestCase(
        name="test_case_wp3",
        request=SegAndTrackRequest(image_path=str(BASE_DIR / "wp3.png")),
        response=SegAndTrackResponse(**test_case_wp3),
    ),
    TestCase(
        name="test_case_head_person_two_boxes",
        request=SegAndTrackRequest(image_path=str(BASE_DIR / "head_person_two_boxes.png")),
        response=SegAndTrackResponse(**test_case_head_person_two_boxes),
    ),
    TestCase(
        name="test_case_head_with_box",
        request=SegAndTrackRequest(image_path=str(BASE_DIR / "head_with_box.png")),
        response=SegAndTrackResponse(**test_case_head_with_box),
    ),
    TestCase(
        name="test_case_several_shelf_places",
        request=SegAndTrackRequest(image_path=str(BASE_DIR / "several_shelf_places.png")),
        response=SegAndTrackResponse(**test_case_several_shelf_places),
    ),
]

test_cases = {test_case.name: test_case for test_case in tests}
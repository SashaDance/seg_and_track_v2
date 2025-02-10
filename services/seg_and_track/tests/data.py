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
    "count_box_and_containers": 4,
    "scores": [
        0.952,
        0.945,
        0.932,
        0.913
    ],
    "classes_ids": [
        1,
        0,
        0,
        1
    ],
    "tracking_ids": [
        0,
        998,
        313,
        990
    ],
    "boxes": [
        {
            "x_min": 1173,
            "y_min": 556,
            "x_max": 1316,
            "y_max": 714
        },
        {
            "x_min": 231,
            "y_min": 335,
            "x_max": 361,
            "y_max": 459
        },
        {
            "x_min": 388,
            "y_min": 339,
            "x_max": 502,
            "y_max": 427
        },
        {
            "x_min": 662,
            "y_min": 311,
            "x_max": 832,
            "y_max": 388
        }
    ],
    "poses": [
        {
            "rvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            "tvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ]
        },
        {
            "rvec": [
                [
                    -3.03,
                    0.147,
                    -0.375
                ]
            ],
            "tvec": [
                [
                    -0.71,
                    -0.286,
                    0.754
                ]
            ]
        },
        {
            "rvec": [
                [
                    -3.081,
                    0.064,
                    -0.023
                ]
            ],
            "tvec": [
                [
                    -0.472,
                    -0.321,
                    0.89
                ]
            ]
        },
        {
            "rvec": [
                [
                    -2.668,
                    0.057,
                    -0.585
                ]
            ],
            "tvec": [
                [
                    0.127,
                    -0.518,
                    1.325
                ]
            ]
        }
    ],
    "box_on_box": False,
    "man_in_frame": True,
    "box_container_on_floor": True,
    "box_or_container_in_frame": True,
    "right_size_flags": False,
    "boxes_output": [
        {
            "box_id": 0,
            "placed_on_shelf_with_id": -1
        },
        {
            "box_id": 998,
            "placed_on_shelf_with_id": 1
        },
        {
            "box_id": 313,
            "placed_on_shelf_with_id": 2
        },
        {
            "box_id": 990,
            "placed_on_shelf_with_id": 3
        }
    ],
    "shelves": [
        {
            "shelf_id": 1,
            "x": -0.706,
            "y": -0.105,
            "occupied_by_box_with_id": 998,
            "pose": {
                "rvec": [
                    [
                        -3.062,
                        0.227,
                        -0.286
                    ]
                ],
                "tvec": [
                    [
                        -0.706,
                        -0.105,
                        0.802
                    ]
                ]
            }
        },
        {
            "shelf_id": 2,
            "x": -0.428,
            "y": -0.168,
            "occupied_by_box_with_id": 313,
            "pose": {
                "rvec": [
                    [
                        -2.454,
                        0.147,
                        -1.149
                    ]
                ],
                "tvec": [
                    [
                        -0.428,
                        -0.168,
                        0.929
                    ]
                ]
            }
        },
        {
            "shelf_id": 5,
            "x": 0.873,
            "y": -0.355,
            "occupied_by_box_with_id": -1,
            "pose": {
                "rvec": [
                    [
                        2.925,
                        0.209,
                        -1.971
                    ]
                ],
                "tvec": [
                    [
                        0.873,
                        -0.355,
                        1.462
                    ]
                ]
            }
        },
        {
            "shelf_id": 3,
            "x": 0.108,
            "y": -0.306,
            "occupied_by_box_with_id": 990,
            "pose": {
                "rvec": [
                    [
                        3.208,
                        -0.26,
                        0.994
                    ]
                ],
                "tvec": [
                    [
                        0.108,
                        -0.306,
                        1.267
                    ]
                ]
            }
        },
        {
            "shelf_id": 4,
            "x": 0.393,
            "y": -0.373,
            "occupied_by_box_with_id": -1,
            "pose": {
                "rvec": [
                    [
                        -2.785,
                        0.16,
                        -0.87
                    ]
                ],
                "tvec": [
                    [
                        0.393,
                        -0.373,
                        1.469
                    ]
                ]
            }
        }
    ],
    "graph_box_on_box": None
}

test_case_wp1 = {
    "count_box_and_containers": 4,
    "scores": [
        0.95,
        0.932,
        0.861,
        0.722
    ],
    "classes_ids": [
        0,
        1,
        1,
        1
    ],
    "tracking_ids": [
        313,
        990,
        2,
        5
    ],
    "boxes": [
        {
            "x_min": 350,
            "y_min": 267,
            "x_max": 702,
            "y_max": 538
        },
        {
            "x_min": 882,
            "y_min": 213,
            "x_max": 1358,
            "y_max": 556
        },
        {
            "x_min": 1403,
            "y_min": 421,
            "x_max": 1439,
            "y_max": 552
        },
        {
            "x_min": 1328,
            "y_min": 403,
            "x_max": 1374,
            "y_max": 524
        }
    ],
    "poses": [
        {
            "rvec": [
                [
                    -3.036,
                    0.035,
                    -0.029
                ]
            ],
            "tvec": [
                [
                    -0.114,
                    -0.082,
                    0.278
                ]
            ]
        },
        {
            "rvec": [
                [
                    -2.837,
                    -0.004,
                    -0.077
                ]
            ],
            "tvec": [
                [
                    0.337,
                    -0.085,
                    0.257
                ]
            ]
        },
        {
            "rvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            "tvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ]
        },
        {
            "rvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            "tvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ]
        }
    ],
    "box_on_box": False,
    "man_in_frame": True,
    "box_container_on_floor": False,
    "box_or_container_in_frame": True,
    "right_size_flags": False,
    "boxes_output": [
        {
            "box_id": 313,
            "placed_on_shelf_with_id": 1
        },
        {
            "box_id": 990,
            "placed_on_shelf_with_id": 2
        },
        {
            "box_id": 0,
            "placed_on_shelf_with_id": -1
        },
        {
            "box_id": 0,
            "placed_on_shelf_with_id": -1
        }
    ],
    "shelves": [
        {
            "shelf_id": 1,
            "x": -0.068,
            "y": 0.089,
            "occupied_by_box_with_id": 313,
            "pose": {
                "rvec": [
                    [
                        -2.862,
                        0.008,
                        0.049
                    ]
                ],
                "tvec": [
                    [
                        -0.068,
                        0.089,
                        0.275
                    ]
                ]
            }
        },
        {
            "shelf_id": 2,
            "x": 0.278,
            "y": 0.087,
            "occupied_by_box_with_id": 990,
            "pose": {
                "rvec": [
                    [
                        -2.89,
                        0.04,
                        -0.115
                    ]
                ],
                "tvec": [
                    [
                        0.278,
                        0.087,
                        0.301
                    ]
                ]
            }
        }
    ],
    "graph_box_on_box": None
}

test_case_wp1_2box = {
    "count_box_and_containers": 5,
    "scores": [
        0.958,
        0.946,
        0.946,
        0.92,
        0.845
    ],
    "classes_ids": [
        0,
        0,
        1,
        1,
        1
    ],
    "tracking_ids": [
        998,
        0,
        999,
        2,
        4
    ],
    "boxes": [
        {
            "x_min": 368,
            "y_min": 174,
            "x_max": 897,
            "y_max": 551
        },
        {
            "x_min": 494,
            "y_min": 50,
            "x_max": 808,
            "y_max": 192
        },
        {
            "x_min": 909,
            "y_min": 258,
            "x_max": 1271,
            "y_max": 538
        },
        {
            "x_min": 1261,
            "y_min": 371,
            "x_max": 1375,
            "y_max": 527
        },
        {
            "x_min": 1404,
            "y_min": 397,
            "x_max": 1439,
            "y_max": 556
        }
    ],
    "poses": [
        {
            "rvec": [
                [
                    -3.057,
                    0.016,
                    0.011
                ]
            ],
            "tvec": [
                [
                    -0.054,
                    -0.097,
                    0.242
                ]
            ]
        },
        {
            "rvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            "tvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ]
        },
        {
            "rvec": [
                [
                    -2.888,
                    -0.009,
                    -0.093
                ]
            ],
            "tvec": [
                [
                    0.286,
                    -0.082,
                    0.287
                ]
            ]
        },
        {
            "rvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            "tvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ]
        },
        {
            "rvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            "tvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ]
        }
    ],
    "box_on_box": True,
    "man_in_frame": True,
    "box_container_on_floor": True,
    "box_or_container_in_frame": True,
    "right_size_flags": True,
    "boxes_output": [
        {
            "box_id": 998,
            "placed_on_shelf_with_id": 1
        },
        {
            "box_id": 0,
            "placed_on_shelf_with_id": -1
        },
        {
            "box_id": 999,
            "placed_on_shelf_with_id": 2
        },
        {
            "box_id": 0,
            "placed_on_shelf_with_id": -1
        },
        {
            "box_id": 0,
            "placed_on_shelf_with_id": -1
        }
    ],
    "shelves": [
        {
            "shelf_id": 1,
            "x": -0.068,
            "y": 0.089,
            "occupied_by_box_with_id": 998,
            "pose": {
                "rvec": [
                    [
                        -2.862,
                        0.008,
                        0.049
                    ]
                ],
                "tvec": [
                    [
                        -0.068,
                        0.089,
                        0.275
                    ]
                ]
            }
        },
        {
            "shelf_id": 2,
            "x": 0.278,
            "y": 0.087,
            "occupied_by_box_with_id": 999,
            "pose": {
                "rvec": [
                    [
                        -2.89,
                        0.04,
                        -0.115
                    ]
                ],
                "tvec": [
                    [
                        0.278,
                        0.087,
                        0.301
                    ]
                ]
            }
        }
    ],
    "graph_box_on_box": {
        "id_1": 998,
        "id_2": 0,
        "rel_id": 2,
        "class_name_1": "box",
        "rel_name": "on_top",
        "class_name_2": "box"
    }
}

test_case_wp2 = {
    "count_box_and_containers": 4,
    "scores": [
        0.99,
        0.938,
        0.791,
        0.264
    ],
    "classes_ids": [
        1,
        1,
        0,
        0
    ],
    "tracking_ids": [
        990,
        999,
        5,
        6
    ],
    "boxes": [
        {
            "x_min": 189,
            "y_min": 126,
            "x_max": 864,
            "y_max": 579
        },
        {
            "x_min": 854,
            "y_min": 218,
            "x_max": 1283,
            "y_max": 568
        },
        {
            "x_min": 0,
            "y_min": 332,
            "x_max": 34,
            "y_max": 555
        },
        {
            "x_min": 0,
            "y_min": 443,
            "x_max": 35,
            "y_max": 557
        }
    ],
    "poses": [
        {
            "rvec": [
                [
                    -2.938,
                    0.052,
                    0.023
                ]
            ],
            "tvec": [
                [
                    -0.113,
                    -0.072,
                    0.205
                ]
            ]
        },
        {
            "rvec": [
                [
                    -2.888,
                    -0.019,
                    -0.128
                ]
            ],
            "tvec": [
                [
                    0.229,
                    -0.061,
                    0.235
                ]
            ]
        },
        {
            "rvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            "tvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ]
        },
        {
            "rvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            "tvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ]
        }
    ],
    "box_on_box": True,
    "man_in_frame": False,
    "box_container_on_floor": False,
    "box_or_container_in_frame": True,
    "right_size_flags": True,
    "boxes_output": [
        {
            "box_id": 990,
            "placed_on_shelf_with_id": 3
        },
        {
            "box_id": 999,
            "placed_on_shelf_with_id": 4
        },
        {
            "box_id": 0,
            "placed_on_shelf_with_id": -1
        },
        {
            "box_id": 0,
            "placed_on_shelf_with_id": -1
        }
    ],
    "shelves": [
        {
            "shelf_id": 3,
            "x": -0.106,
            "y": 0.104,
            "occupied_by_box_with_id": 990,
            "pose": {
                "rvec": [
                    [
                        -2.899,
                        0.016,
                        0.054
                    ]
                ],
                "tvec": [
                    [
                        -0.106,
                        0.104,
                        0.235
                    ]
                ]
            }
        },
        {
            "shelf_id": 4,
            "x": 0.229,
            "y": 0.102,
            "occupied_by_box_with_id": 999,
            "pose": {
                "rvec": [
                    [
                        -2.918,
                        -0.001,
                        -0.141
                    ]
                ],
                "tvec": [
                    [
                        0.229,
                        0.102,
                        0.255
                    ]
                ]
            }
        }
    ],
    "graph_box_on_box": {
        "id_1": 6,
        "id_2": 5,
        "rel_id": 2,
        "class_name_1": "box",
        "rel_name": "on_top",
        "class_name_2": "box"
    }
}

test_case_wp3 = {
    "count_box_and_containers": 4,
    "scores": [
        0.939,
        0.807,
        0.719,
        0.263
    ],
    "classes_ids": [
        1,
        1,
        1,
        1
    ],
    "tracking_ids": [
        1,
        4,
        5,
        6
    ],
    "boxes": [
        {
            "x_min": 986,
            "y_min": 616,
            "x_max": 1196,
            "y_max": 841
        },
        {
            "x_min": 947,
            "y_min": 624,
            "x_max": 986,
            "y_max": 738
        },
        {
            "x_min": 1394,
            "y_min": 685,
            "x_max": 1439,
            "y_max": 848
        },
        {
            "x_min": 1205,
            "y_min": 691,
            "x_max": 1230,
            "y_max": 756
        }
    ],
    "poses": [
        {
            "rvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            "tvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ]
        },
        {
            "rvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            "tvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ]
        },
        {
            "rvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            "tvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ]
        },
        {
            "rvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            "tvec": [
                [
                    0.0,
                    0.0,
                    0.0
                ]
            ]
        }
    ],
    "box_on_box": False,
    "man_in_frame": False,
    "box_container_on_floor": True,
    "box_or_container_in_frame": True,
    "right_size_flags": True,
    "boxes_output": [
        {
            "box_id": 0,
            "placed_on_shelf_with_id": -1
        },
        {
            "box_id": 0,
            "placed_on_shelf_with_id": -1
        },
        {
            "box_id": 0,
            "placed_on_shelf_with_id": -1
        },
        {
            "box_id": 0,
            "placed_on_shelf_with_id": -1
        }
    ],
    "shelves": [
        {
            "shelf_id": 5,
            "x": 0.042,
            "y": 0.075,
            "occupied_by_box_with_id": -1,
            "pose": {
                "rvec": [
                    [
                        -2.815,
                        0.011,
                        -0.043
                    ]
                ],
                "tvec": [
                    [
                        0.042,
                        0.075,
                        0.293
                    ]
                ]
            }
        }
    ],
    "graph_box_on_box": None
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
    # TestCase(
    #     name="test_case_head_person_two_boxes",
    #     request=SegAndTrackRequest(image_path=str(BASE_DIR / "head_person_two_boxes.png")),
    #     response=SegAndTrackResponse(**test_case_head_person_two_boxes),
    # ),
    # TestCase(
    #     name="test_case_head_with_box",
    #     request=SegAndTrackRequest(image_path=str(BASE_DIR / "head_with_box.png")),
    #     response=SegAndTrackResponse(**test_case_head_with_box),
    # ),
    # TestCase(
    #     name="test_case_several_shelf_places",
    #     request=SegAndTrackRequest(image_path=str(BASE_DIR / "several_shelf_places.png")),
    #     response=SegAndTrackResponse(**test_case_several_shelf_places),
    # ),
]

test_cases = {test_case.name: test_case for test_case in tests}
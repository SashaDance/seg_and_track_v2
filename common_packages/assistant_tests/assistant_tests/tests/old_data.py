from . import response_comparators
from .models import Turn, TestCase

to_loader_flow_313_telemetry = {
    "images": [],
    "world_state": {
        "robot_position": [1.0, 1.0, 1.57],
        "boxes": [
            {"box_id": 313, "placed_on_shelf_with_id": 6},
        ],
        "shelves": [
            {"shelf_id": 1, "occupied_by_box_with_id": -1},
            {"shelf_id": 2, "occupied_by_box_with_id": -1},
            {"shelf_id": 3, "occupied_by_box_with_id": -1},
            {"shelf_id": 4, "occupied_by_box_with_id": -1},
            {"shelf_id": 5, "occupied_by_box_with_id": -1},
            {"shelf_id": 6, "occupied_by_box_with_id": 313},
        ],
    },
    "seg_track": [],
    "scene_graph": [],
}


to_loader_flow = TestCase(
    name="to_loader_flow",
    turns=[
        Turn(request="Привет, Квант", response="Добрый день, какой у вас вопрос?"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="Отнеси коробку", response="Поставьте коробку на стол выдачи штрих-кодом ко мне."),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(
            request_type="qr_code",
            request="313",
            response="Двигаюсь к погрузчику",
            telemetry=to_loader_flow_313_telemetry,
            response_comparator=response_comparators.is_in_say,
        ),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(
            request="Как погода?",
            response=" ",
            response_comparator=response_comparators.is_in_say,
        ),
    ],
)


failed_to_loader_flow = TestCase(
    name="failed_to_loader_flow",
    turns=[
        Turn(request="Привет, Квант", response="Добрый день, какой у вас вопрос?"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="Отнеси коробку", response="Поставьте коробку на стол выдачи штрих-кодом ко мне."),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(
            request_type="qr_code",
            request="313",
            response="Двигаюсь к погрузчику",
            telemetry=to_loader_flow_313_telemetry,
            response_comparator=response_comparators.is_in_say,
        ),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(
            request_type="error",
            request={
                "code": "software_error",
                "details": "Ошибка программы: software_error",
                "command": {"name": "drop"},
            },
            response="drop",
            telemetry={},
            response_comparator=response_comparators.is_command_in_plan,
        ),
    ],
)

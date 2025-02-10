from . import response_comparators
from . import turn_requests
from .models import Turn, TestCase


delivery_order_313_telemetry = {
    "images": [],
    "world_state": {
        "robot_position": [1.0, 1.0, 1.57],
        "boxes": [
            {"box_id": 313, "placed_on_shelf_with_id": 1},
            {"box_id": 990, "placed_on_shelf_with_id": 2},
            {"box_id": 998, "placed_on_shelf_with_id": 4},
            {"box_id": 999, "placed_on_shelf_with_id": 5},
        ],
        "shelves": [
            {"shelf_id": 1, "occupied_by_box_with_id": 313},
            {"shelf_id": 2, "occupied_by_box_with_id": 990},
            {"shelf_id": 3, "occupied_by_box_with_id": -1},
            {"shelf_id": 4, "occupied_by_box_with_id": 998},
            {"shelf_id": 5, "occupied_by_box_with_id": 999},
            {"shelf_id": 6, "occupied_by_box_with_id": -1},
        ],
    },
    "seg_track": [],
    "scene_graph": [
        {
            "id_1": 313,
            "timestamp_1": 17459802,
            "id_2": 990,
            "timestamp_2": 17459802,
            "rel_id": 2,
            "class_name_1": "box",
            "rel_name": "right",
            "class_name_2": "box",
        },
        {
            "id_1": 998,
            "timestamp_1": 17459802,
            "id_2": 999,
            "timestamp_2": 17459802,
            "rel_id": 2,
            "class_name_1": "box",
            "rel_name": "right",
            "class_name_2": "box",
        },
    ],
}

order_flow_not_found_no_questions = TestCase(
    name="order_flow_not_found_no_questions",
    turns=[
        Turn(request="Привет, Квант", response="Добрый день, какой у вас вопрос?"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(
            request="Хочу забрать заказ",
            response="Поднес+ите штрихк+од к, ск+анеру.",
            response_comparator=response_comparators.is_in_plan_with_ssml,
        ),
        Turn(
            request_type="success",
            request={
                "payload": "98172634912834",
                "command": {"name": "scan_code"},
            },
            response="К сожалению что-то пошло не так, ваш заказ не найден. Есть ли у вас еще вопросы?",
            success_requests=turn_requests.custom_cmd_success_requests,
            response_comparator=response_comparators.is_first_in_plan,
            aggregation=any,
        ),
        Turn(request="Нет", response="Заходите к, нам ещё, мы вам всегда рады."),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
    ],
)


order_flow_found = TestCase(
    name="order_flow_found",
    turns=[
        Turn(request="Привет, Квант", response="Добрый день, какой у вас вопрос?"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="Хочу забрать заказ", response="Поднесите штрих-код к сканеру."),
        Turn(
            request_type="success",
            request={
                "payload": "313",
                "command": {"name": "scan_code"},
            },
            response="Подождите несколько минут, я принесу ваш заказ.",
            success_requests=turn_requests.custom_cmd_success_requests,
            response_comparator=response_comparators.is_in_say,
            aggregation=any,
        ),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(
            request="да",
            response="Благодарим вас за покупку. Заходите к, нам ещё, мы вам всегда рады. Есть ли у вас еще вопросы?",
        ),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
    ],
)


autopilot_flow_requests = TestCase(
    name="autopilot_flow_requests",
    turns=[
        Turn(
            request="установить точку цифра",
            response="Установил точку назначения вход в Цифру",
            response_comparator=response_comparators.is_not_in_say,
        ),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="включить автопилот", response="Автопилот запущен, ожидаю команды"),
        # set_point
        # negative
        # 'Я же не знаю, сколько у меня расстояние.'
        # 'Нормально, правильно.'
        # set_point
        # negative
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(
            request="Поехали? Ну конечно. В команду. Давай.",
            response="set_point",
            response_comparator=response_comparators.is_command_not_in_plan,
        ),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(
            request="Это правило до пожирного места.",
            response="set_point",
            response_comparator=response_comparators.is_command_not_in_plan,
        ),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(
            request="Хардклоп поедет.",
            response="set_point",
            response_comparator=response_comparators.is_command_not_in_plan,
        ),
        ## вход в Цифру
        # В Цифру
        # В цифру!
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="В цифру!", response="Установил точку назначения вход в Цифру"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="доедь до цифры", response="Установил точку назначения вход в Цифру"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="едем до цифры", response="Установил точку назначения вход в Цифру"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="едем ко входу в цифру", response="Установил точку назначения вход в Цифру"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="установить точку ко входу в цифру", response="Установил точку назначения вход в Цифру"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="едем вперед до цифры", response="Установил точку назначения вход в Цифру"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="построй маршрут до цифры", response="Установил точку назначения вход в Цифру"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="построй маршрут до входа в цифру", response="Установил точку назначения вход в Цифру"),
        ## вход в Арктику
        # в Арктику.
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="в Арктику.", response="Установил точку назначения вход в Арктику"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="доедь до арктики", response="Установил точку назначения вход в Арктику"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="едем до арктики", response="Установил точку назначения вход в Арктику"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="едем ко входу в арктику", response="Установил точку назначения вход в Арктику"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="установить точку ко входу в арктику", response="Установил точку назначения вход в Арктику"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="едем вперед до арктики", response="Установил точку назначения вход в Арктику"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="построй маршрут до арктики", response="Установил точку назначения вход в Арктику"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="построй маршрут до входа в арктику", response="Установил точку назначения вход в Арктику"),
        ## гараж
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="Ехали в гараж.", response="Установил точку назначения гараж"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="или в гараж?", response="Установил точку назначения гараж"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="Дедь в гараж.", response="Установил точку назначения гараж"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="Гараж.", response="Установил точку назначения гараж"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="В Гараж", response="Установил точку назначения гараж"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="ГОРОЖ!", response="Установил точку назначения гараж"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="В ГАРАЖ!", response="Установил точку назначения гараж"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="доедь до гаража", response="Установил точку назначения гараж"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="едем до гаража", response="Установил точку назначения гараж"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="едем ко входу в гараж", response="Установил точку назначения гараж"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="установить точку ко входу в гараж", response="Установил точку назначения гараж"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="едем вперед до гаража", response="Установил точку назначения гараж"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="построй маршрут до гаража", response="Установил точку назначения гараж"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="построй маршрут до входа в гараж", response="Установил точку назначения гараж"),
        ## вход в ФизТех
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="МФТИ", response="Установил точку назначения вход в ФизТех"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="доедь до МФТИ", response="Установил точку назначения вход в ФизТех"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="едем до МФТИ", response="Установил точку назначения вход в ФизТех"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="едем ко входу в МФТИ", response="Установил точку назначения вход в ФизТех"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="установить точку ко входу в МФТИ", response="Установил точку назначения вход в ФизТех"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="едем вперед до МФТИ", response="Установил точку назначения вход в ФизТех"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="построй маршрут до Физтеха", response="Установил точку назначения вход в ФизТех"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="построй маршрут до входа в МФТИ", response="Установил точку назначения вход в ФизТех"),
        # go
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="едем вперед метр", response="Выполняю движение на расстояние 1 метр"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="едем вперед 2 метра", response="Выполняю движение на расстояние 2 метра"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="едем вперед три метра", response="Выполняю движение на расстояние 3 метра"),
        # Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),Turn(request="едем назад 3 метра", response="Выполняю движение на расстояние 3 метра"),
        # turn
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="направо", response="Выполняю поворот направо"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="поверни направо", response="Выполняю поворот направо"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="налево", response="Выполняю поворот налево"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="поверни налево", response="Выполняю поворот налево"),
        # status
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="какой статус", response="Докладываю статус: подключ+ение к, сет+и стабильное"),
        # stop
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="остановись", response="Останавливаюсь"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="стоять", response="Останавливаюсь"),
        # no cmd
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(
            request="Поговорим о чём-нибудь",
            response="Неизвестная команда для автопилота.",
            response_comparator=response_comparators.is_in_say,
        ),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="выключить автопилот", response="Автопилот выключен"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(
            request="установить точку цифра",
            response="Установил точку назначения Entrance_of_Cifra",
            response_comparator=response_comparators.is_not_in_say,
        ),
    ],
)


order_flow_real_requests = TestCase(
    name="order_flow_real_requests",
    turns=[
        Turn(request="Привет, Квант", response="Добрый день, какой у вас вопрос?"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(
            request="Хочу забрать заказ",
            response="Поднесите штрих-код к сканеру.",
        ),
        Turn(
            request_type="success",
            request={
                "payload": "313",
                "command": {"name": "scan_code"},
            },
            response="Подождите несколько минут, я принесу ваш заказ.",
            success_requests=turn_requests.custom_cmd_success_requests,
            response_comparator=response_comparators.is_in_say,
            aggregation=any,
        ),
        Turn(
            request_type="error",
            request={
                "code": "software_error",
                "details": "коробка стоит на коробка",
                "command": {"name": "pick_up"},
            },
            response="Произошла ошибка при выполнении поставленной задачи.",
            response_comparator=response_comparators.is_in_say,
            aggregation=any,
        ),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(
            request="Да",
            response="Благодарим вас за покупку. Заходите к, нам ещё, мы вам всегда рады. Есть ли у вас еще вопросы?",
        ),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="Нет", response="Заходите к, нам ещё, мы вам всегда рады."),
    ],
)


order_flow_failed_real_requests = TestCase(
    name="order_flow_failed_real_requests",
    turns=[
        Turn(request="Привет, Квант", response="Добрый день, какой у вас вопрос?"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="Хочу забрать заказ", response="Поднесите штрих-код к сканеру."),
        Turn(
            request_type="success",
            request={
                "payload": "313",
                "command": {"name": "scan_code"},
            },
            response="Подождите несколько минут, я принесу ваш заказ.",
            success_requests=turn_requests.custom_cmd_success_requests,
            response_comparator=response_comparators.is_in_say,
            aggregation=any,
        ),
        Turn(
            request_type="error",
            request={
                "code": "software_error",
                "details": "коробка стоит на коробка",
                "command": {"name": "pick_up"},
            },
            response="Произошла ошибка при выполнении поставленной задачи.",
            response_comparator=response_comparators.is_in_say,
            aggregation=any,
        ),
        Turn(
            request_type="error",
            request={
                "code": "software_error",
                "details": "коробка стоит на коробка",
                "command": {"name": "pick_up"},
            },
            response="Произошла ошибка при выполнении поставленной задачи.",
            response_comparator=response_comparators.is_in_say,
            aggregation=any,
        ),
        Turn(
            request_type="error",
            request={
                "code": "software_error",
                "details": "коробка стоит на коробка",
                "command": {"name": "pick_up"},
            },
            response="Не удалось выполнить поставленную задачу. Возвращаюсь на изначальную позицию.",
            response_comparator=response_comparators.is_in_say,
            aggregation=any,
        ),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(
            request="О чем поговорим?",
            response=" ",
            response_comparator=response_comparators.is_in_say,
        ),
    ],
)


main_flow_fail_real_requests = TestCase(
    name="main_flow_fail_real_requests",
    turns=[
        Turn(request="Привет, Квант", response="Добрый день, какой у вас вопрос?"),
        Turn(
            request_type="error",
            request={
                "code": "software_error",
                "details": "Ошибка программы: software_error",
                "command": {"name": "say"},
            },
            response="",
            response_comparator=response_comparators.is_error,
        ),
        Turn(request="Хочу забрать заказ", response="Поднесите штрих-код к сканеру."),
        Turn(
            request_type="error",
            request={
                "code": "software_error",
                "details": "сканер не работает",
                "command": {"name": "scan_code"},
            },
            response="Произошла ошибка: сканер не работает",
            response_comparator=response_comparators.is_in_say,
            aggregation=any,
        ),
        Turn(request="Хочу забрать заказ", response="Поднесите штрих-код к сканеру."),
        Turn(
            request_type="success",
            request={
                "payload": "313",
                "command": {"name": "scan_code"},
            },
            response="Подождите несколько минут, я принесу ваш заказ.",
            success_requests=turn_requests.custom_cmd_success_requests,
            response_comparator=response_comparators.is_in_say,
            aggregation=any,
        ),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
    ],
)


direct_commands_flow_requests = TestCase(
    name="direct_commands_flow_requests",
    turns=[
        Turn(request="повернись налево", response="turn", response_comparator=response_comparators.is_command_not_in_plan),
        # Turn(request="режим команд", response="Режим управления прямыми командами запущен, ожидаю команды"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(
            request="включить режим прямых коман",
            response="Режим управления прямыми командами запущен, ожидаю команды",
            response_comparator=response_comparators.is_in_say,
        ),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="повернись налево", response="turn", response_comparator=response_comparators.is_command_in_plan),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(
            request="",
            response="Неизвестная прямая команда. Отвечает модуль поддержки диалога.",
            response_comparator=response_comparators.is_in_say,
        ),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="вперед 2 метра", response="go", response_comparator=response_comparators.is_command_in_plan),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="двигайся до точки 2", response="go_to", response_comparator=response_comparators.is_command_in_plan),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="возьми ящик 313", response="pick_up", response_comparator=response_comparators.is_command_in_plan),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="опусти ящик 313", response="drop", response_comparator=response_comparators.is_command_in_plan),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="какой статус", response="status", response_comparator=response_comparators.is_command_in_plan),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="садись", response="sit_down", response_comparator=response_comparators.is_command_in_plan),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="поднимайся", response="stand_up", response_comparator=response_comparators.is_command_in_plan),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="стоять", response="stop", response_comparator=response_comparators.is_command_in_plan),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(
            request="переместить в положение 4",
            response="go_to",
            response_comparator=response_comparators.is_command_in_plan,
        ),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(
            request=" Включить дворники, ",
            response="windshield_wipers",
            response_comparator=response_comparators.is_command_in_plan,
        ),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="Сложи зеркала", response="mirror_fold", response_comparator=response_comparators.is_command_in_plan),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(
            request="Заблокируй двери",
            response="lock_doors",
            response_comparator=response_comparators.is_command_in_plan,
        ),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(
            request="Установи температуру на...",
            response="set_temperature",
            response_comparator=response_comparators.is_command_in_plan,
        ),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="Включи кондиционер", response="ac_on", response_comparator=response_comparators.is_command_in_plan),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="Позвони Васе", response="call_contact", response_comparator=response_comparators.is_command_in_plan),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(
            request="Воспроизведи музыку",
            response="play_media",
            response_comparator=response_comparators.is_command_in_plan,
        ),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="Танцуй", response="dance", response_comparator=response_comparators.is_command_in_plan),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(
            request="Прыжок с поворотом",
            response="jump_turn",
            response_comparator=response_comparators.is_command_in_plan,
        ),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="Наклонись назад", response="tilt", response_comparator=response_comparators.is_command_in_plan),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="Следуй за мной", response="follow", response_comparator=response_comparators.is_command_in_plan),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="Найди стул", response="search_view", response_comparator=response_comparators.is_command_in_plan),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(
            request="Опиши объект перед тобой",
            response="describe_view",
            response_comparator=response_comparators.is_command_in_plan,
        ),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(
            request="Обнови последний объект",
            response="search_data_base",
            response_comparator=response_comparators.is_command_in_plan,
        ),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(
            request="Что перед тобой?",
            response="question_view",
            response_comparator=response_comparators.is_command_in_plan,
        ),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="Подойди ко мне", response="go_user", response_comparator=response_comparators.is_command_in_plan),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
    ],
)
chit_chat_flow_requests = TestCase(
    name="chit_chat_flow_requests",
    turns=[
        Turn(request="Привет, Квант", response="Добрый день, какой у вас вопрос?"),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(
            request="Поговорим о чём-нибудь",
            response=" ",
            response_comparator=response_comparators.is_in_say,
        ),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(
            request="Поговорим о чём-нибудь",
            response=" ",
            response_comparator=response_comparators.is_in_say,
        ),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(request="Расскажи про себя", response=" ", response_comparator=response_comparators.is_in_say),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
    ],
)
go_to_waypoint_flow_requests = TestCase(
    name="go_to_waypoint_flow_requests",
    turns=[
        Turn(
            request="Иди на зарядку",
            response="Направляюсь к, зарядному устройству",
            response_comparator=response_comparators.is_in_say,
        ),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(
            request="Отправляйся на ПВЗ",
            response="Направляюсь к, пункту выдачи заказов",
            response_comparator=response_comparators.is_in_say,
        ),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(
            request="Поиграем в футбол",
            response="Направляюсь к площадке для игры в футбол",
            response_comparator=response_comparators.is_in_say,
        ),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
        Turn(
            request="Вернись на ПВЗ",
            response="Направляюсь к, пункту выдачи заказов",
            response_comparator=response_comparators.is_in_say,
        ),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
    ],
)
develop_flow_requests = TestCase(
    name="develop_flow_requests",
    turns=[
        Turn(
            request="Сбросить состояние мира",
            response="Восстановлено состояние мира по умолчанию.",
            response_comparator=response_comparators.is_in_say,
        ),
        Turn(request_type="success", response="success", response_comparator=response_comparators.is_status),
    ],
)


test_cases = [
    order_flow_found,
    order_flow_not_found_no_questions,
    autopilot_flow_requests,
    direct_commands_flow_requests,
    chit_chat_flow_requests,
    go_to_waypoint_flow_requests,
    develop_flow_requests,
    main_flow_fail_real_requests,
    order_flow_real_requests,
    order_flow_failed_real_requests,
]


test_cases = {test_case.name: test_case for test_case in test_cases}

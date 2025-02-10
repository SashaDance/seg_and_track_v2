from enum import Enum
from typing import Optional, Literal, List, Tuple, Union
from pydantic.v1 import BaseModel  # , Field, field_validator, ValidationInfo


class RobotPosition(BaseModel):
    x: float  #  = Field(description="Координата X положения робота")
    y: float  #  = Field(description="Координата Y положения робота")
    theta: float  #  = Field(description="Ориентация робота (угол в радианах)")


class BoxState(BaseModel):
    box_id: int  #  = Field(description="Идентификатор коробки")
    placed_on_shelf_with_id: int  # = Field(
    #     description="Идентификатор полки, на которой находится коробка (-1, если в руках у робота)"
    # )


class ShelfState(BaseModel):
    shelf_id: int  #  = Field(description="Идентификатор полки")
    occupied_by_box_with_id: int  # = Field(
    #     description="Идентификатор коробки, находящейся на полке (-1, если полка пустая)"
    # )


class WorldState(BaseModel):
    robot_position: Tuple[float, float, float]  #  = Field(description="Положение робота в пространстве (x, y, theta)")
    boxes: List[BoxState]  #  = Field(description="Список состояний коробок на складе")
    shelves: List[ShelfState]  #  = Field(description="Список состояний полок на складе")

    # def toDict(self):
    #     return self.dict()


class Pose(BaseModel):
    position: Tuple[float, float, float]  #  = Field(description="Позиция объекта в пространстве (x, y, z)")
    orientation: Tuple[
        float, float, float, float
    ]  #  = Field(description="Ориентация объекта в пространстве (кватернион)")


class TrackingObject(BaseModel):
    class_id: int  #  = Field(description="Идентификатор класса объекта")
    confidence: float  #  = Field(description="Уверенность в классификации объекта")
    tracking_id: int  #  = Field(description="Идентификатор отслеживания объекта")
    box_size: Tuple[float, float, float]  #  = Field(description="Размер коробки")
    pose: Pose  #  = Field(description="Поза объекта, включающая позицию и ориентацию")


class SceneGraphNode(BaseModel):
    id_1: int  #  = Field(description="Идентификатор первого объекта")
    timestamp_1: float  #  = Field(description="Метка времени для первого объекта")
    class_name_1: str  #  = Field(description="Название класса первого объекта")
    id_2: int  #  = Field(description="Идентификатор второго объекта")
    timestamp_2: float  #  = Field(description="Метка времени для второго объекта")
    class_name_2: str  #  = Field(description="Название класса второго объекта")
    rel_id: int  #  = Field(description="Идентификатор отношения между объектами")
    rel_name: str  #  = Field(description="Название отношения между объектами")


class Image(BaseModel):
    url: str  #  = Field(description="URL изображения")


class Telemetry(BaseModel):
    images: Optional[List[Image]] = None  # Field(
    # default=None, description="Ссылка на картинку, если нужно обрабатывать картинку"
    # )
    world_state: Optional[WorldState] = None  # Field(
    # default=None, description="Состояние мира, включающее положение робота, коробок и полок"
    # )
    seg_track: Optional[List[TrackingObject]] = None  # Field(
    # default=None, description="Результаты работы модуля сегментации и трекинга"
    # )
    scene_graph: Optional[List[SceneGraphNode]] = None  # Field(
    # default=None, description="Граф сцены, описывающий отношения между объектами"
    # )

    # def toDict(self):
    #     return self.dict()


class CommandInfo(BaseModel):
    id: str  #  = Field(description="ID команды")
    name: str  #  = Field(description="Название команды")


class SuccessCommandResponse(BaseModel):
    command: CommandInfo  #  = Field(description="Выполненая комманда")
    payload: Optional[Union[str, Telemetry]]  #  = Field(default=None, description="Payload of executed command")


# TODO: rename to CommandResult
# TODO: rename to CommandInfo
# TODO: rename to DreamCommandResponse


class ErrorCommandResponse(BaseModel):
    command: CommandInfo  #  = Field(description="Информация о команде")
    code: str  #  = Field(description="Код ошибки")
    details: str  #  = Field(description="Сообщение об ошибке")


class RequestType(str, Enum):
    TEXT_REQUEST = "text_request"
    ERROR = "error"
    SUCCESS = "success"


class RequestPayload(BaseModel):
    type: RequestType  #  = Field(description="Тип данных")
    text_request: Optional[str]  #  = Field(default=None, description="Запрос пользователя")
    success: Optional[SuccessCommandResponse]  #  = Field(default=None, description="Данные о выполненной команде")
    error: Optional[ErrorCommandResponse]  #  = Field(default=None, description="Данные об ошибке")


class AssistantRequest(BaseModel):
    user_id: str  # = Field(
    payload: RequestPayload  # = Field(


class PlanCommand(BaseModel):
    name: str
    id: str
    args: dict = {}


class ResponsePayload(BaseModel):
    type: Literal["plan", "error", "success"]  # = Field(description="Тип ответа: plan или error")
    plan: Optional[list[PlanCommand]] = None  #  = Field(description="Список комманд")
    error: Optional[Literal["stop_bot"]] = None  # Field(default=None, description="Данные об ошибке")


class AssistantResponse(BaseModel):
    metadata: Optional[str] = None  # Field(default=None, description="Ответ от ассистента в сыром виде, для логов")
    payload: ResponsePayload  #  = Field(description="Ответ от ассистента либо план комманд, либо данные об ошибке")
    is_dialog: bool = False  #  =  Field(description="Флаг указывающий состояние диалога")

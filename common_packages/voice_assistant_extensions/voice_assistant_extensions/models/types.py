from typing import Union, List, Tuple, Optional

from pydantic import BaseModel, Field, model_validator

from .commands import (
    GoCommand,
    TurnCommand,
    SayCommand,
    GoToCommand,
    PickUpCommand,
    DropCommand,
    SitDownCommand,
    StandUpCommand,
    StopCommand,
    StatusCommand,
    EnableAutopilotCommand,
    DisableAutopilotCommand,
    SetPointCommand,
    ScanCodeCommand,
)

AnyCommand = Union[
    GoCommand,
    TurnCommand,
    SayCommand,
    GoToCommand,
    PickUpCommand,
    DropCommand,
    SitDownCommand,
    StandUpCommand,
    StopCommand,
    StatusCommand,
    EnableAutopilotCommand,
    DisableAutopilotCommand,
    SetPointCommand,
    ScanCodeCommand,
]

PlanType = List[AnyCommand]


class CommandPlan(BaseModel):
    plan: PlanType = Field(description="List of commands")


class RobotPosition(BaseModel):
    x: float = Field(description="Координата X положения робота")
    y: float = Field(description="Координата Y положения робота")
    theta: float = Field(description="Ориентация робота (угол в радианах)")


class BoxState(BaseModel):
    box_id: int = Field(description="Идентификатор коробки")
    placed_on_shelf_with_id: int = Field(
        description="Идентификатор полки, на которой находится коробка (-1, если в руках у робота)"
    )


class ShelfState(BaseModel):
    shelf_id: int = Field(description="Идентификатор полки")
    occupied_by_box_with_id: int = Field(
        description="Идентификатор коробки, находящейся на полке (-1, если полка пустая)"
    )


class WorldState(BaseModel):
    robot_position: Tuple[float, float, float] = Field(description="Положение робота в пространстве (x, y, theta)")
    boxes: List[BoxState] = Field(description="Список состояний коробок на складе")
    shelves: List[ShelfState] = Field(description="Список состояний полок на складе")


class Pose(BaseModel):
    position: Tuple[float, float, float] = Field(description="Позиция объекта в пространстве (x, y, z)")
    orientation: Tuple[float, float, float, float] = Field(description="Ориентация объекта в пространстве (кватернион)")


class TrackingObject(BaseModel):
    class_id: int = Field(description="Идентификатор класса объекта")
    confidence: float = Field(description="Уверенность в классификации объекта")
    tracking_id: int = Field(description="Идентификатор отслеживания объекта")
    box_size: Tuple[float, float, float] = Field(description="Размер коробки")
    pose: Pose = Field(description="Поза объекта, включающая позицию и ориентацию")


class SceneGraphNode(BaseModel):
    id_1: int = Field(description="Идентификатор первого объекта")
    timestamp_1: float = Field(description="Метка времени для первого объекта")
    class_name_1: str = Field(description="Название класса первого объекта")
    id_2: int = Field(description="Идентификатор второго объекта")
    timestamp_2: float = Field(description="Метка времени для второго объекта")
    class_name_2: str = Field(description="Название класса второго объекта")
    rel_id: int = Field(description="Идентификатор отношения между объектами")
    rel_name: str = Field(description="Название отношения между объектами")


class Image(BaseModel):
    url: str = Field(description="URL изображения")


class Telemetry(BaseModel):
    images: Optional[List[Image]] = Field(
        default=None, description="Ссылка на картинку, если нужно обрабатывать картинку"
    )
    world_state: Optional[WorldState] = Field(
        default=None, description="Состояние мира, включающее положение робота, коробок и полок"
    )
    seg_track: Optional[List[TrackingObject]] = Field(
        default=None, description="Результаты работы модуля сегментации и трекинга"
    )
    scene_graph: Optional[List[SceneGraphNode]] = Field(
        default=None, description="Граф сцены, описывающий отношения между объектами"
    )

    @model_validator(mode="before")
    @classmethod
    def validate_error_details(cls, values):
        if values.get("status") == "error":
            if not values.get("error_details"):
                raise ValueError('error_details must be provided when status is "error"')
        return values


class ErrorDetails(BaseModel):
    description: Optional[str] = Field(default=None, description="Error description")
    code: Optional[str] = Field(default=None, description="Error code")

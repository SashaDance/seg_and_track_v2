from typing import Literal

from pydantic import BaseModel, Field


class GoCommandArgs(BaseModel):
    distance: float = Field(description="Distance to travel")


class TurnCommandArgs(BaseModel):
    direction: Literal["right", "left"] = Field(description="Direction to turn")


class SayCommandArgs(BaseModel):
    text: str = Field(description="Text to be spoken")


class GoToCommandArgs(BaseModel):
    waypoint_id: int = Field(description="ID of the waypoint to go to")


class PickUpCommandArgs(BaseModel):
    box_id: int = Field(description="ID of the box to pick up")


class DropCommandArgs(BaseModel):
    shelf_id: int = Field(description="ID of the box to drop")


class SetPointCommandArgs(BaseModel):
    point: str = Field(description="Name of the point to set")

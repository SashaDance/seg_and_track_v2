from typing import Literal

from pydantic import BaseModel, Field

from ._base import CommandName
from .arguments import (
    GoCommandArgs,
    TurnCommandArgs,
    SayCommandArgs,
    GoToCommandArgs,
    PickUpCommandArgs,
    DropCommandArgs,
    SetPointCommandArgs,
)


class BaseCommand(BaseModel):
    id: str = Field(description="Уникальный id комманды в плане")


class GoCommand(BaseCommand):
    name: Literal[CommandName.GO] = Field(description="Command to move a certain distance")
    args: GoCommandArgs = Field(description="Arguments for GO command")


class TurnCommand(BaseCommand):
    name: Literal[CommandName.TURN] = Field(description="Command to turn")
    args: TurnCommandArgs = Field(description="Arguments for turn command")


class SayCommand(BaseCommand):
    name: Literal[CommandName.SAY] = Field(description="Command to say a text")
    args: SayCommandArgs = Field(description="Arguments for say command")


class GoToCommand(BaseCommand):
    name: Literal[CommandName.GO_TO] = Field(description="Command to go to a waypoint")
    args: GoToCommandArgs = Field(description="Arguments for go_to command")


class PickUpCommand(BaseCommand):
    name: Literal[CommandName.PICK_UP] = Field(description="Command to pick up a box")
    args: PickUpCommandArgs = Field(description="Arguments for pick_up command")


class DropCommand(BaseCommand):
    name: Literal[CommandName.DROP] = Field(description="Command to drop a box")
    args: DropCommandArgs = Field(description="Arguments for drop command")


class SitDownCommand(BaseCommand):
    name: Literal[CommandName.SIT_DOWN] = Field(description="Command to sit down")


class StandUpCommand(BaseCommand):
    name: Literal[CommandName.STAND_UP] = Field(description="Command to stand up")


class StopCommand(BaseCommand):
    name: Literal[CommandName.STOP] = Field(description="Command to stop")


class StatusCommand(BaseCommand):
    name: Literal[CommandName.STATUS] = Field(description="Command to report status")


class EnableAutopilotCommand(BaseCommand):
    name: Literal[CommandName.ENABLE_AUTOPILOT] = Field(description="Command to enable autopilot")


class DisableAutopilotCommand(BaseCommand):
    name: Literal[CommandName.DISABLE_AUTOPILOT] = Field(description="Command to disable autopilot")


class SetPointCommand(BaseCommand):
    name: Literal[CommandName.SET_POINT] = Field(description="Command to set a point")
    args: SetPointCommandArgs = Field(description="Arguments for set_point command")


class ScanCodeCommand(BaseCommand):
    name: Literal[CommandName.SCAN_CODE] = Field(description="Command to scan a code")

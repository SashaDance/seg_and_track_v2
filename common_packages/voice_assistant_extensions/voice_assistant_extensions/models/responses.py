from typing import Literal, Optional

from pydantic import BaseModel, Field, model_validator
from ._base import CommandName
from .types import ErrorDetails, Telemetry


class EndPlanResponse(BaseModel):
    status: Literal["end_plan"] = Field(description="Indicates if the plan was ended")


class CommandResponse(BaseModel):
    status: Literal["success", "error", "end_plan"] = Field(description="Indicates if the command was successful")
    payload: Optional[str] = Field(default=None, description="Payload of executed command")
    meta: Optional[str] = Field(default=None, description="Meta of the command execution")
    command: Optional[CommandName] = Field(default=None, description="The command that was executed")
    id: Optional[str] = Field(default=None, description="Command ID")
    error_details: Optional[ErrorDetails] = Field(default=None, description="Additional details or error message")

    @model_validator(mode="before")
    @classmethod
    def validate_command_and_id(cls, values):
        if values.get("status") != "end_plan":
            if not values.get("command") or not values.get("id"):
                raise ValueError("command and id must be provided")
        return values

    @model_validator(mode="before")
    @classmethod
    def validate_error_details(cls, values):
        if values.get("status") == "error":
            if not values.get("error_details"):
                raise ValueError('error_details must be provided when status is "error"')
        return values


class GetSegNTrackResponse(BaseModel):
    status: Literal["success", "error", "not_implemented"] = Field(description="Status")
    error_details: Optional[str] = Field(default=None, description="Сообщение об ошибке")
    telemetry: Optional[Telemetry] = Field(default=None, description="Данные телеметрии")

    @model_validator(mode="before")
    @classmethod
    def validate_error_details(cls, values):
        if values.get("status") == "error":
            if not values.get("error_details"):
                raise ValueError('error_details must be provided when status is "error"')
        if values.get("status") == "success":
            if not values.get("telemetry"):
                raise ValueError('telemetry must be provided when status is "success"')
        return values

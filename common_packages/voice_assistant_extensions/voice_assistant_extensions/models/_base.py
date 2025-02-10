from enum import Enum


class CommandName(str, Enum):
    GO = "go"
    TURN = "turn"
    SAY = "say"
    GO_TO = "go_to"
    PICK_UP = "pick_up"
    DROP = "drop"
    SIT_DOWN = "sit_down"
    STAND_UP = "stand_up"
    STOP = "stop"
    STATUS = "status"
    ENABLE_AUTOPILOT = "enable_autopilot"
    DISABLE_AUTOPILOT = "disable_autopilot"
    SET_POINT = "set_point"
    SCAN_CODE = "scan_code"

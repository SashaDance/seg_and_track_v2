import re

from chatsky.script import Message

from services_api import assistant

clr_regex = re.compile(r"[\W]+")
ё_regex = re.compile(r"ё")


def clean_text(text: str) -> str:
    # print(f" in_text = {text}")
    # print(f"out_text = " + clr_regex.sub("", text))
    return ё_regex.sub("е", clr_regex.sub("", text))


def matches_regex(msg: Message, regex: str) -> bool:
    pattern = re.compile(regex)

    match = pattern.search(msg.text)

    return bool(match)


def is_in_plan_with_ssml(checked_response: Message, target_response: Message) -> bool:
    plan = assistant.AssistantResponse.parse_raw(checked_response.text).payload.plan
    return plan and target_response in [cmd.args.get("text", "") for cmd in plan]


def is_text_equal(checked_response: Message, target_response: Message) -> bool:
    return clean_text(checked_response.text) == clean_text(target_response.text)


def is_in_plan(checked_response: Message, target_response: Message) -> bool:
    plan = assistant.AssistantResponse.parse_raw(checked_response.text).payload.plan
    return plan and clean_text(target_response) in [clean_text(cmd.args.get("text", "")) for cmd in plan]


def is_first_in_plan(checked_response: Message, target_response: Message) -> bool:
    plan = assistant.AssistantResponse.parse_raw(checked_response.text).payload.plan
    return plan and clean_text(target_response) in [clean_text(cmd.args.get("text", "")) for cmd in plan[:1]]


def is_in_say(checked_response: Message, target_response: Message) -> bool:
    plan = assistant.AssistantResponse.parse_raw(checked_response.text).payload.plan
    return plan and clean_text(target_response) in " ".join([clean_text(cmd.args.get("text", "")) for cmd in plan if cmd.name == "say"])


def is_not_in_say(checked_response: Message, target_response: Message) -> bool:
    return not is_in_say(checked_response, target_response)


def is_error(checked_response: Message, target_response: Message) -> bool:
    return bool(assistant.AssistantResponse.parse_raw(checked_response.text).payload.error)


def is_command_in_plan(checked_response: Message, target_response: str) -> bool:
    plan = assistant.AssistantResponse.parse_raw(checked_response.text).payload.plan
    return plan and bool([cmd.args.get("text", "") for cmd in plan if cmd.name == target_response])


def is_command_not_in_plan(checked_response: Message, target_response: str) -> bool:
    return not is_command_in_plan(checked_response, target_response)


def is_status(checked_response: Message, target_response: str) -> bool:
    return assistant.AssistantResponse.parse_raw(checked_response.text).payload.type == target_response

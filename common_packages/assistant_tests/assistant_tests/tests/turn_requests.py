import copy

from services_api import assistant


def default_text_requests(turn, responses, ctx_id):
    assert turn.request_type == "text_request"
    payload = {"type": turn.request_type}
    payload["text_request"] = turn.request
    request = {
        "user_id": ctx_id,
        "payload": payload,
    }
    return [request]


def default_success_requests(turn, responses, ctx_id, check_type=True):
    if check_type:
        assert turn.request_type == "success"
    plan = assistant.AssistantResponse.parse_raw(responses[-1].text).payload.plan
    result_requests = []
    for cmd in plan:
        command_info = {"name": cmd.name, "id": cmd.id}
        payload = {
            "type": "success",
            "success": {"command": command_info},
        }
        result_requests += [
            {
                "user_id": ctx_id,
                "payload": payload,
            }
        ]
    return result_requests


def custom_cmd_success_requests(turn, responses, ctx_id):
    assert turn.request_type == "success"
    custom_cmd = turn.request["command"]["name"]
    success_requests = default_success_requests(turn, responses, ctx_id)
    requests_with_custom_cmd = []
    for request in success_requests:
        command_info = request["payload"]["success"]["command"]
        if command_info["name"] == custom_cmd:
            custom_payload = copy.deepcopy(turn.request)
            custom_payload["command"]["id"] = command_info["id"]
            payload = {
                "type": "success",
                "success": custom_payload,
            }
            custom_request = {
                "user_id": ctx_id,
                "payload": payload,
            }
            requests_with_custom_cmd.append(custom_request)
            break
        else:
            requests_with_custom_cmd.append(request)
    return requests_with_custom_cmd


def default_error_requests(turn, responses, ctx_id):
    assert turn.request_type == "error"
    failed_cmd = turn.request["command"]["name"]
    success_requests = default_success_requests(turn, responses, ctx_id, check_type=False)
    requests_with_fail = []
    for request in success_requests:
        command_info = request["payload"]["success"]["command"]
        if command_info["name"] == failed_cmd:
            error_payload = copy.deepcopy(turn.request)
            error_payload["command"]["id"] = command_info["id"]
            payload = {
                "type": "error",
                "error": error_payload,
            }
            failed_request = {
                "user_id": ctx_id,
                "payload": payload,
            }
            requests_with_fail.append(failed_request)
            break
        else:
            requests_with_fail.append(request)
    return requests_with_fail

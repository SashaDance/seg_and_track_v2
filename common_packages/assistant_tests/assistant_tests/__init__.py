import requests
import uuid


from assistant_tests.tests.data import test_cases  # noqa: F401


def test_scenario(test_case, url):
    ctx_id = str(uuid.uuid4())
    test_case_responses = []
    test_case_requests = []
    for turn in test_case.turns:
        if turn.request_type == "text_request":
            turn_requests = turn.text_requests(turn, test_case_responses, ctx_id)
        elif turn.request_type == "success":
            turn_requests = turn.success_requests(turn, test_case_responses, ctx_id)
        elif turn.request_type == "error":
            turn_requests = turn.error_requests(turn, test_case_responses, ctx_id)
        else:
            raise ValueError(f"Unknown request type: {turn.request_type}")
        turn_responses = []
        print(f">********************<{turn.request=}")
        print(f">++++++++++++++++++++<{turn.response=}")
        for i, request in enumerate(turn_requests):
            test_case_requests.append(request)
            response = requests.post(url=url, json=request)
            turn_responses.append(response)
            assert response.ok
            print(f">--------------------<({i}) {response.json()=}")

        if turn.response_comparator is not None:
            assert turn.aggregation([turn.response_comparator(response, turn.response) for response in turn_responses])
        else:
            assert turn.aggregation(
                [test_case.response_comparator(response, turn.response) for response in turn_responses]
            )
        test_case_responses += turn_responses

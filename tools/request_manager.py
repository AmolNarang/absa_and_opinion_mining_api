import json
import warnings

import requests
from config import HOST, APP_MAIN_PORT, BASE_DATA_PATH
from tools.logging_util import setup_logger

operation_logger = setup_logger('operation', path=f"{BASE_DATA_PATH}/logs")


def external_request(url: str, data):
    try:
        result = requests.post(
            url,
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        ).text

        result = json.loads(result)
        return result
    except json.JSONDecodeError:
        warnings.warn(f"\033[93m Error in loading json \033[0m")
    except Exception as e:
        warnings.warn(f"\033[93m Error when requesting to external resource: {e} \033[0m")
        operation_logger.exception(f"{__name__}: error with external request url:{url}")
    return None


def request(port, method: str, data):
    try:
        result = requests.post(
            f"http://{HOST}:{port}/{method}",
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        ).text
        return json.loads(result), True
    except json.JSONDecodeError as e:
        e = str(e)
        warnings.warn(f"\033[93m Error in loading json \033[0m")
        return e, False
    except Exception as e:
        e = str(e)
        warnings.warn(f"\033[93m Error when requesting to external resource: {e} \033[0m")
        operation_logger.exception(f"{__name__}: error in request, {port}, {method}")
        return e, False




if __name__ == "__main__":
    # print(request(APP_MAIN_PORT, 'classify', {
    #     "id": "citibankdb@main",
    #     "text": [
    #         "atm is not working"
    #     ]
    # }))

    print(external_request("http://localhost:550/test", {
        "id": "citibankdb@main",
        "text": [
            "atm is not working"
        ]
    }))

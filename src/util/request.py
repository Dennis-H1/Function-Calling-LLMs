import os
import requests

from src.util.errors import ServerResponseError

HOST = os.environ.get("HOST") or "127.0.0.1"
PORT = os.environ.get("PORT") or 5000
REQUEST_TIMEOUT = 5


def server_request(function_name: str, arguments: dict):
    try:
        response = requests.get(
            f"http://{HOST}:{PORT}/function_call/{function_name}", arguments, timeout=REQUEST_TIMEOUT)

        if response.status_code == 200:
            return response.content.decode(encoding="utf-8")

        raise ServerResponseError

    except (requests.ConnectionError, ServerResponseError):
        raise ServerResponseError

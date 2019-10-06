import json
from urllib.error import HTTPError
from urllib.request import Request, urlopen

BASE_URL = "https://caissy.dev/shops"


class ApiError(Exception):
    pass


def perform_request(uri, method="GET", data=None):
    request = Request(f"{BASE_URL}/{uri}")
    request.method = method
    request.add_header("content-type", "application/json")

    if data:
        request.data = json.dumps(data).encode('utf-8')

    try:
        with urlopen(request) as response:
            data = response.read()
            headers = response.headers
            if headers['content-type'] == "application/json":
                return json.loads(data)
            else:
                return None
            
    except HTTPError as e:
        code = e.code
        headers = e.headers
        data = e.read()
        error = ApiError()
        error.code = code
        if headers['content-type'] == "application/json":
            error.content = json.loads(data)
        raise error

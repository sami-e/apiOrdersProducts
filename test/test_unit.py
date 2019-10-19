from urllib.request import urlopen


from flask import Request, json
from inf5190.services import  ApiError


class TestApiError(object):
    def test_perform_request(self):
        request = Request(f"https://caissy.dev/shops/products")
        request.method = "GET"
        with urlopen(request) as response:
            data = response.read()
            reponse_test = json.loads(data)
            assert reponse_test is not None
            assert b"1248" in reponse_test
            assert b"1232" in reponse_test
            assert b"1235" in reponse_test
            assert b"1245" in reponse_test
            assert b"1231" in reponse_test

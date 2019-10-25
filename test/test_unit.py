import json
from urllib.request import Request, urlopen
from flask import Request, json

from inf5190.services import perform_request


class TestApiError(object):
    def test_perform_request(self):
        reponse_data = perform_request("products")
        data = json.loads(reponse_data)
        assert data is not None
        assert b"1248" in data
        assert b"1232" in data
        assert b"1235" in data
        assert b"1245" in data
        assert b"1231" in data

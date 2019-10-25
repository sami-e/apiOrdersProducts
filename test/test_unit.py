import json
from flask import Request, json
from inf5190.services import perform_request


class TestApiError(object):
    def test_perform_request(self):
        reponse_data = perform_request("products")
        data_str = json.dumps(reponse_data)
        assert data_str is not None
        assert "1248" in data_str
        assert "1232" in data_str
        assert "1235" in data_str
        assert "1245" in data_str
        assert "1231" in data_str


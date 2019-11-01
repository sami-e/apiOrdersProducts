import json
from tests.test_data import order, order_false, shipping_info, credit_card
from inf5190.services import perform_request


class TestRoutes(object):
    
    def test_perform_request(self):
        response_data = perform_request("products")
        data_str = json.dumps(response_data)
        assert data_str is not None
        assert "id" in data_str
        assert "price" in data_str
        assert "weight" in data_str

    def test_index(self, app, client):
        with app.app_context():
            response = client.get("/")
            assert response.status_code == 200
            assert b"1245" in response.data

    def test_post_redirect_get_order(self, app, client):
        with app.app_context():
            response = client.post("/order", json=order_false)
            assert response.status_code == 422
            assert b"out-of-inventory" in response.data

            response = client.post("/order", json=order)
            assert response.status_code == 302
            assert response.location == "http://localhost/order/1"
            response = client.get("/order/1")
            assert response.status_code == 200
            assert b"order" in response.data
            assert b"total_price" in response.data
            assert b"1020" in response.data

    def test_put_order(self, app, client):
        with app.app_context():
            response = client.post("/order", json=order)
            assert response.status_code == 302
    
            response = client.put("/order/1", json=shipping_info)
            assert response.status_code == 200
            assert b"country" in response.data
    
            response = client.put("/order/1", json=credit_card)
            assert response.status_code == 200
            assert b"success" in response.data
            assert b"true" in response.data


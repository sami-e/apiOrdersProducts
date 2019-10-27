import pytest

order_post = {
    "product": {
        "id": 1245,
        "quantity": 2
    }
}
shipping_info = {
    "order": {
        "email": "caissy.jean-philippe@uqam.ca",
        "shipping_information": {
            "country": "Canada",
            "address": "201, rue Président-Kennedy",
            "postal_code": "H2X 3Y7",
            "city": "Montréal",
            "province": "QC"
        }
    }
}
credit_card = {
    "credit_card": {
        "name": "John Doe",
        "number": "4242 4242 4242 4242",
        "expiration_year": 2024,
        "cvv": "123",
        "expiration_month": 9
    }
}

class TestPoll(object):
    def test_create_Order(self, app, client):
        with app.app_context():
            response = client.get("/")
            assert response.status_code == 200
            assert b"1245" in response.data
            assert b"1248" in response.data
            assert b"1232" in response.data
            assert b"1235" in response.data
            assert b"1245" in response.data
            assert b"1231" in response.data

            response = client.post("/order", json=order_post)
            assert response.status_code == 302
            assert response.location == "http://localhost/order/1"

            response = client.get("/order/1")
            assert response.status_code == 200
            assert b"1245" in response.data
            response = client.put("/order/1", json=shipping_info)
            assert response.status_code == 200
            assert b"email" in response.data

            response = client.put("/order/1", json=credit_card)
            assert response.status_code == 200
            assert b"success" in response.data

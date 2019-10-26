order = {
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
credit_card_f = {
    "credit_card": {
        "name": "John Doe",
        "number": "4000 0000 0000 0002",
        "expiration_year": 2024,
        "cvv": "123",
        "expiration_month": 9
    }
}


class TestApp(object):

    def test_index(self, app, client):
        with app.app_context():
            response = client.get("/")
            assert response.status_code == 200
            assert b"1245" in response.data

    def test_index_false(self, app, client):
        with app.app_context():
            response = client.get("/")
            assert response.status_code == 200
            assert b"12455" not in response.data

    def test_post_redirect_get_order(self, app, client):
        with app.app_context():
            order_post = {
                "product": {
                    "id": 1245,
                    "quantity": 2
                }
            }
            response = client.post("/order", json=order_post, follow_redirects=True)
            assert response.status_code == 200
            assert b"order" in response.data
            assert b"total_price" in response.data
            assert b"1020" in response.data

    def test_post_redirect_get_order_false(self, app, client):
        with app.app_context():
            order_post = {
                "product": {
                    "id": 1245,
                    "quantity": ""
                }
            }
            response = client.post("/order", json=order_post, follow_redirects=True)
            assert response.status_code == 422
            assert b"missing-fields" in response.data

    def test_put_order(self, app, client):
        with app.app_context():
            response_order = client.post("/order", json=order, follow_redirects=True)
            response_shipping = client.put("/order/1", json=shipping_info, follow_redirects=True)
            response_credit = client.put("/order/1", json=credit_card, follow_redirects=True)
            assert response_order.status_code == 200
            assert response_shipping.status_code == 200
            assert response_credit.status_code == 200
            assert b"country" in response_credit.data
            assert b"expiration_year" in response_credit.data
            assert b"amount_charged" in response_credit.data
            assert b"true" in response_credit.data

    def test_put_order_false(self, app, client):
        with app.app_context():
            response_order = client.post("/order", json=order, follow_redirects=True)
            response_shipping = client.put("/order/1", json=shipping_info, follow_redirects=True)
            response_credit = client.put("/order/1", json=credit_card_f, follow_redirects=True)
            assert response_order.status_code == 200
            assert response_shipping.status_code == 200
            assert response_credit.status_code == 422
            assert b"card-declined" in response_credit.data

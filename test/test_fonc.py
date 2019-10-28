from inf5190.test.test_data import order_post, shipping_info, credit_card, credit_card_false


class TestRoutes(object):

    def test_index(self, app, client):
        with app.app_context():
            response = client.get("/")
            assert response.status_code == 200
            assert b"1245" in response.data

    def test_post_redirect_get_order(self, app, client):
        with app.app_context():
            response = client.post("/order", json=order_post, follow_redirects=True)
            assert response.status_code == 200
            assert b"order" in response.data
            assert b"total_price" in response.data
            assert b"1020" in response.data

    def test_post_redirect_get_order_false(self, app, client):
        with app.app_context():
            response = client.post("/order", json=order_post, follow_redirects=True)
            assert response.status_code == 422
            assert b"missing-fields" in response.data

    def test_put_order(self, app, client):
        with app.app_context():
            response_order = client.post("/order", json=order_post, follow_redirects=True)
            response_shipping = client.put("/order/1", json=shipping_info, follow_redirects=True)
            response_credit = client.put("/order/1", json=credit_card, follow_redirects=True)
            assert response_order.status_code == 200
            assert response_shipping.status_code == 200
            assert response_credit.status_code == 200
            assert b"country" in response_credit.data
            assert b"expiration_year" in response_credit.data
            assert b"amount_charged" in response_credit.data
            assert b"true" in response_credit.data
            response_credit = client.put("/order/1", json=credit_card_false, follow_redirects=True)
            assert response_credit.status_code == 422
            assert b"card-declined" in response_credit.data


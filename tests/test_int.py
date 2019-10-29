from tests.test_data import order, shipping_info, shipping_info_false, credit_card, credit_card_false


class TestApp(object):
    
    def test_whole_order(self, app, client):
        with app.app_context():
            response = client.post("/order", json=order, follow_redirects=True)
            assert response.status_code == 200

            response = client.put("/order/1", json=shipping_info_false, follow_redirects=True)
            assert response.status_code == 422
            assert b"missing-fields" in response.data

            response = client.put("/order/1", json=credit_card, follow_redirects=True)
            assert response.status_code == 422
            assert b"missing-fields" in response.data  # missing shipping information

            response = client.put("/order/1", json=shipping_info, follow_redirects=True)
            assert response.status_code == 200
            assert b"country" in response.data

            response = client.put("/order/1", json=credit_card_false, follow_redirects=True)
            assert response.status_code == 422
            assert b"card-declined" in response.data

            response = client.put("/order/1", json=credit_card, follow_redirects=True)
            assert response.status_code == 200
            assert b"expiration_year" in response.data
            assert b"amount_charged" in response.data

            response = client.put("/order/1", json=credit_card, follow_redirects=True)
            assert response.status_code == 422
            assert b"already-paid" in response.data

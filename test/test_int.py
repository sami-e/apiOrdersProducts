from inf5190.test.test_data import order_post, shipping_info, credit_card


class TestApp(object):
    
    def test_whole_order(self, app, client):
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
            assert b"country" in response.data

            response = client.put("/order/1", json=credit_card)
            assert response.status_code == 200
            assert b"success" in response.data
            assert b"true" in response.data

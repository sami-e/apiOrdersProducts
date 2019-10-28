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

credit_card_false = {
    "credit_card": {
        "name": "John Doe",
        "number": "4000 0000 0000 0002",
        "expiration_year": 2024,
        "cvv": "123",
        "expiration_month": 9
    }
}

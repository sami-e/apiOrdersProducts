# Flask API to order products


## Description

This is a Flask REST API build in educational settings : see [jpcaissy course on web app](https://github.com/jpcaissy/INF5190) (UQÀM-2019).  
The products are retrieved from a given API (https://caissy.dev/shops/products) and stored in a PostgreSQL DB. RQ (a simple Python library for queueing jobs) and Redis are also used for paying orders (https://caissy.dev/shops/pay) and caching completed orders.

## API documentation

Base URL: https://inf5190-tp.herokuapp.com/

- GET /  
Content-Type: application/json  
**Description**: Returns all the existing products you can order  
**Outputs**:  
```
{  
   "products" : [  
      {  
         "name" : "Hapiness Bottle",  
         "weight" : 450,  
         "id" : 123,  
         "in_stock" : true,  
         "description" : "An incredible bottle filled with happiness and joy. One of a kind!",  
         "price" : 5999,  
         "image": "http://caissy.dev/shops/images/image.png"  
      },  
      {  
         "description" : "A limited edition special Flying Squirrel. Hurry up, it won't last long!",  
         "image": "http://caissy.dev/shops/images/image.png",  
         "in_stock" : false,  
         "id" : 456,  
         "name" : "Flying Squirrel Limited Edition",  
         "weight" : 220,  
         "price" : 3149  
      }  
   ]  
}  
```  
- POST /order  
Content-Type: application/json  
**Description**: Makes a new order  
**Inputs**:  
```
{  
	"products": [  
        { "id": 1231, "quantity": 1 },  
        { "id": 1245, "quantity": 2 }  
    ]  
}  
```  
**Outputs**: Redirects to GET /order/<int:order_id> 
```
{  
    "order": {  
        "credit_card": {},  
        "email": null,  
        "id": 1,  
        "paid": false,  
        "products": [  
            {  
                "id": 1231,  
                "quantity": 1  
            },  
            {  
                "id": 1245,  
                "quantity": 2  
            }  
        ],  
        "shipping_information": {},  
        "shipping_price": 10,  
        "total_price": 7019,  
        "transaction": {}  
    }  
}  
```  

- GET /order/<int:order_id>   
Content-Type: application/json  
**Description**: Retrieves an existing order  
**Outputs**: See above POST /order  

- PUT /order/<int:order_id>  
Content-Type: application/json  
**Description**: Updates an order by adding email and shipping information  
**Inputs**:  
```
{  
   "order" : {  
      "email" : "caissy.jean-philippe@uqam.ca",  
      "shipping_information" : {  
         "country" : "Canada",  
         "address" : "201, rue Président-Kennedy",  
         "postal_code" : "H2X 3Y7",  
         "city" : "Montréal",  
         "province" : "QC"  
      }  
   }  
}  
```  
**Outputs**:  
```
{  
    "order": {  
        "credit_card": {},  
        "email": "caissy.jean-philippe@uqam.ca",  
        "id": 1,  
        "paid": false,  
        "products": [  
            {  
                "id": 1231,  
                "quantity": 1  
            },  
            {  
                "id": 1245,  
                "quantity": 2  
            }  
        ],  
        "shipping_information": {  
            "address": "201, rue Président-Kennedy",  
            "city": "Montréal",  
            "country": "Canada",  
            "postal_code": "H2X 3Y7",  
            "province": "QC"  
        },  
        "shipping_price": 10,  
        "total_price": 7019,  
        "transaction": {}  
    }  
}  
```  

- PUT /order/<int:order_id>  
Content-Type: application/json  
**Description**: Completes an order by paying it  
**Inputs**:  
```
{  
   "credit_card" : {  
      "name" : "John Doe",  
      "number" : "4242 4242 4242 4242",  
      "expiration_year" : 2024,  
      "cvv" : "123",  
      "expiration_month" : 9  
   }  
}  
```  
**Outputs**:  
```
{  
  "order": {  
    "credit_card": {  
      "expiration_month": 9,  
      "expiration_year": 2024,  
      "first_digits": "4242",  
      "last_digits": "4242",  
      "name": "John Doe"  
    },  
    "email": "caissy.jean-philippe@uqam.ca",  
    "id": 1,  
    "paid": true,  
    "products": [  
      {  
        "id": 1231,  
        "quantity": 1  
      },  
      {  
        "id": 1245,  
        "quantity": 2  
      }  
    ],  
    "shipping_information": {  
      "address": "201, rue Président-Kennedy",  
      "city": "Montréal",  
      "country": "Canada",  
      "postal_code": "H2X 3Y7",  
      "province": "QC"  
    },  
    "shipping_price": 10,  
    "total_price": 7019,  
    "transaction": {  
      "amount_charged": 7029,  
      "error": {},  
      "id": "WKyzrWLqiGU6fklV8w9RUzmGnIbKjUtB",  
      "success": true  
    }  
  }  
}  

```  

## Miscellaneous

- This API was done in educational settings so the only credit card accepted is  
```
"number" : "4242 4242 4242 4242",  
"expiration_year" : 2024,  
"cvv" : "123",  
"expiration_month" : 9  
```    
- The credit card number 4000 0000 0000 0002 generates a "card-declined" error  
- Orders are paid using RQ workers. To activate the worker and pay orders, you have to log in to the heroku project with an authorized account in a Terminal window: ```heroku login```  
- Then run: ```heroku run "FLASK_DEBUG=1 FLASK_APP=inf5190 flask worker"```  
- You can also run the project locally with *docker-compose* to fire the databases and *docker* to start the app (Dockerfile)

## WARNINGS

- This API depends on two externals API:  
https://caissy.dev/shops/products and https://caissy.dev/shops/pay  
- Tests was done with ```pytest``` and a SQLite DB, so they are not up-to-date (PostgreSQL)  

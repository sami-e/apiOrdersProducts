import json
from flask import Flask
from inf5190 import models
from inf5190 import views
from urllib.request import urlopen


def create_app(initial_config=None):
    app = Flask("inf5190")
    models.init_app(app)
    
    @app.route('/')
    def index():
        return views.index("Hello")
    
    return app

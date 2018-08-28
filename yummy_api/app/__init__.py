from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from configuration.config import DevelopingConfig
from flasgger import Swagger
from flask_login import LoginManager
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
swagger = Swagger(app,
                  template={
                    "info": {
                        "title": "Yummy Recipes API",
                        "description": "Ymmy recipes helps many individuals " +
                        "who love to cook and aet food keep track of " +
                        "those awesome food recipes. Yummy recipes allows" +
                        " them to remember recipes and share with others."
                    },
                    "securityDefinitions": {
                        "TokenHeader": {
                            "type": "apiKey",
                            "name": "Authorization",
                            "in": "header"
                        }
                    },
                    "Consumes": "Application/json"
                  })
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config.from_object(DevelopingConfig)
db = SQLAlchemy(app)

# set up login manager for the api
login_manager = LoginManager()
login_manager.init_app(app)

from app.views.users import UserView
from app.views.category import CategoryView
from app.views.recipes import RecipesView


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'Error': 'Page not found'}), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'Error': 'Method not allowed'}), 405

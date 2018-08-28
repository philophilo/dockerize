from app import app, db
from app.models.users import Users
from app.models.category import Category
from app.models.recipes import Recipes
from configuration.config import TestingConfig
import json
from werkzeug.security import generate_password_hash
from datetime import datetime
from flask_testing import TestCase


class BaseTestCase(TestCase):
    """Base class for tests"""
    test_user = "user"
    test_user_password = "Pass123!"
    test_user_name = "fname lname"
    test_user_email = "test.email@gmail.com"
    test_category_name = "Meat"
    test_category_description = "Strictly beef"
    test_recipe = "local beef"
    test_recipe2 = "italian beef"
    test_recipe_description = "Ugandan beef"
    test_recipe_ingredients = "onions, meat, tomatoes"

    # function required by flask-testing
    def create_app(self):
        return app

    # defined functions
    def create_user(self):
        """Helper function creates user for tests"""
        user = Users(username=self.test_user,
                     name=self.test_user_name,
                     email=self.test_user_email,
                     password=generate_password_hash(
                         self.test_user_password))
        user.add()

    def create_category(self):
        """Helper function creates category for tests"""

        category = Category(user_id=1,
                            cat_name=self.test_category_name,
                            description=
                            self.test_category_description)
        category.add()

    def create_recipe(self):
        """Helper function creates recipe for tests"""

        recipe = Recipes(name=self.test_recipe,
                                category=1,
                                description=self.test_recipe_description,
                                ingredients=self.test_recipe_ingredients)
        recipe2 = Recipes(name=self.test_recipe2,
                                category=1,
                                description=self.test_recipe_description,
                                ingredients=self.test_recipe_ingredients)
        recipe2.add()
        recipe.add()

    def helper_login(self):
        """Helper function authetication for tests"""
        response = self.client.post('/auth/login',
                                    content_type='application/json',
                                    data=json.dumps(
                                        dict(username=self.test_user,
                                             password=self.test_user_password)))
        return response

    def helper_login_with_token(self):
        """Helper function returns authentication header with token for tests"""
        reply = json.loads(self.helper_login().data.decode())
        bearer = 'Bearer {}'.format(reply['token'])
        headers = {'Authorization': bearer}
        return headers

    def setUp(self):
        """Helper function sets up working environment for tests"""
        app.config.from_object(TestingConfig)
        db.create_all()
        db.session.commit()

    def tearDown(self):
        """Helper function destroys working environment for tests"""
        db.session.remove()
        db.drop_all()

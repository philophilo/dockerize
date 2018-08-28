from tests.test_base import BaseTestCase
from app.serializer import *
import json


class TestSerialiszers(BaseTestCase):
    # testing serializer functions
    def test_user_can_register(self):
        """Test that a user can registered"""
        values = check_values({'name':12345})
        self.assertEquals(values, False)

    def test_invalid_token(self):
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MTYyMzk3OTMsImlhdCI6MTUxNjIzOTc4Nywic3ViIjo2fQ.bXyAE51jamki3wYhitsQhywJJaTdx23A_GKFlRJvms8"
        bearer = 'Bearer {}'.format(token)
        new_headers = {'Authorization': bearer}
        self.create_user()
        self.create_category()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.post('/category/1/recipes/',
                                        content_type='application/json',
                                        headers=new_headers,
                                        data=json.dumps(
                                            dict(recipe_name='ugandan meat',
                                                 description=self.test_recipe_description,
                                                 ingredients="beef, onions")))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['Error'], 'Invalid token')

    def test_no_token(self):
        self.create_user()
        self.create_category()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.post('/category/1/recipes/',
                                        content_type='application/json',
                                        data=json.dumps(
                                            dict(recipe_name='ugandan meat',
                                                 description=self.test_recipe_description,
                                                 ingredients="beef, onions")))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['Error'], 'Please provide a token')

    def test_invalid_token(self):
        token = 4
        bearer = 'Bearer {}'.format(token)
        new_headers = {'Authorization': bearer}
        self.create_user()
        self.create_category()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.post('/category/1/recipes/',
                                        content_type='application/json',
                                        headers=new_headers,
                                        data=json.dumps(
                                            dict(recipe_name='ugandan meat',
                                                 description=self.test_recipe_description,
                                                 ingredients="beef, onions")))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['Error'], 'Invalid token')

    def test_handle_exceptions(self):
        """Test exception handling"""
        try:
            c = {'a': 1}
            return c['b']
        except Exception as e:
            handle_exceptions(
                type(e).__name__, {'KeyError':{'Error':'key not found',
                                               'e':400}})
            reply = json.loads(format_error['error'][0].data.decode())
            self.assertEqual(reply['Error'], 'key not found')

    def test_handle_unfamiliar_exceptions(self):
        """Test exception handling"""
        try:
            c = {'a': 1}
            return c['b']
        except Exception as e:
            response = handle_exceptions(
                type(e).__name__, {'ValueError':'the value is invalid'})
            self.assertTrue(str(e))

    def test_check_fullname(self):
        """Test full names"""
        name =  "John Peter"
        response = check_fullname(name)
        self.assertEqual(response, True)

    def test_check_upper_limit_fullname(self):
        """Test full names"""
        name =  "John Peter"
        response = check_upper_limit_fullname(name)
        self.assertEqual(response, True)

    def test_check_lower_limit_fullname(self):
        """Test full names"""
        name =  "John Peter"
        response = check_lower_limit_fullname(name)
        self.assertEqual(response, True)

    def test_valid_username(self):
        """Test full names"""
        username =  "name_1"
        response = check_username(username)
        self.assertEqual(response, True)

    def test_username_upper_limit(self):
        """Test full names"""
        password =  "name_1"
        response = check_username_upper_limit(password)
        self.assertEqual(response, True)

    def test_username_lower_limit(self):
        """Test full names"""
        password =  "name_1"
        response = check_username_lower_limit(password)
        self.assertEqual(response, True)

    def test_password_upper_limit(self):
        """Test full names"""
        password =  "Password1!"
        response = check_password_upper_limit(password)
        self.assertEqual(response, True)

    def test_password_lower_limit(self):
        """Test full names"""
        password =  "Password1!"
        response = check_password_lower_limit(password)
        self.assertEqual(response, True)

    def test_item_name_is_alphabet(self):
        """Test full names"""
        name =  "Meat"
        response = check_item_name_alphabet(name)
        self.assertEqual(response, True)

    def test_item_name_upper_limit(self):
        """Test full names"""
        name =  "Meat"
        response = check_item_name_upper_limit(name)
        self.assertEqual(response, True)

    def test_item_name_lower_limit(self):
        """Test full names"""
        name =  "Meat"
        response = check_item_name_lower_limit(name)
        self.assertEqual(response, True)

    def test_validate_email(self):
        """Test full names"""
        email =  "hello@gmail.com"
        response = validate_email(email)
        self.assertEqual(response, True)

    def test_validate_description(self):
        """Test full names"""
        description =  "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
        print(len(description), '####')
        response = validate_descriptions(description)
        self.assertEqual(response, None)

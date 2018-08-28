from tests.test_base import BaseTestCase
import json


class TestUserRegistration(BaseTestCase):
    # testing user registration
    def test_user_can_register(self):
        """Test that a user can registered"""
        with self.client:
            response = self.client.post('/auth/register',
                                        content_type='application/json',
                                        data=json.dumps(
                                            dict(username="user",
                                                 name="fname lname",
                                                 email="test.user@gmail.com",
                                                 password="Pass1!")))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['username'], "user", msg="username key fail")

    def test_user_registers_with_weak_password(self):
        """Test that a user can registered"""
        with self.client:
            response = self.client.post('/auth/register',
                                        content_type='application/json',
                                        data=json.dumps(
                                            dict(username="user",
                                                 name="fname lname",
                                                 email="test.user@gmail.com",
                                                 password="Pass")))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['Error'], "Password must have atleast one Block letter, a number and a symbol")

    def test_user_with_long_password(self):
        """Test that a user can registered"""
        with self.client:
            response = self.client.post('/auth/register',
                                        content_type='application/json',
                                        data=json.dumps(
                                            dict(username="user",
                                                 name="fname lname",
                                                 email="test.user@gmail.com",
                                                 password="Passklnwjenidjnwieniunfinfinrinirinijn!0mdfkjkjdfhbrhbfhjbjhfbrhrbhbbhjjhrbhebbberbhjerjbn1")))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['Error'], "Password can have between 6 and 50 characters")

    def test_existing_user_account(self):
        """Test duplicating an existing user account"""
        self.create_user()
        with self.client:
            response = self.client.post('/auth/register',
                                        content_type='application/json',
                                        data=json.dumps(
                                            dict(
                                                username=self.test_user,
                                                email=self.test_user_email,
                                                name=self.test_user_name,
                                                password=self.test_user_password
                                                )))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['Error'], 'Username already exists')

    def test_wrong_user_login_credentials(self):
        """Test authentication with wring user credentials"""
        self.create_user()
        with self.client:
            response = self.client.post('/auth/login',
                                        content_type='application/json',
                                        data=json.dumps(
                                            dict(username='user1',
                                                 password='password')))
            reply = json.loads(response.data.decode())
            self.assertTrue(reply['Error'], 'Incorrect username or password')

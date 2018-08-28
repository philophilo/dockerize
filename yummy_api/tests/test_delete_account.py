from tests.test_base import BaseTestCase
import json


class TestDeleteAccount(BaseTestCase):
    # ---delete account tests
    def test_deleting_account_without_password_key(self):
        """Test deleting a user account without a password key"""
        self.create_user()
        self.create_category()
        self.create_recipe()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.delete('/auth/delete-account',
                                          content_type='application/json',
                                          headers=headers)
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['Error'], 'Password is missing')

    def test_deleting_account_with_empty_password_value(self):
        """Test deleting an account with emoty password value"""
        self.create_user()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.delete('/auth/delete-account',
                                          content_type='application/json',
                                          headers=headers,
                                          data=json.dumps(
                                              dict(password='')))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['Error'], 'password is empty')

    def test_deleting_account_with_wrong_password(self):
        """Test deleting an account with wrong password"""
        self.create_user()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.delete('/auth/delete-account',
                                          content_type='application/json',
                                          headers=headers,
                                          data=json.dumps(
                                            dict(password='p')))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['Error'], 'Incorrect password')

    def test_deleting_account_successfully(self):
        """Test deleting an account successfully"""
        self.create_user()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.delete('/auth/delete-account',
                                          content_type='application/json',
                                          headers=headers,
                                          data=json.dumps(
                                              dict(password=self.test_user_password
                                                   )))
            self.assertEqual(response.status_code, 200)

from tests.test_base import BaseTestCase
import json


class TestPasswordReset(BaseTestCase):
    # -----testing password reset
    def test_password_reset_without_password_key(self):
        self.create_user()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.put('/auth/reset-password',
                                       content_type='application/json',
                                       headers=headers,
                                       data=json.dumps(
                                           dict(new_password='pass123',
                                                confirm_password='pass123')))
            reply = json.loads(response.data.decode())
            print(reply)
            self.assertEqual(reply['Error'], 'password key missing')

    def test_password_reset_with_wrong_password(self):
        self.create_user()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.put('/auth/reset-password',
                                       content_type='application/json',
                                       headers=headers,
                                       data=json.dumps(
                                           dict(password='password',
                                                new_password='pass123',
                                                confirm_password='pass123')))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['Error'], 'Incorrect password')

    def test_password_reset_without_new_password_key(self):
        self.create_user()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.put('/auth/reset-password',
                                       content_type='application/json',
                                       headers=headers,
                                       data=json.dumps(
                                           dict(password='pass')))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['Error'], 'new_password key missing')

    def test_password_reset_without_confirming_new_password(self):
        self.create_user()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.put('/auth/reset-password',
                                       content_type='application/json',
                                       headers=headers,
                                       data=json.dumps(
                                           dict(password='pass',
                                                new_password='pass123')))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['Error'], 'confirm_password key missing')

    def test_password_reset_with_unmatching_passwords(self):
        self.create_user()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.put('/auth/reset-password',
                                       content_type='application/json',
                                       headers=headers,
                                       data=json.dumps(
                                           dict(password=self.test_user_password,
                                                new_password='pass12',
                                                confirm_password='pass123')))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['Error'], 'Passwords do not match')

    def test_password_reset_success(self):
        self.create_user()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.put('/auth/reset-password',
                                       content_type='application/json',
                                       headers=headers,
                                       data=json.dumps(
                                           dict(password=self.test_user_password,
                                                new_password='pass123',
                                                confirm_password='pass123')))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['message'], 'Password was reset')

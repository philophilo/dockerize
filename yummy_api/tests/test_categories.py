from tests.test_base import BaseTestCase
import json


class TestCategories(BaseTestCase):
    """ Testing categories """
    def test_create_category(self):
        """Test the creation of a category"""
        self.create_user()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.post('/category',
                                        content_type='application/json',
                                        headers=headers,
                                        data=json.dumps(
                                           dict(
                                               category_name='local beef',
                                               category_description=self.test_category_description
                                            )))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['category_name'], "local beef")
            self.assertEqual(reply['message'], 'category created')
            self.assertTrue(reply['id'], msg='no id')

    def test_view_categories(self):
        """
        Test the viewing of all categories at once with pagination
        """
        self.create_user()
        self.create_category()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.get('/category/',
                                       content_type='application/json',
                                       headers=headers)
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['count'], "1")
            self.assertEqual(reply['message'], 'categories found')
            self.assertEqual(reply['number_of_pages'], 1)
            self.assertEqual(reply['current_page'], 1)
            self.assertEqual(reply['next_page'], None)
            self.assertEqual(reply['previous_page'], None)
            self.assertTrue(reply['categories'], msg='no categories')

    def test_view_one_existing_category(self):
        self.create_user()
        self.create_category()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.get('/category/1',
                                       content_type='application/json',
                                       headers=headers)
            reply = json.loads(response.data.decode())
            print('>>>>>', reply)
            self.assertEqual(reply['message'], 'category found')
            self.assertEqual(reply['category_name'], 'Meat')

    def test_view_one_nonexisting_category(self):
        self.create_user()
        self.create_category()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.get('/category/2',
                                       content_type='application/json',
                                       headers=headers)
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['Error'], 'category not found')

    def test_updating_category(self):
        self.create_user()
        self.create_category()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.put('/category/1',
                                       content_type='application/json',
                                       headers=headers,
                                       data=json.dumps(
                                           dict(
                                               category_name='local beef',
                                               category_description=self.test_category_description
                                           )))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['message'], 'category updated')
            self.assertEqual(reply['category_name'], 'local beef')

    def test_updating_unknown_category(self):
        self.create_user()
        self.create_category()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.put('/category/2',
                                       content_type='application/json',
                                       headers=headers,
                                       data=json.dumps(
                                           dict(
                                               category_name='local beef',
                                               category_description=self.test_category_description
                                           )))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['Error'], 'category not found')

    def test_retrieving_more_pages(self):
        self.create_user()
        self.create_category()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.get('/category/?page=8',
                                       content_type='application/json',
                                       headers=headers)
            reply = json.loads(response.data.decode())
            print('----', reply)
            self.assertEqual(reply['message'], 'no categories found')


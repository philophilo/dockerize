from tests.test_base import BaseTestCase
import json


class TestSearch(BaseTestCase):
    # ----search tests
    def test_searching_categories(self):
        self.create_user()
        self.create_category()
        self.create_recipe()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.get('/category/search/?q=Meat',
                                       content_type='application/json',
                                       headers=headers)
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['message'], 'Categories found')

    def test_searching_recipes(self):
        self.create_user()
        self.create_category()
        self.create_recipe()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.get('/recipes/search/?q=local',
                                       content_type='application/json',
                                       headers=headers)
            reply = json.loads(response.data.decode())
            print('----', reply)
            self.assertEqual(reply['message'], 'Recipes found')

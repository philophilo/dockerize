from tests.test_base import BaseTestCase
import json


class TestRecipes(BaseTestCase):
    # -----recipe tests
    def test_create_recipe(self):
        """
        Test creating a new recipe
        """
        self.create_user()
        self.create_category()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.post('/category/1/recipes/',
                                        content_type='application/json',
                                        headers=headers,
                                        data=json.dumps(
                                            dict(recipe_name='ugandan meat',
                                                 description=self.test_recipe_description,
                                                 ingredients="beef, onions")))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['message'], 'Recipe created')

    def test_create_recipe_in_unknown_category(self):
        """
        Test creating a new recipe
        """
        self.create_user()
        self.create_category()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.post('/category/5/recipes/',
                                        content_type='application/json',
                                        headers=headers,
                                        data=json.dumps(
                                            dict(recipe_name='ugandan meat',
                                                 description=self.test_recipe_description,
                                                 ingredients="beef, onions")))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['Error'], 'category not found')

    def test_create_recipe_with_long_name(self):
        """
        Test creating a new recipe
        """
        self.create_user()
        self.create_category()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.post('/category/1/recipes/',
                                        content_type='application/json',
                                        headers=headers,
                                        data=json.dumps(
                                            dict(recipe_name='ugandanmeatugandanmeatugandanmeat ',
                                                 description=self.test_recipe_description,
                                                 ingredients="beef, onions")))
            reply = json.loads(response.data.decode())
            print(reply, '-----------')
            self.assertEqual(reply['Error'], 'The name should have between 4 and 20 characters')

    def test_view_recipe_in_category(self):
        """
        Test viewing recipes in a category with pagination
        """
        self.create_user()
        self.create_category()
        self.create_recipe()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.get('/category/1/recipes/',
                                       content_type='application/json',
                                       headers=headers)
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['count'], '1')
            self.assertEqual(reply['number_of_pages'], 1)
            self.assertEqual(reply['current_page'], 1)
            self.assertEqual(reply['next_page'], None)
            self.assertEqual(reply['previous_page'], None)
            self.assertTrue(reply['recipes'], msg='no recipes')

    def test_view_recipe_in_category(self):
        """
        Test viewing recipes in a category with pagination
        """
        self.create_user()
        self.create_category()
        self.create_recipe()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.get('/category/1/recipes/?page=5',
                                       content_type='application/json',
                                       headers=headers)
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['Error'], 'no recipes found')

    def test_create_duplicate_recipe(self):
        """
        Test creating a new recipe
        """
        self.create_user()
        self.create_category()
        self.create_recipe()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.post('/category/1/recipes/',
                                        content_type='application/json',
                                        headers=headers,
                                        data=json.dumps(
                                            dict(recipe_name=self.test_recipe,
                                                 description=self.test_recipe_description,
                                                 ingredients="beef, onions")))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['Error'], 'Recipe name already exists')

    def test_create_recipe_without_required_parameters(self):
        """
        Test creating a new recipe
        """
        self.create_user()
        self.create_category()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.post('/category/1/recipes/',
                                        content_type='application/json',
                                        headers=headers,
                                        )
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['Error'], 'Please parse category id, ' +
                             'recipe name and ingredients')


    def test_view_recipes_from_category(self):
        """
        Test viewing recipe in a category that doesnot exits
        """
        self.create_user()
        self.create_category()
        self.create_recipe()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.get('/category/1/recipes/',
                                       content_type='application/json',
                                       headers=headers)
            reply = json.loads(response.data.decode())
            print('****', reply)
            self.assertEqual(reply['message'], 'recipes found')

    def test_view_recipe_from_unknown_category(self):
        """
        Test viewing recipe in a category that doesnot exits
        """
        self.create_user()
        self.create_category()
        self.create_recipe()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.get('/category/2/recipes/',
                                       content_type='application/json',
                                       headers=headers)
            reply = json.loads(response.data.decode())
            print('****', reply)
            self.assertEqual(reply['Error'], 'category not found')

    def test_viewing_one_recipe(self):
        """
        Test viewing recipe in a category that doesnot exits
        """
        self.create_user()
        self.create_category()
        self.create_recipe()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.get('/category/1/recipes/1',
                                       content_type='application/json',
                                       headers=headers)
            reply = json.loads(response.data.decode())
            print('****', reply)
            self.assertEqual(reply['count'], 1)
            self.assertEqual(reply['message'], 'recipe found')

    def test_updating_known_recipe(self):
        """
        Test updating recipe with a known id (key)
        """
        self.create_user()
        self.create_category()
        self.create_recipe()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.put('/category/1/recipes/1',
                                       content_type='application/json',
                                       headers=headers,
                                       data=json.dumps(
                                           dict(recipe_name="Ugandan beef",
                                                recipe_category_id=1,
                                                description=self.test_recipe_description,
                                                ingredients="beef, onions")))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['message'], 'Recipe updated')

    def test_updating_unknown_recipe(self):
        """
        Test updating an unkown recipe
        """
        self.create_user()
        self.create_category()
        self.create_recipe()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.put('/category/1/recipes/3',
                                       content_type='application/json',
                                       headers=headers,
                                       data=json.dumps(
                                           dict(recipe_name="Ugandan beef",
                                                recipe_category_id=1,
                                                description=self.test_recipe_description,
                                                ingredients="beef, onions")))
            reply = json.loads(response.data.decode())
            print('----', reply)
            self.assertEqual(reply['Error'], 'Recipe not found')

    def test_updating_recipe_with_unknown_category(self):
        """
        Test updating an unkown recipe
        """
        self.create_user()
        self.create_category()
        self.create_recipe()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.put('/category/5/recipes/1',
                                       content_type='application/json',
                                       headers=headers,
                                       data=json.dumps(
                                           dict(recipe_name="Ugandan beef",
                                                recipe_category_id=5,
                                                description=self.test_recipe_description,
                                                ingredients="beef, onions")))
            reply = json.loads(response.data.decode())
            print('----', reply)
            self.assertEqual(reply['Error'], 'category not found')

    def test_updating_recipe_with_missing_keys(self):
        """
        Test updating an unkown recipe
        """
        self.create_user()
        self.create_category()
        self.create_recipe()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.put('/category/1/recipes/1',
                                       content_type='application/json',
                                       headers=headers,
                                       data=json.dumps(
                                           dict(recipe_name="Ugandan beef",
                                                recipe_category_id=1,
                                                ingredients="beef, onions")))
            reply = json.loads(response.data.decode())
            print('----', reply)
            self.assertEqual(reply['Error'], 'description key missing')


    def test_deleting_known_recipe(self):
        """
        Test deleting a known recipe
        """
        self.create_user()
        self.create_category()
        self.create_recipe()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.delete('/category/1/recipes/1',
                                          content_type='application/json',
                                          headers=headers
                                          )
            reply = json.loads(response.data.decode())
            print('-----', reply)
            self.assertEquals(reply['message'], 'recipe deleted')
            self.assertEquals(response.status_code, 200)

    def test_deleting_unknown_recipe(self):
        """
        Test deleting unknown recipe
        """
        self.create_user()
        self.create_category()
        self.create_recipe()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.delete('/category/1/recipes/3',
                                          content_type='application/json',
                                          headers=headers,
                                          data=json.dumps(
                                              dict(recipe_name="Ugandan beef"))
                                          )
            reply = json.loads(response.data.decode())
            print('----------->', reply)
            self.assertEqual(reply['Error'], 'Recipe not found')

    def test_deleting_recipe_from_unknown_category(self):
        """
        Test deleting recipe from unknown category
        """
        self.create_user()
        self.create_category()
        self.create_recipe()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.delete('/category/2/recipes/1',
                                          content_type='application/json',
                                          headers=headers,
                                          data=json.dumps(
                                              dict(recipe_name="Ugandan beef")))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['Error'], 'Category not found')

    def test_deleting_unknown_category(self):
        self.create_user()
        self.create_category()
        self.create_recipe()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.delete('/category/2',
                                          content_type='application/json',
                                          headers=headers,
                                          data=json.dumps(
                                              dict(category_name="Meat")))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['Error'], 'category not found')

    def test_deleting_known_category(self):
        self.create_user()
        self.create_category()
        self.create_recipe()
        with self.client:
            headers = self.helper_login_with_token()
            response = self.client.delete('/category/1',
                                          content_type='application/json',
                                          headers=headers,
                                          data=json.dumps(
                                              dict(category_name="Meat")))
            reply = json.loads(response.data.decode())
            self.assertEqual(reply['message'], 'category deleted')
            self.assertEqual(response.status_code, 200)

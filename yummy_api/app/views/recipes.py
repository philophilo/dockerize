from app import app
from flask import request, jsonify
from flasgger import swag_from
from app.models.recipes import Recipes
from app.models.users import Users
from flask_login import login_required
from app.serializer import (check_values, format_error,
                            validation,
                            handle_exceptions,
                            check_token_wrapper, create_error)
from app.category_serializer import check_category_id
from app.recipies_serializer import (do_create_recipe, do_recipe_update,
                                     definitions,
                                     do_recipes_search,
                                     get_recipes)


class RecipesView():
    """The class has the views for recipes"""

    @app.route('/category/<int:category_id>/recipes/', methods=['POST'])
    # @login_required
    @check_token_wrapper
    @swag_from('/app/docs/recipesaddrecipe.yml')
    def add_recipe(token, category_id):
        """The function adds recipes to the database"""
        try:
            user_id, data, error = Users.decode_token(token), request.json, \
                {'Error': 'category not found', 'e': 404}
            if check_category_id(user_id, category_id, error, True):
                return do_create_recipe(data, category_id)
            return format_error['error']
        except Exception as ex:
            excepts = {'ValueError': {'Error': 'Invalid entry, please provide' +
                                      ' the category id as integer while ' +
                                      'recipe name and ingredients as string',
                                      'e': 400},
                       'IntegrityError': {'Error': 'Recipe name already exists',
                                          'e': '409'},
                       'BadRequest': {'Error': 'Please parse category id, ' +
                                      'recipe name and ingredients', 'e': 400
                                      }}
            handle_exceptions(type(ex).__name__, excepts)
            return format_error['error']

    @app.route('/category/<int:category_id>/recipes/<int:recipe_id>',
               methods=['PUT'])
    # @login_required
    @check_token_wrapper
    @swag_from('/app/docs/recipesupdaterecipe.yml')
    def update_recipe(token, category_id, recipe_id):
        """The function updates a recipe"""
        try:
            user_id, data, error = Users.decode_token(token), request.json, \
                {'Error': 'category not found', 'e': 404}
            recipe_category_id = data.pop('recipe_category_id')
            if int(recipe_category_id) and validation(
                data, ['recipe_name', 'ingredients', 'description']) \
                    and check_category_id(user_id, category_id, error, True):
                return do_recipe_update(
                    [data, recipe_category_id], user_id, category_id, recipe_id)
            return format_error['error']
        except Exception as ex:
            excepts = {'KeyError': {'Error': str(ex).strip('\'') +
                                    ' key missing', 'e': 400},
                       'IntegrityError': {'Error': 'Recipe name already ' +
                                          'exists', 'e': 409},
                       'ValueError': {'Error': 'Invalid entry', 'e': 400},
                       'BadRequest': {'Error': 'Please parse category id, ' +
                                      'recipe name and ingredients', 'e': 400}}
            handle_exceptions(type(ex).__name__, excepts)
            return format_error['error']

    # TODO remove the category_id from the route
    @app.route('/category/<int:category_id>/recipes/<int:recipe_id>',
               methods=['DELETE'])
    # @login_required
    @check_token_wrapper
    @swag_from('/app/docs/recipesdeleterecipe.yml')
    def delete_recipe(token, category_id, recipe_id):
        """The function delete a recipe"""
        try:
            # get the user id from the token
            user_id, error = Users.decode_token(token), \
                {'Error': 'Category not found', 'e': 404}
            if check_category_id(user_id, category_id, error, True):
                user_recipe = Recipes.query.filter_by(
                    rec_cat=category_id, rec_id=recipe_id).first()
                if user_recipe is not None:
                    user_recipe.delete()
                    return jsonify({'message': 'recipe deleted'}), 200
                else:
                    create_error({'Error': 'Recipe not found'}, 404)
            return format_error['error']
        # capture value error
        except Exception as ex:
            excepts = {'ValueError': {'Error': 'Invalid entry, please ' +
                                      'provide the category id and recipe ' +
                                      'id as integers', 'e': 400},
                       'BadRequest': {'Error': 'Please parse the recipe id ' +
                                      'and category id', 'e': 400}}
            handle_exceptions(type(ex).__name__, excepts)
            return format_error['error']

    @app.route('/category/<int:category_id>/recipes/', methods=['GET'])
    @check_token_wrapper
    @swag_from('/app/docs/recipesviewcategoryrecipes.yml')
    def view_category_recipes(token, category_id):
        """The function return recipes in a category"""
        try:
            user_id, error = Users.decode_token(token), \
                {'Error': 'category not found', 'e': 404}
            if check_category_id(user_id, category_id, error, True):
                return get_recipes(user_id, category_id, True)
            return format_error['error']
        # capture value error
        except Exception as ex:
            excepts = {'ValueError': {'Error': 'Invalid entry, please ' +
                                      ' provide the category id as ' +
                                      'integer', 'e': 400},
                       'BadRequest': {'Error': 'Please parse the category ' +
                                      'id', 'e': 400}}
            handle_exceptions(type(ex).__name__, excepts)
            return format_error['error']

    @app.route('/category/<int:category_id>/recipes/<int:recipe_id>',
               methods=['GET'])
    @login_required
    @check_token_wrapper
    @swag_from('/app/docs/recipesviewonerecipe.yml')
    def view_one_recipe(token, category_id, recipe_id):
        """The function returns one recipe"""
        try:
            user_id, error = Users.decode_token(token), \
                {'Error': 'category not found', 'e': 404}
            if check_category_id(user_id, category_id, error, True):
                return get_recipes(user_id, category_id, False, recipe_id)
            return format_error['error']
        except Exception as ex:
            excepts = {'ValueError': {'Error': 'Invalid entry, please ' +
                                      'provide the category id and recipe ' +
                                      'id as integers', 'e': 400},
                       'BadRequest': {'Error': 'Please parse the recipe id ' +
                                      'and category id', 'e': 400}}
            handle_exceptions(type(ex).__name__, excepts)
            return format_error['error']

    @app.route('/recipes/search/', methods=['GET'])
    # @login_required
    @check_token_wrapper
    @swag_from('/app/docs/recipessearchrecipes.yml')
    def search_recipes(token):
        """The function searches and returns recipes in the database"""
        try:
            q = definitions()[2]
            user_id = Users.decode_token(token)
            check_response = check_values({'q': q})
            if check_response:
                return do_recipes_search(user_id)
            return format_error['error'], 400
        except Exception as ex:
            excepts = {'ValueError': {'Error': 'Invalid entry, please ' +
                                      'provide q as a string', 'e': 400},
                       'BadRequest': {'Error': 'Please provide the q ' +
                                      'parameter', 'e': 400}}
            handle_exceptions(type(ex).__name__, excepts)
            return format_error['error']

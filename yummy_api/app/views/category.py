from app import app
from flask import request, jsonify
from flasgger import swag_from
from app.models.category import Category
from app.models.users import Users
from flask_login import login_required
from sqlalchemy import and_
from app.serializer import (check_values, validation,
                            valid_data, validate_descriptions, format_error,
                            check_token_wrapper, handle_exceptions,
                            objects)
from app.category_serializer import (check_category_name, check_category_id)


def return_category(message):
    category = {'id': objects['category'].cat_id,
                'category_name': objects['category'].cat_name,
                'category_description': objects['category'].cat_description,
                'message': message}
    return category


def create_category_list(user_categories):
    results = []
    for category in user_categories.items:
        result = {'id': category.cat_id, 'category_name': category.cat_name,
                  'category_description': category.cat_description,
                  'category_date': category.cat_date
                  }
        results.append(result)
    return results


def get_paginated_categories(user_id, page, per_page):
    user_categories = Category.query.filter_by(
        user_id=user_id).paginate(page, per_page, False)
    if user_categories.items:
        current_page, number_of_pages, next_page, previous_page = \
            user_categories.page, user_categories.pages, \
            user_categories.next_num, user_categories.prev_num
        results = create_category_list(user_categories)
        return jsonify({'categories': results, 'count': str(len(results)),
                        'current_page': current_page,
                        'number_of_pages': number_of_pages,
                        'next_page': next_page, 'previous_page': previous_page,
                        'message': 'categories found'}), 200
    return jsonify({'message': 'no categories found'}), 404


def update_category(user_id, category_id, error):
    if check_category_id(user_id, category_id, error, True):
        objects['category'].cat_name = valid_data["category_name"]
        objects['category'].cat_description = valid_data[
            "category_description"]
        objects['category'].update()
        return jsonify(return_category('category updated')), 201
    return format_error['error']


def do_add_category(user_id):
    category = Category(
        user_id=int(user_id), cat_name=valid_data['category_name'],
        description=valid_data['category_description'],
    )
    category.add()
    return jsonify({
        'id': category.cat_id, 'category_name': category.cat_name,
        'category_description': category.cat_description,
        'category_date': category.cat_date,
        'message': 'category created'}), 201


def do_category_search(user_id, page, per_page, q):
    """The function returns a categories similar to the searched string"""
    user_categories = Category.query.filter(and_(
        Category.user_id == user_id,
        Category.cat_name.ilike('%'+q+'%'))).paginate(
            page, per_page, False)
    if user_categories.items:
        current_page = user_categories.page
        number_of_pages = user_categories.pages
        next_page = user_categories.next_num
        previous_page = user_categories.prev_num
        results = create_category_list(user_categories)
        return jsonify(
            {'categories': results, 'current_page': current_page,
             'number_of_pages': number_of_pages, 'next_page': next_page,
             'previous_page': previous_page, 'message': 'Categories found'}
        ), 200
    return jsonify({'message': 'no categories found'}), 404


class CategoryView():
    """The class has views for categories"""
    @app.route('/category', methods=['POST'])
    @check_token_wrapper
    @swag_from('/app/docs/categorycreatecategory.yml')
    def create_category(token):
        """The function creates a new category"""
        try:
            next = request.args.get('next')
            data, user_id, error = request.json, Users.decode_token(token), \
                {'Error': 'Category name already exists', 'e': 409}
            if validation(data, ['category_name', 'category_description']) and \
                    validate_descriptions(valid_data['category_description']) \
                    and check_category_name(user_id, error, False):
                return do_add_category(user_id)
            return format_error['error']
        except Exception as ex:
            excepts = {'IntegrityError': {'Error': 'Category name already ' +
                                          'exists', 'e': 409},
                       'BadRequest': {'Error': 'Please create a category ' +
                                      'name key and value', 'e': 400},
                       'ValueError': {'Error': "you sent an " + str(ex),
                                      'e': 400}}
            handle_exceptions(type(ex).__name__, excepts)
            return format_error['error']

    @app.route('/category/', methods=['GET'])
    @check_token_wrapper
    @swag_from('/app/docs/categoryviewallcategories.yml')
    def view_all_categories(token):
        """The function returns all categories"""
        try:
            user_id, page, per_page = Users.decode_token(token), \
                int(request.args.get('page', 1)), \
                int(request.args.get('per_page', 5))
            return get_paginated_categories(user_id, page, per_page)
        except Exception as ex:
            excepts = {'ValueError': {'Error': 'Invalid entry', 'e': 400},
                       'BadRequest': {'Error': 'Provide all fields', 'e': 400}}
            handle_exceptions(type(ex).__name__, excepts)
            return format_error['error']

    @app.route('/category/<int:category_id>', methods=['GET'])
    @login_required
    @check_token_wrapper
    @swag_from('/app/docs/categoryviewacategory.yml')
    def view_a_category(token, category_id):
        """The function returns one category"""
        try:
            user_id, error = Users.decode_token(token), \
                {'Error': 'category not found', 'e': 404}
            # get the category object with category
            if check_category_id(user_id, category_id, error, True):
                return jsonify(return_category('category found')), 200
            return format_error['error']
        except Exception as ex:
            return jsonify({'Error': str(ex)}), 400

    @app.route('/category/<int:category_id>', methods=['PUT'])
    # @login_required
    @check_token_wrapper
    def update_category(token, category_id):
        """The function updates a category"""
        try:
            data, user_id, error = request.json, Users.decode_token(token), \
                {'Error': 'category not found', 'e': 404}
            if validation(data, ['category_name', 'category_description']):
                return update_category(user_id, category_id, error)
            return format_error['error']
        except Exception as ex:
            excepts = {'IntegrityError': {'Error': 'Recipe name already ' +
                                          'exists', 'e': 409},
                       'ValueError': {'Error': 'Invalid entry', 'e': 400},
                       'BadRequest': {'Error': 'Please parse both category ' +
                                      'id and category name', 'e': 400},
                       'KeyError': {'Error': str(ex).strip('\'') + ' is ' +
                                    'missing', 'e': 400}}
            handle_exceptions(type(ex).__name__, excepts)
            return format_error['error']

    @app.route('/category/<int:category_id>', methods=['DELETE'])
    @check_token_wrapper
    @swag_from('/app/docs/categorydeletecategory.yml')
    def delete_category(token, category_id):
        """The function deletes a category"""
        try:
            # get user id from token
            user_id, error = Users.decode_token(token), \
                {'Error': 'category not found', 'e': 404}
            if check_category_id(user_id, category_id, error, True):
                objects['category'].delete()
                return jsonify({'message': 'category deleted'}), 200
            return format_error['error']
        except Exception as ex:
            excepts = {'ValueError': {'Error': 'Invalid entry for category id',
                                      'e': 400},
                       'BadRequest': {'Error': 'Please parse category id',
                                      'e': 400}}
            handle_exceptions(type(ex).__name__, excepts)
            return format_error['error']

    @app.route('/category/search/', methods=['GET'])
    @check_token_wrapper
    @swag_from('/app/docs/categorysearchcategories.yml')
    def search_categories(token):
        """The function searches and returns categories"""
        try:
            # TODO validate the search parameters
            q = str(request.args.get('q', '')).title()
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 5))
            user_id = Users.decode_token(token)
            # check if q is a string and not empty
            check_response = check_values({'q': q})
            if check_response:
                return do_category_search(user_id, page, per_page, q)
            return format_error['error']

        except Exception as ex:
            excepts = {'ValueError': {'Error': 'Invalid entry please provide ' +
                                      'q as a string', 'e': 400},
                       'BadRequest': {'Error': 'Please parse the q parameter',
                                      'e': 400}}
            handle_exceptions(type(ex).__name__, excepts)
            return format_error['error']

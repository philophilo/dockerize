from flask import request, jsonify
from app.models.category import Category
from app.models.recipes import Recipes
from app.serializer import (format_error,
                            valid_data, validate_descriptions, validation,
                            validate_item_names,
                            objects, create_error)


def definitions():
    page, per_page, q = int(request.args.get('page', 1)), \
        int(request.args.get('per_page', 5)), \
        str(request.args.get('q', '')).title()
    return page, per_page, q


def do_create_recipe(data, category_id):
    if validation(data, ['recipe_name', 'ingredients', 'description']) and \
            validate_item_names(valid_data['recipe_name']) and \
            validate_descriptions(valid_data['description']):
        recipe = Recipes(name=valid_data['recipe_name'], category=category_id,
                         ingredients=valid_data['ingredients'],
                         description=valid_data['description'])
        recipe.add()
        return jsonify(
            {'recipe_id': recipe.rec_id, 'recipe_name': recipe.rec_name,
             'category_name': objects['category'].cat_name,
             'ingredients': recipe.rec_ingredients.split(','),
             'message': 'Recipe created'}), 201
    return format_error['error']


def do_recipe_update(data_list, user_id, category_id, recipe_id):
    data, recipe_category_id = data_list
    user_recipe = Recipes.query.filter_by(
        rec_cat=category_id, rec_id=recipe_id).first()
    if user_recipe is not None:
        user_recipe.rec_name = valid_data['recipe_name']
        user_recipe.rec_cat = category_id
        user_recipe.rec_ingredients = valid_data['ingredients'],
        user_recipe.rec_description = valid_data['description']
        user_recipe.rec_cat = recipe_category_id
        user_recipe.update()
        return jsonify(
            {'recipe_id': user_recipe.rec_id,
                'recipe_name': user_recipe.rec_name,
                'category_name': objects['category'].cat_name,
                'category_id': user_recipe.rec_cat,
                'description': user_recipe.rec_description,
                'recipe_ingredients':
                user_recipe.rec_ingredients.split(','),
                'message': 'Recipe updated'}), 201
    create_error({'Error': 'Recipe not found'}, 404)
    return format_error['error']


def create_recipes_list(user_recipes):
    results = []
    for recipe in user_recipes:
        result = {
            'id': recipe.rec_id, 'recipe_name': recipe.rec_name,
            'description': recipe.rec_description, 'ingredients':
            recipe.rec_ingredients.split(","),
            'recipe_date': recipe.rec_date,
            'category_id': recipe.rec_cat
        }
        results.append(result)
    return results


def get_one_recipe(user_recipes):
    """The method returns one recipe from a parsed recipes object"""
    if user_recipes is not None:
        results = create_recipes_list(user_recipes)
        for recipe in results:
            recipe['category_name'] = objects['category'].cat_name
        if len(results):
            return jsonify({'recipes': results, 'message': 'recipe found',
                            'count': len(results)}), 200
        else:
            create_error({'error': 'no recipes found'}, 404)
    create_error({'Error': 'no recipes found'}, 404)
    return format_error['error']


def get_paginated_recipes(user_recipes):
    """The method returns paginated recipes from a parsed recipes object"""
    if user_recipes.items:
        current_page, number_of_pages, next_page, previous_page = \
            user_recipes.page, user_recipes.pages, user_recipes.next_num, \
            user_recipes.prev_num
        results = create_recipes_list(user_recipes.items)
        for recipe in results:
            recipe['category_name'] = objects['category'].cat_name
        return jsonify(
            {'recipes': results, 'count': str(len(results)),
             'current_page': current_page, 'number_of_pages': number_of_pages,
             'category_name': objects['category'].cat_name,
             'next_page': next_page,
             'previous_page': previous_page, 'message': 'recipes found'}), 200
    create_error({'Error': 'no recipes found'}, 404)
    return format_error['error']


def get_recipes(user_id, category_id, paginate, recipe_id=None):
    page, per_page, q = definitions()
    if paginate:
        user_recipes = Recipes.query.filter_by(
            rec_cat=category_id).paginate(page, per_page, False)
        return get_paginated_recipes(user_recipes)
    else:
        user_recipes = Recipes.query.filter_by(rec_cat=category_id,
                                               rec_id=recipe_id)
        return get_one_recipe(user_recipes)


def find_recipes(user_id):
    page, per_page, q = definitions()
    found_recipes = Category.query.join(
        Recipes, Category.cat_id == Recipes.rec_cat).add_columns(
            Category.cat_id, Category.user_id, Category.cat_name,
            Recipes.rec_id, Recipes.rec_name, Recipes.rec_description,
            Recipes.rec_ingredients, Recipes.rec_date).filter(
                Category.user_id == user_id).filter(
                    Recipes.rec_name.ilike('%'+q+'%')).paginate(
                        page, per_page, False)
    return found_recipes, page


def do_recipes_search(user_id):
    found_recipes = find_recipes(user_id)
    current_page, number_of_pages, next_page, previous_page, page = \
        found_recipes[0].page, found_recipes[0].pages, \
        found_recipes[0].next_num, found_recipes[0].prev_num, found_recipes[1]
    if page <= number_of_pages:
        results = []
        for recipe in found_recipes[0].items:
            result = {
                'category_id': recipe.cat_id, 'category_name': recipe.cat_name,
                'id': recipe.rec_id, 'recipe_name': recipe.rec_name,
                'description': recipe.rec_description,
                'ingredients': recipe.rec_ingredients.split(','),
                'recipe_date': recipe.rec_date
            }
            results.append(result)
        return jsonify(
            {'recipes': results, 'count': str(len(results)),
             'current_page': current_page, 'number_of_pages': number_of_pages,
             'next_page': next_page, 'previous_page': previous_page,
             'message': 'Recipes found'}), 200
    else:
        create_error({'Error': 'Page not found'}, 404)
    return format_error['error']

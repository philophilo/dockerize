from app.serializer import create_error, objects, valid_data, error
from app.models.category import Category


def check_category_name(user_id, e, state):
    check_category = Category.query.filter_by(
        user_id=int(user_id),
        cat_name=valid_data['category_name']
    ).first()
    if check_category is None and not state:
        return True
    elif check_category and state:
        objects['category'] = check_category
        return objects
    error['Error'] = e['Error']
    create_error(error, e['e'])


def check_category_id(user_id, category_id, e, state):
    user_category = Category.query.filter_by(
        cat_id=category_id, user_id=user_id).first()
    if user_category is None and not state:
        return True
    elif user_category and state:
        objects['category'] = user_category
        return objects
    error['Error'] = e['Error']
    create_error(error, e['e'])

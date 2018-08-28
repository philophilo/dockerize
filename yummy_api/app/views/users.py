from app import app, login_manager
from flask import request, jsonify, redirect
from flasgger import swag_from
from app.models.blacklist import Blacklist
from app.models.users import Users
from werkzeug.security import (generate_password_hash,
                               check_password_hash)
from flask_login import (login_user, login_required,
                         logout_user)
from datetime import datetime
from app.serializer import (check_data_keys, check_values, create_error,
                            valid_data, error, objects, check_token_wrapper,
                            handle_exceptions, validation,
                            valid_register, query_username, format_error
                            )


login_manager.login_view = '/'


# login_manager's user loader from the users' object
@login_manager.user_loader
def load_user(user_username):
    return Users.query.filter_by(user_username=user_username).first()


def password_reset_verification(user_id):
    user = Users.query.filter_by(id=user_id).first()
    if check_password_hash(user.user_password, valid_data['password']):
        if valid_data['new_password'] == valid_data['confirm_password']:
            objects['user'] = user
            return True
        else:
            create_error({'Error': 'Passwords do not match'}, 400)
    else:
        create_error({'Error': 'Incorrect password'}, 403)


@app.route("/")
def index():
    return redirect("apidocs")


class UserView():
    """The class views for user account"""
    @app.route('/auth/register', methods=['POST'])
    @swag_from('/app/docs/userregister.yml')
    def user_register():
        """The function registers a new user"""
        try:
            data, error = request.json, {'Error': 'Username already exists',
                                          'e': 409}
            if validation(data, ['username', 'name', 'password', 'email']) \
                    and valid_register() and query_username(error, False):
                user = Users(valid_data['username'],
                                generate_password_hash(valid_data['password']),
                                valid_data['name'], valid_data['email'])
                user.add()
                return jsonify({'username': user.user_username}), 201
            return format_error['error']
        except Exception as ex:
            excepts = {'KeyError': {'Error': str(ex).strip('\'')+' key is ' +
                                    'missing', 'e': 400}, 'IntegrityError':
                       {'Error': 'Email already exists', 'e': '409'},
                       'BadRequest': {'Error': 'All fields keys are required',
                                      'e': 400}, 'ValueError':
                       {'Error': str(ex), 'e': 400}}
            handle_exceptions(type(ex).__name__, excepts)
            return format_error['error']

    @app.route("/auth/login", methods=['POST'])
    @swag_from('/app/docs/userlogin.yml')
    def login():
        """The function logs in a new user"""
        try:
            print("====================================")
            data, q_error = request.json, {'Error': 'User not found', 'e': 403}
            if validation(data, ['username', 'password']) and \
                    query_username(q_error, True):
                if check_password_hash(
                        objects['user'].user_password,
                        valid_data['password']):
                    token = objects['user'].generate_auth_token()
                    login_user(objects['user'])
                    user = {"username": objects['user'].user_username,
                            "name": objects['user'].user_name,
                            "email": objects['user'].user_email}
                    print(user, "+++++++++++++++++++++++++++")
                    return jsonify({
                        'user':user, 'token': token.decode('ascii'),
                        'message': 'login was successful'}), 200
                else:
                    create_error({'Error': 'Incorrect password'}, 403)
            return format_error['error']
        except Exception as ex:
            excepts = {'BadRequest': {'Error': 'Please ensure all fieds are ' +
                                      'correctly specified', 'e': 400}}
            handle_exceptions(type(ex).__name__, excepts)
            return format_error['error']

    @app.route("/auth/get_user", methods=['GET'])
    @check_token_wrapper
    @swag_from('/app/docs/userlogin.yml')
    def get_user(token):
        """The function logs in a new user"""
        try:
            user_id = Users.decode_token(token)
            user = Users.query.filter_by(id=user_id).first()
            if (user):
                user = {"username": user.user_username,
                        "name": user.user_name,
                        "id": user_id,
                        "email": user.user_email}
                return jsonify({
                    "user": user, "message": "user records found"
                }), 200
            return jsonify({"Error": "User record not found"}), 401
        except Exception as ex:
            excepts = {'BadRequest': {'Error': 'Please ensure all fieds are ' +
                                      'correctly specified', 'e': 400}}
            handle_exceptions(type(ex).__name__, excepts)
            return format_error['error']

    @app.route('/auth/reset-password', methods=['PUT'])
    # @login_required
    @check_token_wrapper
    @swag_from('/app/docs/userresetpassword.yml')
    def reset_password(token):
        """The function updates a user's password"""
        try:
            data, user_id = request.json, Users.decode_token(token)
            if validation(data, ['password', 'new_password', 'confirm_password']
                          ) and password_reset_verification(user_id):
                objects['user'].user_password = generate_password_hash(
                    valid_data['new_password'])
                objects['user'].update()
                return jsonify({'message': 'Password was reset'}), 201
            return format_error['error']
        except Exception as ex:
            excepts = {'AttributeError':
                       {'Error': 'All attributes are expected', 'e': 400},
                       'BadRequest': {'Error': 'Parse all fields', 'e': 400}}
            handle_exceptions(type(ex).__name__, excepts)
            return format_error['error']

    @app.route('/auth/delete-account', methods=['DELETE'])
    @login_required
    @check_token_wrapper
    @swag_from('/app/docs/userdeleteaccount.yml')
    def delete_account(token):
        """The function deletes a user's account"""
        try:
            user_id, data = Users.decode_token(token), request.json
            if validation(data, ['password']):
                user = Users.query.filter_by(id=user_id).first()
                # check if the password provided matches the known
                if check_password_hash(user.user_password,
                                       valid_data['password']):
                    user.delete()
                    return jsonify({'Error': 'Account deleted'}), 200
                else:
                    create_error({'Error': 'Incorrect password'}, 403)
            return format_error['error']
        except Exception as ex:
            excepts = {'TypeError': {'Error': 'Please provide a password ' +
                                     'key and value', 'e': 400},
                       'BadRequest': {'Error': 'Password is missing', 'e': 400}}
            handle_exceptions(type(ex).__name__, excepts)
            return format_error['error']

    @app.route('/auth/logout', methods=['POST'])
    # @login_required
    @check_token_wrapper
    @swag_from('/app/docs/userlogout.yml')
    def logout(token):
        """The function ends a user's session and blacklists the token"""
        try:
            blacklist = Blacklist(token=token, date=datetime.now())
            blacklist.add()
            logout_user()
            return jsonify({'message': 'logout was successful'}), 200
        except Exception as ex:
            return jsonify(ex), 400

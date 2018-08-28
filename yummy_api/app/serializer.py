from flask import request
from app.models.users import Users
import re
from jwt import ExpiredSignatureError, InvalidTokenError
from flask import jsonify
from functools import wraps

error = {}
valid_data = {}
format_error = {}
objects = {}
cleaned_values = {}


def create_error(error, code):
    format_error['error'] = jsonify(error), code
    return True


def check_empty_spaces(string):
    """ Check if a string still has any empty spaces"""
    if not (isinstance(string, str)):
        return False, ' is not a string'
    string = string.strip()
    split_string = string.split(" ")
    number_of_splits = len(split_string)
    empty_chunks = 0
    for i in split_string:
        if len(i) == 0:
            empty_chunks += 1
    if empty_chunks == number_of_splits:
        return False, ' is empty'
    return True, string


def check_values(details):
    """check that the value is strictly a string"""
    for key, value in details.items():
        result = check_empty_spaces(value)
        if result[0]:
            valid_data[key] = result[1]
        else:
            error['Error'] = key+''+result[1]
            create_error(error, 400)
            return False
    return True


def check_token_wrapper(func):
    """check token validity"""
    @wraps(func)
    def auth(*args, **kwargs):
        token = None

        try:
            auth_header = request.headers.get('Authorization')
            token = auth_header.split(" ")[1]
            if Users.decode_token(token):
                return func(token, *args, **kwargs)
        except Exception as ex:
            excepts = {'ValueError': {'Error': 'Invalid token', 'e': 401},
                       'InvalidTokenError': {'Error': 'Invalid token',
                                             'e': 401},
                       'ExpiredSignatureError': {'Error': 'The token is ' +
                                                 'expired', 'e': 401},
                       'AttributeError': {'Error': 'Please provide a token',
                                          'e': 401}}
            handle_exceptions(type(ex).__name__, excepts)
            return format_error['error']
    return auth


def handle_exceptions(ex, expected):
    error, code = {}, 0
    if ex in expected:
        error['Error'], code = expected[ex]['Error'], expected[ex]['e']
    return create_error(error, code) if code else create_error(ex, 400)


def check_fullname(name):
    """ Check firstname and lastname seperated by space"""
    if re.match("([a-zA-Z]+) ([a-zA-Z]+)$", name):
        return True


def check_upper_limit_fullname(name):
    """ checks maximum length of name """
    if len(name) <= 50:
        return True


def check_lower_limit_fullname(name):
    """ checks minimum length of name """
    if len(name) >= 4:
        return True


def check_username(username):
    """check valid username"""
    if re.match("^[a-zA-Z0-9_-]+$", username):
        return True


def check_username_upper_limit(username):
    """check the upper limit of the username"""
    if len(username) <= 20:
        return True


def check_username_lower_limit(username):
    """check the lower limit of the username"""
    if len(username) >= 4:
        return True


def check_password(password):
    """check that the password has numbers, symbols and minimum"""
    pattern = re.compile(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!#%*?&])[A-Za-z\d$@$!%*?&]')
    result = pattern.match(password)
    print("****", result, password)
    if result:
        return True


def check_password_upper_limit(password):
    """check the upper limit of password"""
    if len(password) <= 50:
        return True


def check_password_lower_limit(password):
    """check the lower mimit of the password"""
    if len(password) >= 6:
        return True


def check_item_name_alphabet(name):
    """check whether name is alphabetical"""
    if re.match("^[a-zA-Z ]+$", name):
        return True


def check_item_name_upper_limit(name):
    """check the upper limit of a name"""
    if len(name) <= 20:
        return True


def check_item_name_lower_limit(name):
    """ check the lower limit of a name"""
    if len(name) >= 4:
        return True


def validate_username(username):
    """ Validate username constraints """
    if check_username(username):
        if check_username_upper_limit(username) and \
                check_username_lower_limit(username):
            return True
        error['Error'] = 'Username can have between 4 and 20 characters'
        return False
    error['Error'] = 'username can have ' \
        'alphabets, numbers and selected symbols(\'_ and -\')'
    create_error(error, 400)
    return False


def validate_name(fullname):
    """Validate full name constraints"""
    if check_fullname(fullname):
        if check_upper_limit_fullname(fullname) and \
                check_lower_limit_fullname(fullname):
            return True
        error['Error'] = 'Firstname and Lastname cannot be less than 4'
        return False
    error['Error'] = 'Your firstname and lastname must ' \
        'be alphabetical and seperated by a space'
    create_error(error, 400)
    return False


def validate_email(email):
    """Validate user email addresses"""
    if re.match(r'[a-zA-Z0-9.-]+@[a-z]+\.[a-z]+', email):
        return True
    error['Error'] = 'Invalid email address'
    create_error(error, 400)


def validate_descriptions(description):
    """Validate item description"""
    if len(description) <= 200:
        return True
    error['Error'] = 'Description is too long'
    create_error(error, 400)


def validate_password(password):
    """Validate password constraints"""
    if check_password(password):
        print('---')
        if check_password_upper_limit(password) and \
                check_password_lower_limit(password):
            return True
        error['Error'] = 'Password can have between 6 and 50 characters'
        create_error(error, 400)
        return False
    error['Error'] = 'Password must have atleast one Block letter, ' \
        'a number and a symbol'
    create_error(error, 400)
    return False


def validate_item_names(name):
    """Validate item names"""
    if isinstance(name, str) and check_item_name_alphabet(name):
        if check_item_name_upper_limit(name) and \
                check_item_name_lower_limit(name):
            return True
        else:
            error['Error'] = 'The name should have between 4 and 20 characters'
            create_error(error, 400)
    else:
        error['Error'] = 'The name must be from alphabetical letters'
        create_error(error, 400)


def check_data_keys(data, expected_keys):
    """Check if expected are present in received data"""
    for key in expected_keys:
        if key not in data:
            error['Error'] = key+' key missing'
            create_error(error, 400)
            return False
    return True


def validation(data, expected):
    """Checks for expected data values"""
    data_keys = check_data_keys(data, expected)
    new_data = {}
    for exp in expected:
        if exp in data:
            new_data[exp] = data[exp]
    if data_keys and check_values(new_data):
        return True


def valid_register():
    print("=====", valid_data['password'])
    if validate_username(valid_data['username']) and validate_name(
        valid_data['name']) and validate_password(valid_data[
            'password']) and validate_email(valid_data['email']):
        return True


def query_username(e, state):
    check_user = Users.query.filter_by(
        user_username=valid_data['username']).first()
    if check_user is None and not state:
        return True
    elif check_user and state:
        objects['user'] = check_user
        return objects
    error['Error'] = e['Error']
    create_error(error, e['e'])

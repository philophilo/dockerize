[![Build Status](https://travis-ci.org/philophilo/yummy_api.svg?branch=develop)](https://travis-ci.org/philophilo/yummy_api) [![Coverage Status](https://coveralls.io/repos/github/philophilo/yummy_api/badge.svg?branch=develop)](https://coveralls.io/github/philophilo/yummy_api?branch=develop) [![Maintainability](https://api.codeclimate.com/v1/badges/5e39cd477a45d4144b68/maintainability)](https://codeclimate.com/github/philophilo/yummy_api/maintainability)


Yummy Recipes is an application that allow users to keep track of their owesome food recipes. It helps individuals who love to cook and eat good food to remember recipes and also share with others.

# Features
* A user creates an account, logs in, logs out, updates password and deletes his/her account
* A user creates, views, updates and deletes his/her recipes categories
* A user creates, views, updates and deletes his/her recipes of existing categories

# Pre-requisites
* Python 3.6.X
* Python 2.7.3
* Flask
* Postman
* Flasgger
* Postgres

# Installations

* Create a new folder  ``mkdir webapp``
* ``cd webapp/``
* Install virtualenv ``$pip install virtualenv``
* Create a virtual environment ``virtualenv -p python3 venv``
* Clone the repo ``https://github.com/philophilo/yummy_api.git``
* Activate your virtual environment `source venv/bin/activate`
* Install project requirements ``pip install -r requirements.txt``
* Setup the postgres database ``yummy`` and test database ``test_yummy``
* Update the configuration files
* Create database and tables ``python manage.py db init`` ``python manage.py db migrate`` ``python manage.py db upgrade``
* Run the application ``python run.py``

# Running tests
You can test the application using two libraries nose2 or nosetests: ``nose2 --with-coverage` or `nosetests --with-coverage --cover-package=apps``


# Running tests
You can test the application using two libraries nose2 or nosetests: ``nose2 --with-coverage` or `nosetests --with-coverage --cover-package=apps``

# API on Heroku
[yummy-foods.herokuapp.com](https://yummy-foods.herokuapp.com/apidocs/)

# API Endpoints
### Users
|              URL Endpoints            | HTTP Requests |                      Access                    | Public Access|
|---------------------------------------|---------------|------------------------------------------------|--------------|
|POST /auth/register                    |     POST      | Registers a new user                           |  TRUE        |
|POST /auth/login                       |     POST      | Authenticates a registered user                |  TRUE        |
|POST /auth/logout                      |     POST      | Registers a new user                           |  FALSE       |
|PUT /auth/reset-password               |     PUT       | Resets a registered users's password           |  FALSE       |
|DELETE /auth/delete-account            |   DELETE      | Deletes a registered user's account            |  FALSE       |

### Categories
|              URL Endpoints            | HTTP Requests |                      Access                    | Public Access|
|---------------------------------------|---------------|------------------------------------------------|--------------|
|POST /category                         |     POST      | Creates a new categroy                         |  FALSE       |
|PUT /category/\<category_id>           |     PUT       | Edits a category with specified id             |  FALSE       |
|GET /category                          |     GET       | Retrieves a paginated list of  categories      |  FALSE       |
|GET /category/\<category_id>           |     GET       | Retrieves a specified category                 |  FALSE       |
|GET /category/search/\<id>             |     GET       | Retrieves a category with specified id         |  FALSE       |
|DELETE /category/\<id>                 |     DELETE    | Deletes a category with specified id           |  FALSE       |

### Recipes
|                    URL Endpoints                    | HTTP Requests |                        Access                        | Public Access|
|-----------------------------------------------------|---------------|------------------------------------------------------|--------------|
|POST /category/<category_id>/recipes/                |     POST      | Creates a new recipe                                 |  FALSE       |
|PUT /category/<category_id>/recipes/\<recipe_id>     |     PUT       | Edits a recipe with specified id                     |  FALSE       |
|GET /category/<category_id>/recipes/                 |     GET       | Retrieves a paginated lists of recipes               |  FALSE       |
|GET /recipes/search/                                 |     GET       | Retrieves a list of recipes through GET vairables    |  FALSE       |
|GET /category/\<category_id>/recipes/\<recipe_id>    |     GET       | Retrieves a list of recipes in a category            |  FALSE       |
|DELETE /category/\<category_id>/recipes/\<recipe_id> |     DELETE    | Deletes a recipe in category with specified id       |  FALSE       |

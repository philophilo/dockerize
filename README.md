# Containerization

[![Build Status](https://travis-ci.org/philophilo/yummy_api.svg?branch=develop)](https://travis-ci.org/philophilo/yummy_api) [![Coverage Status](https://coveralls.io/repos/github/philophilo/yummy_api/badge.svg?branch=develop)](https://coveralls.io/github/philophilo/yummy_api?branch=develop) [![Maintainability](https://api.codeclimate.com/v1/badges/5e39cd477a45d4144b68/maintainability)](https://codeclimate.com/github/philophilo/yummy_api/maintainability)
[![CircleCI](https://circleci.com/gh/philophilo/dockerize.svg?style=svg)](https://circleci.com/gh/philophilo/dockerize)

##

### Containerizing yummy recipes
Docker is currently leading as a containerization tool. Kubernetes container orchestrator by default deploys docker containers. 

##### Creating a docker image

Building a docker images required configuration to tell docker what kind of images should be created. The configurations are stored in a file named Dockerfile.

Creating a docker image `docker build -t yummy .` The command will by default build an image based on the Dockerfile in that directory. The `-t` command then tags the image created with names `yummy`

Tagging an image `docker tag yummy philophilo/yummy` The command tags an image on the machine named yummy with `philophilo/yummy` where `[dockerhub repository]/[image name]`.

Push the image to docker hub `docker push philophilo/yummy`

##### Running the application in docker locally

`docker run -it -d -p 127.0.0.1:80:80 --name yummy_container yummy` docker will create a container named `yummy_container` from the image `yummy.` This will be created in a dettached mode because of flag `-d`. For interactive processes (like a shell), you must use `-i -t` together in order to allocate a tty for the container process. `-i -t` can also be written as `-it`.

The application can then be accessed on `http://127.0.0.1/apidocs/` 

##### Continuous Integration and continuous deployment pipeline

The CICD pipeline for containerized application is done on cicleci.

###### Creating a circleci image
Circleci uses docker files to have fast testing without queueing. The image is created and also pushed to a docker hub repository. The images id configured to run `python3.6` `kops` `docker` and `kubectl`. These are then used by circleci to complete the CI/CD pipeline.

###### Running CI/CD pipeline on circle
The pipeline [configuration](https://github.com/philophilo/dockerize/blob/master/.circleci/config.yml) is stored in `.circleci/config`. Circleci picks up the changes when pushed and rebuilds the application. The tests are run, the images is rebuilt after passing tests. It is the pushed to the repository with the new changes. The pipeline continues to deploy to a kubernetes a cluster in the `AWS S3 bucker`

##### Deployment configuration
The deployment [configuration](https://github.com/philophilo/dockerize/blob/master/deployment.yml) pulls the docker container from the repository with 1 replica and opens port 80. A service is also created which in turn creates a loa balancer that also open port 80.

##### Creating a kubernetes cluster on AWS
For deployment to occur, the cluster must be existing. The kubernetes cluster is created from an AWS instance and [configured](https://github.com/philophilo/jenkins-image/blob/56d161257777082b490d1ba275a9b7956f5323a4/kube.sh#L5-L101). 

## Deployed kubernetes application
[yummy.philophilo.xyz](http://yummy.philophilo.xyz/)

# Yummy Recipes
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

#!/bin/bash
# start nginx service
service nginx start
# activate environment
. ../venv/bin/activate
# use gunorn to run the app
gunicorn run:app

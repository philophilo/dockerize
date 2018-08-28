#!/bin/bash
service nginx start
. ../venv/bin/activate
gunicorn run:app

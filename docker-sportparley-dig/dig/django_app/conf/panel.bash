#!/bin/bash

HOST=0.0.0.0
PORT=8000
exec python manage.py runserver_plus $HOST:$PORT

#!/bin/bash

DJANGO_WSGI_MODULE=ws_sportparley.wsgi
DJANGO_NAME=WSWebAPI

exec gunicorn -c /etc/app/conf/gunicorn.conf ${DJANGO_WSGI_MODULE}:application \
    --bind unix:/usr/src/${DJANGO_NAME}/WSWebAPI_dig_ws_1.sock
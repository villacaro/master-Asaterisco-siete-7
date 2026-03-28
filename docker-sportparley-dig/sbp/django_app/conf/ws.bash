#!/bin/bash

DJANGO_WSGI_MODULE=ws_sportparley.wsgi
DJANGO_NAME=WSWebAPI
SCALE_NAME=`echo $REDIS_NAME| cut -d'/' -f 2`

exec gunicorn -c /etc/app/conf/gunicorn.conf ${DJANGO_WSGI_MODULE}:application \
    --bind unix:/usr/src/${DJANGO_NAME}/${DJANGO_NAME}_${SCALE_NAME}.sock
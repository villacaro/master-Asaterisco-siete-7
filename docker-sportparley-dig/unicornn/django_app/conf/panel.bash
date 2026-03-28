#!/bin/bash

DJANGO_NAME=sbp
DJANGO_WSGI_MODULE=admin_banklotsports.wsgi
SCALE_NAME=`echo $REDIS_NAME| cut -d'/' -f 2`

exec gunicorn -c /etc/app/conf/gunicorn.conf ${DJANGO_WSGI_MODULE}:application \
    --bind unix:/usr/src/${DJANGO_NAME}/${DJANGO_NAME}_${SCALE_NAME}.sock
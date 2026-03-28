#!/bin/bash

SCALE_WORKER=`echo $REDIS_NAME| cut -d'/' -f 2`
exec python manage.py celery worker --hostname=${SCALE_WORKER//_} --loglevel=DEBUG
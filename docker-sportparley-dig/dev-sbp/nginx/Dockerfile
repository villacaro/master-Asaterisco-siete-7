FROM nginx

MAINTAINER ebar0n <edwar.baron@gmail.com>

COPY nginx.conf /etc/nginx/nginx.conf
RUN rm /etc/nginx/conf.d/default.conf

COPY ssl /etc/nginx/ssl/

COPY sites-enabled /etc/nginx/conf.d/
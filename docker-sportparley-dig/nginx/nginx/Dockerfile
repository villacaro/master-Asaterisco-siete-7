FROM nginx

MAINTAINER ebar0n <edwar.baron@gmail.com>

COPY nginx.conf /etc/nginx/nginx.conf
RUN rm /etc/nginx/conf.d/default.conf
COPY ssl /etc/nginx/ssl/

COPY sites-enabled/mp_panel.conf /etc/nginx/conf.d/mp_panel.conf
COPY sites-enabled/mp_ws.conf /etc/nginx/conf.d/mp_ws.conf
COPY sites-enabled/sbp_panel.conf /etc/nginx/conf.d/sbp_panel.conf
COPY sites-enabled/sbp_ws.conf /etc/nginx/conf.d/sbp_ws.conf
COPY sites-enabled/sbp_webapp.conf /etc/nginx/conf.d/sbp_webapp.conf
COPY sites-enabled/web_viwmed.conf /etc/nginx/conf.d/web_viwmed.conf
COPY sites-enabled/sportsbetparlay.conf /etc/nginx/conf.d/sportsbetparlay.conf
COPY sites-enabled/wp_mipuntopago.conf /etc/nginx/conf.d/wp_mipuntopago.conf
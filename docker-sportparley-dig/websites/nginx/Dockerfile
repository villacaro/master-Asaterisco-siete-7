FROM nginx
ADD nginx.conf /etc/nginx/nginx.conf
RUN rm /etc/nginx/conf.d/default.conf
ADD sites-enabled/viwmed.conf /etc/nginx/conf.d/viwmed.conf
ADD sites-enabled/wp_sbp.conf /etc/nginx/conf.d/wp_sbp.conf
ADD sites-enabled/wp_mipuntopago.conf /etc/nginx/conf.d/wp_mipuntopago.conf
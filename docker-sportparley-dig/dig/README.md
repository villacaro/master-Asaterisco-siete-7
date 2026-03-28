# Deploy

        docker-compose up -d postgres
        docker-compose run --rm panel python manage.py migrate admin_datamart --database=admin_datamart_db
        docker-compose run --rm panel python manage.py migrate admin_historic --database=admin_historic_db
        docker-compose run --rm panel python manage.py migrate
        docker-compose run --rm ws python manage.py migrate ws_client --database=webservice_db

        docker-compose run --rm panel python manage.py createmaster
        docker-compose run --rm panel python manage.py collectstatic

        docker-compose run --rm panel bash
                /usr/src/sbp# export PANEL_ADD_MENU=True && python manage.py runscript reload_menu && exit

#!/bin/bash
if [ "$TRAVIS_PULL_REQUEST" == "false" ]; then
if [ "$TRAVIS_BRANCH" == "asterisco7-server" ]; then
	echo "This will deploy!"
	echo ""
	sshpass -e ssh -o StrictHostKeyChecking=no -C -ocompressionLevel=9 -oPort=7458 lvillalobos@50.97.55.155 \
	'cd docker &&
	source access &&
	cd admin_asterisco7 &&
	git pull https://$GITUSER:$GITPASSWD@github.com/ebar0n/admin_asterisco7.git asterisco7-server &&
	cd .. &&
	cd ws_unicornn &&
	git pull https://$GITUSER:$GITPASSWD@github.com/lzambrano18/ws_unicornn.git asterisco7-server &&
	docker exec -i galileo_panel_1 python manage.py migrate --noinput &&
	docker exec -i galileo_panel_1 python manage.py collectstatic --noinput &&
	
	docker restart galileo_panel_1 &&
	docker restart galileo_panel_2 &&
	
	docker restart galileo_ws_1 &&
	docker restart galileo_ws_2 &&
	docker restart galileo_ws_3 &&
	docker restart galileo_ws_4 &&

	docker restart galileo_crontab_1 &&
	docker restart galileo_worker_1 &&
	docker restart galileo_worker_2 &&
	docker restart galileo_worker_3 &&
	docker restart galileo_worker_4 &&
	docker restart galileo_worker_5 &&
	docker restart galileo_worker_6 &&
	docker restart galileo_worker_7 &&
	docker restart galileo_worker_8 &&

	docker restart galileo_flower_1 &&
	
	docker ps &&
	exit'
	echo ""
	echo ":)"
else
	echo "This will not deploy!"
	echo ""
	echo ":("
fi
else
	echo "PR not deploy!"
fi
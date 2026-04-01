#!/bin/bash
if [ "$TRAVIS_PULL_REQUEST" == "false" ]; then
if [ "$TRAVIS_BRANCH" == "galileo-server" ]; then
	echo "This will deploy!";
	sshpass -e ssh -o StrictHostKeyChecking=no -C -ocompressionLevel=9 -oPort=7458 lvillalobos@50.97.55.155 \
	'cd docker &&
	source access &&
	cd admin_asterisco7 &&
	git pull https://$GITUSER:$GITPASSWD@github.com/ebar0n/admin_asterisco7.git galileo-server &&
	cd .. &&
	docker exec -i galileo_panel_1 python manage.py migrate --noinput &&
	docker restart galileo_panel_1 &&
	docker restart galileo_panel_2 &&
	docker ps &&
	exit';
	echo ":)";
else
	echo "Push not deploy!"
fi
else
	echo "PR not deploy!"
fi
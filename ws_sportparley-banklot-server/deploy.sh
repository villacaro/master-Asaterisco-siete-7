#!/bin/bash
if [ "$TRAVIS_PULL_REQUEST" == "false" ]; then
if [ "$TRAVIS_BRANCH" == "banklot-server" ]; then
	echo "This will deploy!";
	sshpass -e ssh -o StrictHostKeyChecking=no -C -ocompressionLevel=9 -oPort=7458 lvillalobos@50.97.55.155 \
	'cd docker &&
	source access &&
	cd ws_sportparley &&
	git pull https://$GITUSER:$GITPASSWD@github.com/lzambrano18/ws_sportparley.git banklot-server &&
	cd .. &&
	docker restart galileo_ws_1 &&
	docker restart galileo_ws_2 &&
	docker restart galileo_ws_3 &&
	docker restart galileo_ws_4 &&
	docker ps &&
	exit';
	echo ":)";
else
	echo "Push not deploy!"
fi
else
	echo "PR not deploy!"
fi
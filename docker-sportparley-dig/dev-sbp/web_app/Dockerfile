FROM python:3.5-slim
MAINTAINER ebar0n <edwar.baron@gmail.com>

RUN apt-get update

RUN apt-get install -y \
	wget gdebi-core
RUN wget --quiet http://download.gna.org/wkhtmltopdf/0.12/0.12.2.1/wkhtmltox-0.12.2.1_linux-jessie-amd64.deb \
	&& gdebi --quiet --non-interactive wkhtmltox-0.12.2.1_linux-jessie-amd64.deb

RUN apt-get install -y \
	postgresql-client libpq-dev \
	gcc supervisor \
	--no-install-recommends
RUN apt-get purge -y wget gdebi-core \
	&& apt-get -y autoremove \
	&& rm wkhtmltox-0.12.2.1_linux-jessie-amd64.deb \
	&& rm -rf /var/lib/apt/lists/*

COPY conf /etc/app/conf/
COPY requerimientos.txt requerimientos.txt

RUN pip install -r requerimientos.txt
RUN pip install Django
RUN pip install djangorestframework
RUN pip install https://github.com/ebar0n/django-mongoengine/archive/master.zip
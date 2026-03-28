# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ws_client.lib
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClientFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140, verbose_name='Nombre del archivo')),
                ('location', models.CharField(max_length=140, verbose_name='Ubicación')),
                ('version', models.CharField(blank=True, null=True, max_length=140, verbose_name='Versión')),
                ('size', models.IntegerField(verbose_name='Tamaño', help_text='En bytes, ejemplo: 1000')),
                ('file_type', models.CharField(max_length=140, choices=[('client', 'Cliente'), ('updater', 'Actualizador'), ('lib', 'Librería')], verbose_name='Tipo')),
                ('os', models.CharField(max_length=140, choices=[('ALL', 'All'), ('WIN32', 'Windows'), ('LINUX', 'Linux'), ('MACOS', 'Mac OS')], verbose_name='Sistema operativo')),
                ('crc', models.CharField(default='0', max_length=140, verbose_name='Hash CRC')),
                ('download_url', models.CharField(max_length=140, verbose_name='Link de descarga')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 1, 23, 20, 26, 27, 810584, tzinfo=utc), auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2015, 1, 23, 20, 26, 27, 810609, tzinfo=utc), auto_now=True)),
            ],
            options={
                'db_tablespace': 'ts_comer',
            },
            bases=(models.Model, ws_client.lib.BasicClass),
        ),
        migrations.CreateModel(
            name='ClientIPAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(max_length=140, verbose_name='Dirección IP')),
                ('ip_type', models.IntegerField(verbose_name='Tipo de IP', choices=[(1, 'Connection'), (2, 'Auto Update'), (3, 'Auth'), (4, 'Get Data')])),
                ('protocol', models.IntegerField(verbose_name='Protocolo', choices=[(1, 'HTTP'), (2, 'HTTPS')])),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 1, 23, 20, 26, 27, 808998, tzinfo=utc), auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2015, 1, 23, 20, 26, 27, 809035, tzinfo=utc), auto_now=True)),
            ],
            options={
                'db_tablespace': 'ts_comer',
            },
            bases=(models.Model, ws_client.lib.BasicClass),
        ),
        migrations.CreateModel(
            name='ClientStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=140, verbose_name='Estado')),
                ('codename', models.CharField(unique=True, max_length=140, verbose_name='Codename', default='client_status_')),
                ('content_type', models.IntegerField(verbose_name='Tipo de status', choices=[(1, 'IP'), (2, 'Versiones'), (3, 'Archivos')])),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 1, 23, 20, 26, 27, 805040, tzinfo=utc), auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2015, 1, 23, 20, 26, 27, 805081, tzinfo=utc), auto_now=True)),
            ],
            options={
                'db_tablespace': 'ts_comer',
            },
            bases=(models.Model, ws_client.lib.BasicClass),
        ),
        migrations.CreateModel(
            name='ClientVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(unique=True, max_length=140, verbose_name='Versión')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 1, 23, 20, 26, 27, 809718, tzinfo=utc), auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2015, 1, 23, 20, 26, 27, 809748, tzinfo=utc), auto_now=True)),
                ('status', models.ForeignKey(to='ws_client.ClientStatus')),
            ],
            options={
                'db_tablespace': 'ts_comer',
            },
            bases=(models.Model, ws_client.lib.BasicClass),
        ),
        migrations.AlterUniqueTogether(
            name='clientversion',
            unique_together=set([('version', 'status')]),
        ),
        migrations.AddField(
            model_name='clientipaddress',
            name='status',
            field=models.ForeignKey(to='ws_client.ClientStatus'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='clientipaddress',
            unique_together=set([('ip_address', 'ip_type'), ('ip_type', 'status')]),
        ),
        migrations.AddField(
            model_name='clientfiles',
            name='client_version',
            field=models.ForeignKey(to='ws_client.ClientVersion', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clientfiles',
            name='status',
            field=models.ForeignKey(to='ws_client.ClientStatus'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='clientfiles',
            unique_together=set([('name', 'version')]),
        ),
    ]

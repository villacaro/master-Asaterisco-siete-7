# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '__first__'),
        ('admin_users', '0012_auto_20141216_1925'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentTypes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(null=True, max_length=160, blank=True)),
                ('codename', models.CharField(max_length=160, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 12, 16, 19, 25, 49, 578336))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 16, 19, 25, 49, 578399), auto_now=True)),
            ],
            options={
                'db_tablespace': 'ts_comer',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sessions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('startdate', models.DateField(default=datetime.datetime(2014, 12, 16, 19, 25, 49, 580742))),
                ('enddate', models.DateField(null=True, blank=True)),
                ('ip', models.IPAddressField()),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 12, 16, 19, 25, 49, 580953))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 16, 19, 25, 49, 580997), auto_now=True)),
                ('user', models.ForeignKey(to='admin_users.Users')),
            ],
            options={
                'db_tablespace': 'ts_comer',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SessionsDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('ref', models.IntegerField(null=True, blank=True)),
                ('model', models.CharField(null=True, max_length=160, blank=True)),
                ('json', jsonfield.fields.JSONField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 12, 16, 19, 25, 49, 582345))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 16, 19, 25, 49, 582404), auto_now=True)),
                ('session', models.ForeignKey(to='admin_historic.Sessions')),
            ],
            options={
                'db_tablespace': 'ts_comer',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SessionsDetailDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('who', models.CharField(null=True, max_length=160, blank=True)),
                ('ref', models.IntegerField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 12, 16, 19, 25, 49, 586988))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 16, 19, 25, 49, 587046), auto_now=True)),
                ('sessiondetail', models.ForeignKey(to='admin_historic.SessionsDetail')),
            ],
            options={
                'db_tablespace': 'ts_comer',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaquillaSessions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('startdate', models.DateField()),
                ('enddate', models.DateField(null=True, blank=True)),
                ('ip', models.IPAddressField()),
                ('key', models.CharField(max_length=200)),
                ('package', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 12, 16, 19, 25, 49, 584157))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 16, 19, 25, 49, 584221), auto_now=True)),
                ('user', models.ForeignKey(to='admin_comercializacion.UsuariosTaquilla')),
            ],
            options={
                'db_tablespace': 'ts_comer',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaquillaSessionsDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('detail', jsonfield.fields.JSONField(null=True, blank=True)),
                ('enrro', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 12, 16, 19, 25, 49, 585578))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 16, 19, 25, 49, 585638), auto_now=True)),
                ('session', models.ForeignKey(to='admin_historic.TaquillaSessions')),
            ],
            options={
                'db_tablespace': 'ts_comer',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsersProcesses',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=140)),
                ('codename', models.CharField(max_length=140, unique=True)),
                ('content_type', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 12, 16, 19, 25, 49, 579553))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 16, 19, 25, 49, 579610), auto_now=True)),
                ('process_suc', models.ForeignKey(to='admin_historic.UsersProcesses', null=True, blank=True)),
            ],
            options={
                'db_tablespace': 'ts_comer',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='taquillasessionsdetail',
            name='userprocess',
            field=models.ForeignKey(to='admin_historic.UsersProcesses'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sessionsdetaildetail',
            name='userprocess',
            field=models.ForeignKey(to='admin_historic.UsersProcesses'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sessionsdetail',
            name='userprocess',
            field=models.ForeignKey(to='admin_historic.UsersProcesses'),
            preserve_default=True,
        ),
    ]

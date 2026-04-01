# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_profiles', '0003_auto_20150302_1941'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parroquias',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 3, 10, 12, 55, 34, 904965), auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2015, 3, 10, 12, 55, 34, 905019), auto_now=True)),
                ('municipio', models.ForeignKey(to='admin_profiles.Municipios')),
            ],
            options={
                'verbose_name': 'Parroquia',
                'verbose_name_plural': 'Parroquias',
                'ordering': ['nombre'],
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='ciudades',
            name='municipio',
        ),
        migrations.RemoveField(
            model_name='direcciones',
            name='ciudad',
        ),
        migrations.DeleteModel(
            name='Ciudades',
        ),
        migrations.AddField(
            model_name='direcciones',
            name='latitud',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='direcciones',
            name='longitud',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='direcciones',
            name='parroquia',
            field=models.ForeignKey(to='admin_profiles.Parroquias', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='municipios',
            name='capital',
            field=models.CharField(max_length=100, null= True),
            preserve_default=True,
        ),
    ]

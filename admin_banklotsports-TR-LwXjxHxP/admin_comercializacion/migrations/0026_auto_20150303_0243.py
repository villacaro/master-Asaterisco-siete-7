# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('admin_finanzas', '0005_auto_20150302_1941'),
        ('admin_comercializacion', '0025_auto_20150302_1941'),
    ]

    operations = [
        migrations.CreateModel(
            name='FactorRiesgo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('factores', jsonfield.fields.JSONField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comercializadora', models.OneToOneField(to='admin_finanzas.Comercializadora', editable=False)),
            ],
            options={
                'verbose_name_plural': 'Factores de riesgo',
                'verbose_name': 'Factor de riesgo',
                'ordering': ['-created_at'],
                'db_tablespace': 'ts_comer',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='usuariostaquilla',
            name='last_login',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login'),
            preserve_default=True,
        ),
    ]

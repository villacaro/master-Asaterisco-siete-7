# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('admin_themes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('color', models.CharField(max_length=140, verbose_name='Color (*)')),
                ('color_type', models.IntegerField(choices=[(0, 'Primary'), (1, 'Secondary'), (2, 'Default')], verbose_name='Tipo de color (*)')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, auto_now=True)),
                ('theme', models.ForeignKey(to='admin_themes.Theme', verbose_name='Tema (*)')),
            ],
            options={
                'verbose_name_plural': 'Colores',
                'verbose_name': 'Color',
            },
            bases=(models.Model,),
        ),
    ]

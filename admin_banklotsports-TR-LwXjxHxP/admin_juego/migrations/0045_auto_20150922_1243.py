# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0044_auto_20150918_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='encuentros',
            name='pk_clone',
            field=models.IntegerField(db_index=True, default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='encuentrosdetail',
            name='pk_clone',
            field=models.IntegerField(db_index=True, default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='encuentrosmodalidades',
            name='pk_clone',
            field=models.IntegerField(db_index=True, default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='equipos',
            name='pk_clone',
            field=models.IntegerField(db_index=True, default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gruposjuego',
            name='pk_clone',
            field=models.IntegerField(db_index=True, default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jornadas',
            name='pk_clone',
            field=models.IntegerField(db_index=True, default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jugadas',
            name='pk_clone',
            field=models.IntegerField(db_index=True, default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jugador',
            name='pk_clone',
            field=models.IntegerField(db_index=True, default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jugadortipo',
            name='pk_clone',
            field=models.IntegerField(db_index=True, default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='temporadas',
            name='pk_clone',
            field=models.IntegerField(db_index=True, default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='torneos',
            name='pk_clone',
            field=models.IntegerField(db_index=True, default=0),
            preserve_default=True,
        ),
    ]

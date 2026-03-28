# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0073_auto_20160113_1200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preferencias',
            name='tipo',
        ),
        migrations.RemoveField(
            model_name='preferencias',
            name='user_type',
        ),
        migrations.RemoveField(
            model_name='preferenciascadena',
            name='agencia',
        ),
        migrations.RemoveField(
            model_name='preferenciascadena',
            name='banca',
        ),
        migrations.RemoveField(
            model_name='preferenciascadena',
            name='bloque',
        ),
        migrations.RemoveField(
            model_name='preferenciascadena',
            name='distribuidor',
        ),
        migrations.RemoveField(
            model_name='preferenciascadena',
            name='preferencia',
        ),
        migrations.DeleteModel(
            name='Preferencias',
        ),
        migrations.DeleteModel(
            name='PreferenciasCadena',
        ),
        migrations.DeleteModel(
            name='TipoPreferencias',
        ),
    ]

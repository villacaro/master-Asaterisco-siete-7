# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


def MigrateDataUsers(apps, schema_editor):
    from scripts import migrate_data_menu_permisos_and_historic

    migrate_data_menu_permisos_and_historic.run()


class Migration(migrations.Migration):

    dependencies = [
        ('admin_users', '0017_auto_20150114_1154'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'ordering': ['content_type'], 'verbose_name_plural': 'Tipos de usuarios', 'verbose_name': 'Tipo de usuario'},
        ),
        migrations.AlterModelOptions(
            name='users',
            options={'ordering': ['user'], 'verbose_name_plural': 'Usuarios', 'verbose_name': 'Usuario'},
        ),
    ]

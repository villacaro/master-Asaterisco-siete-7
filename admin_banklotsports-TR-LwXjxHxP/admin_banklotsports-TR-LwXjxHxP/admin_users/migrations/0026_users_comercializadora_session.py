# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


def MigrateDataUsers(apps, schema_editor):
    pass
    '''
    from scripts import migrate_data_users_001

    migrate_data_users_001.run()
    '''


class Migration(migrations.Migration):

    dependencies = [
        ('admin_finanzas', '0006_auto_20150305_2257'),
        ('admin_users', '0025_auto_20150305_2342'),
    ]

    operations = [
        migrations.RunPython(MigrateDataUsers),
    ]

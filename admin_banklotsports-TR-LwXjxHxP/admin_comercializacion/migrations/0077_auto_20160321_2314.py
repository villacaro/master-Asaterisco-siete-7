# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def MigrateDataAll(apps, schema_editor):
    from admin_comercializacion.models import TypePreferences

    preference = TypePreferences.objects.get(
        codename='preference_queda_frequency'
    )
    preference.heredity = True
    preference.save()
    


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0075_auto_20160120_1403'),
    ]

    operations = [
        migrations.RunPython(MigrateDataAll),
    ]

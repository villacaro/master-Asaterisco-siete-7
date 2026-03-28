# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def MigrateDataAll(apps, schema_editor):
	from admin_permisologia.models import PermissionsSalesRestrictions
	#PermissionsSalesRestrictions.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('admin_permisologia', '0019_permissionssalesrestrictions_deporte'),
    ]

    operations = [
    	migrations.RunPython(MigrateDataAll),
    ]

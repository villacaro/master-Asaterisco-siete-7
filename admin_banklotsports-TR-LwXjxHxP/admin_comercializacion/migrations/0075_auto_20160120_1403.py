# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def MigrateDataAll(apps, schema_editor):
    from admin_users.models import UserProfile
    from admin_comercializacion.models import GroupPreferences, TypePreferences, DefaultPreferences
    profiles = UserProfile.objects.filter(
        codename='userprofile_agencia'
    )
    comparison_codenames = {
        'codename_min': 1,
        'codename_max': 2,
        'codename_free': 3,
    }
    comparison_type = {
        'codename_int': 1,
        'codename_decimal': 2,
        'codename_string': 3,
    }

    preference_cancel_ticket = TypePreferences.objects.update_or_create(
        codename='preference_cancel_ticket',
        defaults={
            'name': 'Permitir anular tickets',
            'comparison': comparison_codenames['codename_free'],
            'order': 4,
            'group': GroupPreferences.objects.get(codename='group_ticket'),
            'type_data': comparison_type['codename_int'],
            'edit': False,
        }
    )
    preference_cancel_ticket[0].profile.add(*profiles)

    DefaultPreferences.objects.update_or_create(
        value=1,
        default=True,
        typepreference=preference_cancel_ticket[0],
    ),


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0074_auto_20160113_2308'),
    ]

    operations = [
        migrations.RunPython(MigrateDataAll),
    ]

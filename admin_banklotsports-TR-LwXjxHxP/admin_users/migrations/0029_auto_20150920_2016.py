# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_users', '0028_remove_users_passwd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='codename',
            field=models.CharField(db_index=True, unique=True, max_length=160),
            preserve_default=True,
        ),
    ]

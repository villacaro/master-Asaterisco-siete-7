# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_themes', '0002_color'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='color',
            unique_together=set([('theme', 'color'), ('theme', 'color_type')]),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0052_auto_20151104_1738'),
        ('admin_permisologia', '0018_permissionssalesrestrictions'),
    ]

    operations = [
        migrations.AddField(
            model_name='permissionssalesrestrictions',
            name='deporte',
            field=models.ForeignKey(default=1, to='admin_juego.Deportes'),
            preserve_default=False,
        ),
        
    ]

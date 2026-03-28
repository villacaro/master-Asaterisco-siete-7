# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0040_auto_20150901_1652'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='encuentrosmodalidades',
            unique_together=set([('encuentro', 'deporte_grupo', 'modalidad_grupo', 'sistema')]),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_mail', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='priority',
            field=models.CharField(default='1', verbose_name='Prioridad', choices=[['0', 'Alta'], ['1', 'Media'], ['2', 'Baja']], max_length=1, help_text='Seleccione la priodidad que desea con la que se envie el mensaje'),
            preserve_default=True,
        ),
    ]

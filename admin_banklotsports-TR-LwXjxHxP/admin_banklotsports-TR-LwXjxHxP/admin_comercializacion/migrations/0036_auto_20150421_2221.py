# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0035_auto_20150324_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agencias',
            name='email',
            field=models.EmailField(null=True, verbose_name='Correo electronico ', blank=True, help_text='Ingrese el correo electronico', max_length=254),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bancas',
            name='email',
            field=models.EmailField(null=True, verbose_name='Correo electronico ', blank=True, help_text='Ingrese el correo electronico', max_length=254),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bloques',
            name='email',
            field=models.EmailField(null=True, verbose_name='Correo electronico ', blank=True, help_text='Ingrese el correo electronico', max_length=254),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='distribuidores',
            name='email',
            field=models.EmailField(null=True, verbose_name='Correo electronico ', blank=True, help_text='Ingrese el correo electronico', max_length=254),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='operadoras',
            name='email',
            field=models.EmailField(null=True, verbose_name='Correo electronico ', blank=True, help_text='Ingrese el correo electronico', max_length=254),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('admin_finanzas', '0013_comercializadora_resumen_personalizado_comer'),
        ('admin_permisologia', '0017_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='PermissionsSalesRestrictions',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('restrictions', jsonfield.fields.JSONField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comercializadora', models.ForeignKey(to='admin_finanzas.Comercializadora')),
            ],
            options={
                'verbose_name': 'Permiso Venta (Restricciones)',
                'db_tablespace': 'ts_comer',
                'verbose_name_plural': 'Permisos ventas (Restricciones)',
            },
            bases=(models.Model,),
        ),
    ]

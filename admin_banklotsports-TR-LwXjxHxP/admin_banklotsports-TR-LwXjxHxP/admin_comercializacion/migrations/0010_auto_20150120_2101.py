# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime

def MigratePassword(apps, schema_editor):
    from admin_comercializacion.models import UsuariosTaquilla, TaquillaDataDefault

    default = TaquillaDataDefault.objects.all()
    if default.exists():
        default = default[0]
        for user in UsuariosTaquilla.objects.all():
            user.set_password( default.passwd )
            user.save( update_fields = ["password"] )

class Migration(migrations.Migration):

    dependencies = [
        ('admin_status', '0001_initial'),
        ('admin_comercializacion', '0009_auto_20150119_1407'),
    ]

    operations = [
        
        migrations.RunPython(MigratePassword),

        migrations.RemoveField(
            model_name='usuariostaquilla',
            name='passwd',
        ),
        migrations.AlterField(
            model_name='agencias',
            name='nombre',
            field=models.CharField(verbose_name='Nombre (*)', help_text='Ingrese nombre', max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bancas',
            name='is_sistema_juego',
            field=models.BooleanField(default=False, verbose_name='¿Administra un sistema de juego? ', help_text='Seleccione este campo solo si desea que la banca tenga su propio sistema de juego'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bancas',
            name='nombre',
            field=models.CharField(verbose_name='Nombre (*)', help_text='Ingrese nombre', max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bloques',
            name='nombre',
            field=models.CharField(verbose_name='Nombre (*)', help_text='Ingrese nombre', max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='distribuidores',
            name='nombre',
            field=models.CharField(verbose_name='Nombre (*)', help_text='Ingrese nombre', max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='operadoras',
            name='nombre',
            field=models.CharField(verbose_name='Nombre (*)', help_text='Ingrese nombre', max_length=100),
            preserve_default=True,
        ),
    ]

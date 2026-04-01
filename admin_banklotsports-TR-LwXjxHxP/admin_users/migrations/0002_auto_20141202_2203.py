# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.utils.timezone

class Migration(migrations.Migration):

    dependencies = [
        ('admin_users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='profile',
            new_name='nombre',
        ),
        migrations.AddField(
            model_name='users',
            name='last_login',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='users',
            name='password',
            field=models.CharField(default='', verbose_name='password', max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='users',
            name='profile',
            field=models.ForeignKey(null=True, verbose_name='Perfil de usuario (*)', help_text='Seleccione el perfil de usuario', to='admin_users.UserProfile'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='users',
            name='token',
            field=models.CharField(null=True, editable=False, max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='users',
            name='user_ref',
            field=models.ForeignKey(null=True, editable=False, to='admin_users.Users'),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_finanzas', '0013_comercializadora_resumen_personalizado_comer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('subject', models.CharField(help_text='Introduzca el asusto del mensaje', max_length=100, verbose_name='Asunto')),
                ('body', models.TextField(help_text='Introduzca el texto a enviar', verbose_name='Mensaje', blank=True)),
                ('priority', models.CharField(choices=[('0', 'Alta'), ('1', 'Media'), ('2', 'Baja')], max_length=1, help_text='Seleccione la priodidad que desea con la que se envie el mensaje', default='1', verbose_name='Prioridad')),
                ('send_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_tablespace': 'ts_comer',
                'verbose_name_plural': 'Mensajes',
                'verbose_name': 'Mensaje',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MessageAdjunt',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('adjunt', models.FileField(upload_to='message_adjunt')),
            ],
            options={
                'db_tablespace': 'ts_comer',
                'verbose_name_plural': 'Adjuntos de un mensaje',
                'verbose_name': 'Adjunto de un mensaje',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MessageComer',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('read', models.BooleanField(default=False)),
                ('tray_group', models.CharField(choices=[('1', 'Recibidos'), ('2', 'Enviados'), ('3', 'Archivados'), ('4', 'Papelera')], max_length=1, default='1')),
                ('comercializadora', models.ForeignKey(to='admin_finanzas.Comercializadora', editable=False)),
                ('message', models.ForeignKey(to='admin_mail.Message', editable=False)),
            ],
            options={
                'ordering': ['-message__send_at'],
                'db_tablespace': 'ts_comer',
                'verbose_name_plural': 'Mensajes',
                'verbose_name': 'Mensaje',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MessageSend',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('options', models.CharField(choices=[('1', 'Simple'), ('2', 'Masivo'), ('3', 'Taquillas')], max_length=1, default='1')),
                ('message', models.OneToOneField(to='admin_mail.Message', editable=False)),
                ('to_comercializadora', models.ManyToManyField(to='admin_finanzas.Comercializadora')),
            ],
            options={
                'db_tablespace': 'ts_comer',
                'verbose_name_plural': 'Mensajes enviados',
                'verbose_name': 'Mensaje enviados',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='message',
            name='adjunts',
            field=models.ManyToManyField(related_name='message_adjunts', editable=False, to='admin_mail.MessageAdjunt'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='from_comercializadora',
            field=models.ForeignKey(to='admin_finanzas.Comercializadora', editable=False),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_users', '0011_auto_20141215_2303'),
        ('admin_status', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Condiciones',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('nombre', models.CharField(max_length=140, null=True, help_text='Ingrese nombre de la condición', verbose_name='Nombre ', blank=True)),
                ('equipo', models.BooleanField(default=False, help_text='Seleccione ese campo si se trata de una condición por equipo', verbose_name='¿Condición por equipo? ')),
                ('etiqueta_ref', models.BooleanField(default=False, help_text='Seleccione este campo si la condicion poseee eiqueta de referencia', verbose_name='¿Posee etiqueta de referencia ?')),
                ('orden', models.IntegerField(null=True, help_text='Ingrese el numero de orden de la condición', verbose_name='Numero de orden (*)', blank=True)),
                ('tipo', models.IntegerField(choices=[(0, 'Por equipo'), (1, 'Individual'), (2, 'Doble'), (4, 'Informativa por equipo')], verbose_name='Tipo de condición (*)')),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 12, 15, 23, 3, 51, 815480))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 15, 23, 3, 51, 815537), auto_now=True)),
            ],
            options={
                'db_tablespace': 'ts_parley',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Deportes',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('nombre', models.CharField(max_length=200, help_text='Ingrese nombre del deporte', unique=True, verbose_name='Nombre (*)')),
                ('orden', models.IntegerField(help_text='Ingrese la numeración de orden', verbose_name='Orden (*)')),
                ('logo', models.ImageField(help_text='Ingrese logo del deporte', blank=True, null=True, upload_to='deportes', verbose_name='Logo ')),
                ('fondoweb', models.ImageField(help_text='Ingrese fondo del deporte', blank=True, null=True, upload_to='deportes/fondos', verbose_name='Fondo')),
                ('cantidad', models.IntegerField(help_text='Seleccione la cantidad de equipos a enfrentarse por encuentro', choices=[(2, '2 participantes'), (1, '+2 participantes')], verbose_name='Participantes (*)')),
                ('cantidad_tiempos', models.IntegerField(help_text='Ingrese la cantidad de tiempos por encuentro mayor o igual a 2', verbose_name='Cantidad de tiempos por encuentro (*)')),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 12, 15, 23, 3, 51, 785194))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 15, 23, 3, 51, 785258), auto_now=True)),
            ],
            options={
                'db_tablespace': 'ts_parley',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Deportes_Grupos',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('deporte', models.ForeignKey(to='admin_juego.Deportes')),
            ],
            options={
                'db_tablespace': 'ts_parley',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Encuentros',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('horajuego', models.DateTimeField(help_text='Seleccione la fecha y hora de inicio del encuentro', verbose_name='Fecha y hora de inicio (*)')),
                ('horacierre', models.DateTimeField(help_text='Seleccione la fecha y hora de cierre del encuentro', verbose_name='Fecha y hora de cierre (*)')),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 12, 15, 23, 3, 51, 803021))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 15, 23, 3, 51, 803077), auto_now=True)),
            ],
            options={
                'db_tablespace': 'ts_parley',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EncuentrosDetail',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('referencia', models.CharField(null=True, max_length=140, blank=True)),
                ('indice', models.IntegerField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 12, 15, 23, 3, 51, 804563))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 15, 23, 3, 51, 804627), auto_now=True)),
                ('encuentro', models.ForeignKey(to='admin_juego.Encuentros')),
            ],
            options={
                'db_tablespace': 'ts_parley',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EncuentrosModalidades',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('etiqueta_ref', models.CharField(null=True, max_length=140, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 12, 15, 23, 3, 51, 813933))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 15, 23, 3, 51, 814001), auto_now=True)),
                ('deporte_grupo', models.ForeignKey(to='admin_juego.Deportes_Grupos', blank=True, null=True)),
                ('encuentro', models.ForeignKey(to='admin_juego.Encuentros')),
            ],
            options={
                'db_tablespace': 'ts_parley',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Equipos',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('nombre', models.CharField(max_length=140, help_text='Ingrese un nombre para el equipo, no pueden haber equipos con el mismo nombre en un deporte', verbose_name='Nombre (*)')),
                ('logo', models.ImageField(null=True, upload_to='equipos', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 12, 15, 23, 3, 51, 790626))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 15, 23, 3, 51, 790684), auto_now=True)),
                ('deporte', models.ForeignKey(to='admin_juego.Deportes', verbose_name='Deportes (*)')),
            ],
            options={
                'db_tablespace': 'ts_parley',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EquiposGrupos',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 12, 15, 23, 3, 51, 801576))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 15, 23, 3, 51, 801641), auto_now=True)),
                ('equipo', models.ForeignKey(to='admin_juego.Equipos')),
            ],
            options={
                'db_tablespace': 'ts_parley',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EquiposLigas',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 12, 15, 23, 3, 51, 795593))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 15, 23, 3, 51, 795670), auto_now=True)),
                ('equipo', models.ForeignKey(to='admin_juego.Equipos')),
            ],
            options={
                'db_tablespace': 'ts_parley',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EquiposTemporadas',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 12, 15, 23, 3, 51, 796980))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 15, 23, 3, 51, 797040), auto_now=True)),
                ('equipo', models.ForeignKey(to='admin_juego.Equipos')),
            ],
            options={
                'db_tablespace': 'ts_parley',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GruposApuestas',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('nombre', models.CharField(max_length=200, help_text='Ingrese nombre del grupo', unique=True, verbose_name='Nombre (*)')),
                ('codename', models.CharField(max_length=140, editable=False)),
                ('orden', models.IntegerField(help_text='Ingrese la numeración de orden', verbose_name='Orden (*)')),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 12, 15, 23, 3, 51, 806257))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 15, 23, 3, 51, 806315), auto_now=True)),
                ('deporte', models.ManyToManyField(through='admin_juego.Deportes_Grupos', help_text='Seleccione los deportes a los que desea asignar el grupo', to='admin_juego.Deportes', blank=True, null=True, verbose_name='Seleccione los deportes (*)')),
            ],
            options={
                'db_tablespace': 'ts_parley',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GruposJuego',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('nombre', models.CharField(max_length=200, help_text='Ingrese un nombre para el grupo', verbose_name='Nombre (*)')),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 12, 15, 23, 3, 51, 800291))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 15, 23, 3, 51, 800349), auto_now=True)),
            ],
            options={
                'db_tablespace': 'ts_parley',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Jornadas',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('jornada', models.CharField(max_length=140, help_text='Ingrese nombre de la jornada', verbose_name='Nombre (*)')),
                ('fechaini', models.DateField(help_text='Fecha de inicio de la jornada', verbose_name='Fecha de inicio (*)')),
                ('fechafin', models.DateField(help_text='Fecha de fin de la jornada', verbose_name='Fecha de fin (*)')),
                ('parley', models.BooleanField(default=False, help_text='Seleccione este campo solo si la temporada admite venta de parley', verbose_name='Permite la venta de parley?')),
                ('quiniela', models.BooleanField(default=False, help_text='Seleccione este campo solo si la temporada admite venta de quiniela', verbose_name='Permite la venta de quiniela?')),
                ('apuestasimple', models.BooleanField(default=False, help_text='Seleccione este campo solo si la temporada admite venta de apuesta simple', verbose_name='Permite la venta de apuesta simple?')),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 12, 15, 23, 3, 51, 798519))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 15, 23, 3, 51, 798574), auto_now=True)),
            ],
            options={
                'db_tablespace': 'ts_parley',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Jugadas',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('indice', models.IntegerField(null=True, blank=True)),
                ('valor_etq_ref', models.CharField(null=True, max_length=140, blank=True)),
                ('valor_americano', models.IntegerField(null=True, blank=True)),
                ('valor_europeo', models.DecimalField(max_digits=10, null=True, decimal_places=2, blank=True)),
                ('favorito', models.NullBooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 12, 15, 23, 3, 51, 818889))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 15, 23, 3, 51, 818950), auto_now=True)),
                ('condicion', models.ForeignKey(to='admin_juego.Condiciones', blank=True, null=True)),
                ('detalle_encuentro', models.ForeignKey(to='admin_juego.EncuentrosDetail', blank=True, null=True)),
                ('encuentros_modalidad', models.ForeignKey(to='admin_juego.EncuentrosModalidades', blank=True, null=True)),
                ('status', models.ForeignKey(to='admin_status.Status', blank=True, null=True)),
            ],
            options={
                'db_tablespace': 'ts_parley',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JugadasInformativas',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('ref_principal', models.CharField(null=True, max_length=140, blank=True)),
                ('ref_other_1', models.CharField(null=True, max_length=140, blank=True)),
                ('ref_other_2', models.CharField(null=True, max_length=140, blank=True)),
                ('ref_other_3', models.CharField(null=True, max_length=140, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 12, 15, 23, 3, 51, 817267))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 15, 23, 3, 51, 817324), auto_now=True)),
                ('condicion', models.ForeignKey(to='admin_juego.Condiciones')),
                ('detalle_encuentro', models.ForeignKey(to='admin_juego.EncuentrosDetail', blank=True, null=True)),
                ('encuentros_modalidad', models.ForeignKey(to='admin_juego.EncuentrosModalidades', blank=True, null=True)),
            ],
            options={
                'db_tablespace': 'ts_parley',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Jugador',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('nombre', models.CharField(max_length=140, help_text='Ingrese un nombre para el jugador', verbose_name='Nombre (*)')),
                ('lateralidad', models.CharField(max_length=140, help_text='Ingrese la lateralidad del jugador', choices=[('D', 'Derecho'), ('Z', 'Zurzo')], verbose_name='Lateralidad (*)')),
                ('foto', models.ImageField(null=True, upload_to='jugadores', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 12, 15, 23, 3, 51, 793978))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 15, 23, 3, 51, 794036), auto_now=True)),
            ],
            options={
                'db_tablespace': 'ts_parley',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JugadorTipo',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('nombre', models.CharField(max_length=200, help_text='Ingrese un nombre para el tipo de jugador', verbose_name='Tipo de jugador (*)')),
                ('codename', models.CharField(max_length=200, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 12, 15, 23, 3, 51, 792513))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 15, 23, 3, 51, 792574), auto_now=True)),
                ('deporte', models.ForeignKey(help_text='Seleccione el deporte al que pertenece el tipo de jugador', verbose_name='Deportes (*)', to='admin_juego.Deportes')),
            ],
            options={
                'db_tablespace': 'ts_parley',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Modalidades',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('modalidad', models.CharField(max_length=200, help_text='Ingrese nombre de la modalidad', unique=True, verbose_name='Nombre (*)')),
                ('orden', models.IntegerField(help_text='Ingrese la numeración de orden', verbose_name='Orden (*)')),
                ('descripcion', models.CharField(max_length=200, null=True, help_text='Ingrese la descrición de la modalidad', verbose_name='Descripción ', blank=True)),
                ('etiqueta_ref', models.BooleanField(default=False, help_text='En caso de poseer etiqueta de referencia seleccione este campo', verbose_name='¿Posee etiqueta de referencia? ')),
                ('codename', models.CharField(max_length=140, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 12, 15, 23, 3, 51, 808790))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 15, 23, 3, 51, 808848), auto_now=True)),
            ],
            options={
                'db_tablespace': 'ts_parley',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Modalidades_Grupos',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('deporte_restriccion', models.ManyToManyField(null=True, help_text='Seleccione los deportes a quitar de la relacion entre grupos y modalidad, solo se puede restringir los seleccionados en un principio para el grupo', verbose_name='Deportes a restringir', to='admin_juego.Deportes', blank=True)),
                ('grupo', models.ForeignKey(to='admin_juego.GruposApuestas')),
                ('modalidad', models.ForeignKey(to='admin_juego.Modalidades')),
            ],
            options={
                'db_tablespace': 'ts_parley',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RestriccionesReferencias',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('max_logro_favorito', models.IntegerField(null=True, help_text='Ingrese el valor debe ser negativo', verbose_name='Logro maximo (-) favoritos (*)', blank=True)),
                ('max_logro_no_favorito', models.IntegerField(null=True, help_text='Ingrese el valor debe ser positivo', verbose_name='Logro maximo (+) no favoritos (*)', blank=True)),
                ('min_ref', models.CharField(max_length=140, null=True, help_text='Ingrese la referencia minima', verbose_name='Referencia minima (*)', blank=True)),
                ('max_ref', models.CharField(max_length=140, null=True, help_text='Ingrese la referencia maxima', verbose_name='Referencia maxima (*)', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 12, 15, 23, 3, 51, 820763))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 15, 23, 3, 51, 820822), auto_now=True)),
                ('condicion', models.ForeignKey(to='admin_juego.Condiciones', blank=True, null=True)),
                ('deporte', models.ForeignKey(to='admin_juego.Deportes')),
                ('grupo', models.ForeignKey(to='admin_juego.GruposApuestas')),
                ('modalidad', models.ForeignKey(to='admin_juego.Modalidades', blank=True, null=True)),
            ],
            options={
                'db_tablespace': 'ts_parley',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SistemaJuego',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('nombre', models.CharField(null=True, max_length=200, blank=True)),
                ('logo', models.ImageField(null=True, upload_to='sistema', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 12, 15, 23, 3, 51, 780403))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 15, 23, 3, 51, 780466), auto_now=True)),
                ('user', models.ForeignKey(to='admin_users.Users')),
            ],
            options={
                'db_tablespace': 'ts_parley',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Temporadas',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('nombre', models.CharField(max_length=140, help_text='Ingrese nombre a la temporada', verbose_name='Nombre (*)')),
                ('fechaini', models.DateField(help_text='Seleccione la fecha de inicio de la temporada', verbose_name='Fecha de inicio (*)')),
                ('fechafin', models.DateField(help_text='Seleccione la fecha de fin de la temporada', verbose_name='Fecha de fin (*)')),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 12, 15, 23, 3, 51, 789156))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 15, 23, 3, 51, 789212), auto_now=True)),
                ('status', models.ForeignKey(help_text='Seleccione un estatus para la temporada', verbose_name='Estatus (*)', to='admin_status.Status')),
            ],
            options={
                'db_tablespace': 'ts_parley',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Torneos',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('nombre', models.CharField(max_length=200, help_text='Ingrese nombre de la liga', verbose_name='Nombre (*)')),
                ('logo', models.ImageField(help_text='Ingrese logo de la liga', blank=True, null=True, upload_to='eventos', verbose_name='Logo')),
                ('fondoweb', models.ImageField(help_text='Ingrese fondo de la liga', blank=True, null=True, upload_to='eventos/fondos', verbose_name='Fondo')),
                ('por_jornadas', models.BooleanField(default=False, help_text='De ser una liga que admite jornadas, seleccione el campo', verbose_name='Liga por jornadas')),
                ('por_grupos', models.BooleanField(default=False, help_text='De ser una liga que admite grupos, seleccione el campo', verbose_name='Liga por grupos')),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 12, 15, 23, 3, 51, 787111))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 15, 23, 3, 51, 787169), auto_now=True)),
                ('deporte', models.ForeignKey(help_text='Seleccione el deporte para la liga', verbose_name='Deporte (*)', to='admin_juego.Deportes')),
            ],
            options={
                'db_tablespace': 'ts_parley',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='torneos',
            unique_together=set([('nombre', 'deporte')]),
        ),
        migrations.AddField(
            model_name='temporadas',
            name='torneo',
            field=models.ForeignKey(help_text='Seleccione una liga para la temporada', verbose_name='Liga (*)', to='admin_juego.Torneos'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='temporadas',
            unique_together=set([('nombre', 'torneo')]),
        ),
        migrations.AlterUniqueTogether(
            name='modalidades_grupos',
            unique_together=set([('modalidad', 'grupo')]),
        ),
        migrations.AddField(
            model_name='modalidades',
            name='grupo',
            field=models.ManyToManyField(through='admin_juego.Modalidades_Grupos', help_text='Seleccione los grupos a los que pertenece la modalidad', to='admin_juego.GruposApuestas', blank=True, null=True, verbose_name='Seleccione los grupos (*)'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='modalidades',
            name='restriction',
            field=models.ManyToManyField(help_text='Selecciones las restricciones a necesarias', to='admin_juego.Modalidades', blank=True, null=True, related_name='restriction_rel_+', verbose_name='Restricciones '),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='jugadortipo',
            unique_together=set([('nombre', 'deporte')]),
        ),
        migrations.AddField(
            model_name='jugador',
            name='tipo',
            field=models.ForeignKey(help_text='Seleccione el tipo de jugador al que pertenece el jugador', verbose_name='Tipo de jugador (*)', to='admin_juego.JugadorTipo'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='jugador',
            unique_together=set([('nombre', 'tipo')]),
        ),
        migrations.AddField(
            model_name='jornadas',
            name='sistema',
            field=models.ForeignKey(to='admin_juego.SistemaJuego', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jornadas',
            name='status',
            field=models.ForeignKey(help_text='Seleccione un estatus para la jornada', verbose_name='Estatus (*)', to='admin_status.Status'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jornadas',
            name='temporadas',
            field=models.ForeignKey(help_text='Seleccione una temporada para la jornada', verbose_name='Temporada (*)', to='admin_juego.Temporadas'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='jornadas',
            unique_together=set([('jornada', 'temporadas', 'sistema')]),
        ),
        migrations.AddField(
            model_name='gruposjuego',
            name='temporada',
            field=models.ForeignKey(help_text='Seleccione una temporada para el grupo', verbose_name='Temporada (*)', to='admin_juego.Temporadas'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='gruposjuego',
            unique_together=set([('nombre', 'temporada')]),
        ),
        migrations.AddField(
            model_name='equipostemporadas',
            name='temporada',
            field=models.ForeignKey(to='admin_juego.Temporadas'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='equipostemporadas',
            unique_together=set([('equipo', 'temporada')]),
        ),
        migrations.AddField(
            model_name='equiposligas',
            name='liga',
            field=models.ForeignKey(to='admin_juego.Torneos'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='equiposligas',
            unique_together=set([('equipo', 'liga')]),
        ),
        migrations.AddField(
            model_name='equiposgrupos',
            name='grupo',
            field=models.ForeignKey(to='admin_juego.GruposJuego'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='equiposgrupos',
            unique_together=set([('equipo', 'grupo')]),
        ),
        migrations.AlterUniqueTogether(
            name='equipos',
            unique_together=set([('nombre', 'deporte')]),
        ),
        migrations.AddField(
            model_name='encuentrosmodalidades',
            name='modalidad_grupo',
            field=models.ForeignKey(to='admin_juego.Modalidades_Grupos', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='encuentrosmodalidades',
            unique_together=set([('encuentro', 'deporte_grupo', 'modalidad_grupo')]),
        ),
        migrations.AddField(
            model_name='encuentrosdetail',
            name='equipos_temporadas',
            field=models.ForeignKey(to='admin_juego.EquiposTemporadas'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='encuentrosdetail',
            name='jugador',
            field=models.ForeignKey(null=True, to='admin_juego.Jugador'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='encuentrosdetail',
            unique_together=set([('encuentro', 'equipos_temporadas')]),
        ),
        migrations.AddField(
            model_name='encuentros',
            name='grupo',
            field=models.ForeignKey(help_text='Seleccione un grupo para el encuentro', to='admin_juego.GruposJuego', blank=True, null=True, verbose_name='Grupo '),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='encuentros',
            name='jornada',
            field=models.ForeignKey(help_text='Seleccione una jornada para el encuentro', verbose_name='Jornada (*)', to='admin_juego.Jornadas'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='encuentros',
            name='status',
            field=models.ForeignKey(help_text='Seleccione un estatus para el encuentro', verbose_name='Estatus (*)', to='admin_status.Status'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deportes_grupos',
            name='grupo',
            field=models.ForeignKey(to='admin_juego.GruposApuestas'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='deportes_grupos',
            unique_together=set([('deporte', 'grupo')]),
        ),
        migrations.AddField(
            model_name='condiciones',
            name='modalidad',
            field=models.ForeignKey(to='admin_juego.Modalidades'),
            preserve_default=True,
        ),
    ]

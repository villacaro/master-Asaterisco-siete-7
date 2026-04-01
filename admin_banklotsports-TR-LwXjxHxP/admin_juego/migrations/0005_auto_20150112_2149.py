# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0004_auto_20150108_0942'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='condiciones',
            options={'verbose_name': 'Condicion de apuesta', 'verbose_name_plural': 'Condiciones de apuestas'},
        ),
        migrations.AlterModelOptions(
            name='deportes',
            options={'verbose_name': 'Deporte', 'verbose_name_plural': 'Deportes', 'ordering': ['orden']},
        ),
        migrations.AlterModelOptions(
            name='deportes_grupos',
            options={'verbose_name': 'Grupo de apuesta por deporte', 'verbose_name_plural': 'Grupos de apuestas  por deportes'},
        ),
        migrations.AlterModelOptions(
            name='encuentros',
            options={'verbose_name': 'Encuentro', 'verbose_name_plural': 'Encuentros'},
        ),
        migrations.AlterModelOptions(
            name='encuentrosdetail',
            options={'verbose_name': 'Detalle de encuentro', 'verbose_name_plural': 'Detalle de los encuentros'},
        ),
        migrations.AlterModelOptions(
            name='encuentrosmodalidades',
            options={'verbose_name': 'Modalidad por encuentro', 'verbose_name_plural': 'Modalidades por encuentros'},
        ),
        migrations.AlterModelOptions(
            name='equipos',
            options={'verbose_name': 'Equipo', 'verbose_name_plural': 'Equipos'},
        ),
        migrations.AlterModelOptions(
            name='equiposgrupos',
            options={'verbose_name': 'Equipo por grupo de juego', 'verbose_name_plural': 'Equipos por grupos de juego'},
        ),
        migrations.AlterModelOptions(
            name='equiposligas',
            options={'verbose_name': 'Equipo por liga', 'verbose_name_plural': 'Equipos por ligas'},
        ),
        migrations.AlterModelOptions(
            name='equipostemporadas',
            options={'verbose_name': 'Equipo por temporada', 'verbose_name_plural': 'Equipos por temporadas'},
        ),
        migrations.AlterModelOptions(
            name='gruposapuestas',
            options={'verbose_name': 'Grupo de apuesta', 'verbose_name_plural': 'Grupos de apuestas'},
        ),
        migrations.AlterModelOptions(
            name='gruposjuego',
            options={'verbose_name': 'Grupo de juego por temporada', 'verbose_name_plural': 'Grupos de juegos por temporadas'},
        ),
        migrations.AlterModelOptions(
            name='jornadas',
            options={'verbose_name': 'Jornada', 'verbose_name_plural': 'Jornadas'},
        ),
        migrations.AlterModelOptions(
            name='jugadas',
            options={'verbose_name': 'Jugada por encuentro', 'verbose_name_plural': 'Jugadas por encuentros'},
        ),
        migrations.AlterModelOptions(
            name='jugadasinformativas',
            options={'verbose_name': 'Jugada informativa', 'verbose_name_plural': 'Jugadas informativas'},
        ),
        migrations.AlterModelOptions(
            name='jugador',
            options={'verbose_name': 'Jugador', 'verbose_name_plural': 'Jugadores'},
        ),
        migrations.AlterModelOptions(
            name='jugadortipo',
            options={'verbose_name': 'Tipo de jugados', 'verbose_name_plural': 'Tipos de jugadores'},
        ),
        migrations.AlterModelOptions(
            name='modalidades',
            options={'verbose_name': 'Modalidad de apuesta', 'verbose_name_plural': 'Modalidades de apuestas'},
        ),
        migrations.AlterModelOptions(
            name='modalidades_grupos',
            options={'verbose_name': 'Modalidad por grupo de apuesta', 'verbose_name_plural': 'Modalidades por grupos de apuestas'},
        ),
        migrations.AlterModelOptions(
            name='restriccionesreferencias',
            options={'verbose_name': 'Restriccion de referencia y logro', 'verbose_name_plural': 'Restricciones de referencias y logros'},
        ),
        migrations.AlterModelOptions(
            name='sistemajuego',
            options={'verbose_name': 'Sistema de juego', 'verbose_name_plural': 'Sistemas de juegos', 'ordering': ['nombre']},
        ),
        migrations.AlterModelOptions(
            name='temporadas',
            options={'verbose_name': 'Temporada', 'verbose_name_plural': 'Temporadas', 'ordering': ['-fechaini']},
        ),
        migrations.AlterModelOptions(
            name='torneos',
            options={'verbose_name': 'Liga', 'verbose_name_plural': 'Ligas'},
        ),
        migrations.AlterField(
            model_name='condiciones',
            name='etiqueta_ref',
            field=models.BooleanField(help_text='Seleccione este campo si la condicion poseee eiqueta de referencia', default=False, verbose_name='¿Posee etiqueta de referencia ? '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='deportes',
            name='fondoweb',
            field=models.ImageField(verbose_name='Fondo ', help_text='Ingrese fondo del deporte', upload_to='deportes/fondos', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='equipos',
            name='deporte',
            field=models.ForeignKey(verbose_name='Deporte (*)', to='admin_juego.Deportes'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='jornadas',
            name='apuestasimple',
            field=models.BooleanField(help_text='Seleccione este campo solo si la temporada admite venta de apuesta simple', default=False, verbose_name='Permite la venta de apuesta simple? '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='jornadas',
            name='parley',
            field=models.BooleanField(help_text='Seleccione este campo solo si la temporada admite venta de parley', default=False, verbose_name='Permite la venta de parley? '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='jornadas',
            name='quiniela',
            field=models.BooleanField(help_text='Seleccione este campo solo si la temporada admite venta de quiniela', default=False, verbose_name='Permite la venta de quiniela? '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='modalidades_grupos',
            name='deporte_restriccion',
            field=models.ManyToManyField(help_text='Seleccione los deportes a quitar de la relacion entre grupos y modalidad, solo se puede restringir  los seleccionados en un principio para el grupo', to='admin_juego.Deportes', null=True, blank=True, verbose_name='Deportes a restringir '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='torneos',
            name='fondoweb',
            field=models.ImageField(verbose_name='Fondo ', help_text='Ingrese fondo de la liga', upload_to='eventos/fondos', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='torneos',
            name='logo',
            field=models.ImageField(verbose_name='Logo ', help_text='Ingrese logo de la liga', upload_to='eventos', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='torneos',
            name='por_jornadas',
            field=models.BooleanField(help_text='De ser una liga que admite jornadas, seleccione el campo', default=False, verbose_name='Liga por jornadas '),
            preserve_default=True,
        ),
    ]

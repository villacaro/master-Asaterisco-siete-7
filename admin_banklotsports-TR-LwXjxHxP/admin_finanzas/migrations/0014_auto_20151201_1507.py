# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_finanzas', '0013_comercializadora_resumen_personalizado_comer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comercializadora',
            name='agencia',
            field=models.ForeignKey(blank=True, verbose_name='Agencia', editable=False, to='admin_comercializacion.Agencias', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comercializadora',
            name='banca',
            field=models.ForeignKey(blank=True, verbose_name='Banca', editable=False, to='admin_comercializacion.Bancas', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comercializadora',
            name='bloque',
            field=models.ForeignKey(blank=True, verbose_name='Bloque', editable=False, to='admin_comercializacion.Bloques', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comercializadora',
            name='distribuidor',
            field=models.ForeignKey(blank=True, verbose_name='Distribuidor', editable=False, to='admin_comercializacion.Distribuidores', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comercializadora',
            name='operadora',
            field=models.ForeignKey(blank=True, verbose_name='Operadora', editable=False, to='admin_comercializacion.Operadoras', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comercializadora',
            name='saldo_fecha',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de saldo inicial (*)', help_text='Introduzca la fecha del saldo inicial de la comercializadora'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comercializadora',
            name='saldo_inicial',
            field=models.DecimalField(blank=True, verbose_name='Saldo inicial (*)', help_text='Introduzca el saldo inicial de la comercializadora', default=0.0, decimal_places=2, max_digits=15, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comercializadora',
            name='taquilla',
            field=models.ForeignKey(blank=True, verbose_name='Taquilla', editable=False, to='admin_comercializacion.Taquillas', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cuenta',
            name='comercializadora',
            field=models.ForeignKey(blank=True, verbose_name='Comercializadora ', editable=False, to='admin_finanzas.Comercializadora', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cuenta',
            name='description',
            field=models.CharField(max_length=100, verbose_name='Descripción (*)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dia',
            name='fecha',
            field=models.DateField(unique=True, verbose_name='Fecha '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='diatrabajo',
            name='actual',
            field=models.BooleanField(default=True, verbose_name='Actual'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='diatrabajo',
            name='comercializadora',
            field=models.ForeignKey(verbose_name='Comercializadora', to='admin_finanzas.Comercializadora'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='diatrabajo',
            name='dia',
            field=models.ForeignKey(verbose_name='Día', to='admin_finanzas.Dia'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='diatrabajo',
            name='procesado',
            field=models.BooleanField(default=False, verbose_name='Procesado'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='estatocuenta',
            name='cuenta',
            field=models.ForeignKey(verbose_name='Cuenta', to='admin_finanzas.Cuenta'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='estatocuenta',
            name='dia',
            field=models.ForeignKey(verbose_name='Día', to='admin_finanzas.Dia'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='estatocuenta',
            name='saldo',
            field=models.DecimalField(default=0.0, max_digits=15, decimal_places=2, verbose_name='Saldo'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movimiento',
            name='comprobante',
            field=models.ImageField(blank=True, upload_to='movimientos', null=True, verbose_name='Comprobante '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movimiento',
            name='dia',
            field=models.ForeignKey(verbose_name='Día ', to='admin_finanzas.Dia'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movimiento',
            name='tipo',
            field=models.ForeignKey(verbose_name='Tipo de movimiento', to='admin_finanzas.TipoMovimiento'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movimiento',
            name='user',
            field=models.ForeignKey(blank=True, verbose_name='Usuario ', to='admin_users.Users', null=True, on_delete=django.db.models.deletion.SET_NULL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tipomovimiento',
            name='codename',
            field=models.CharField(max_length=100, verbose_name='Código (*)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tipomovimiento',
            name='description',
            field=models.CharField(max_length=100, verbose_name='Descripción (*)'),
            preserve_default=True,
        ),
    ]

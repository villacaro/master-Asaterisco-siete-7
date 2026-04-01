# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime

def ResetResumenAdministrativo(apps, schema_editor):
    from admin_finanzas.models import ResumenAdministrativo, Movimiento, \
                                      DiaTrabajo, Banco, TipoCuenta, \
                                      TipoMovimiento
    ResumenAdministrativo.objects.all().delete()
    # Movimiento.objects.all().delete()
    DiaTrabajo.objects.all().delete()
    Banco.objects.all().delete()
    Banco.objects.bulk_create([
        Banco(
            nombre = "100% Banco",
        ),
        Banco(
            nombre = "Bancaribe",
        ),
        Banco(
            nombre = "Banco Bicentenario",
        ),
        Banco(
            nombre = "Banco Caroní",
        ),
        Banco(
            nombre = "Banco del Tesoro",
        ),
        Banco(
            nombre = "Banco de Venezuela",
        ),
        Banco(
            nombre = "Banco Exterior",
        ),
        Banco(
            nombre = "Banco Industrial de Venezuela",
        ),
        Banco(
            nombre = "Banco Mercantil",
        ),
        Banco(
            nombre = "Banco Nacional de Crédito - BNC",
        ),
        Banco(
            nombre = "Banco Occidental de Descuento - BOD",
        ),
        Banco(
            nombre = "Banco Plaza",
        ),
        Banco(
            nombre = "Banco Venezolano de Crédito",
        ),
        Banco(
            nombre = "Banesco",
        ),
        Banco(
            nombre = "Banplus",
        ),
        Banco(
            nombre = "BBVA Banco Provincial",
        ),
        Banco(
            nombre = "Efectivo",
        ),

    ])
    
    TipoCuenta.objects.all().delete()
    TipoCuenta.objects.bulk_create([
        TipoCuenta(
            nombre = "Cuenta Corriente",
            codigo = "C.C",
        ),
        TipoCuenta(
            nombre = "Cuenta de Ahorros",
            codigo = "C.A",
        ),
        TipoCuenta(
            nombre = "Cuenta Efectivo",
            codigo = "C.E",
        ),
    ])

    TipoMovimiento.objects.all().delete()
    TipoMovimiento.objects.bulk_create([
        TipoMovimiento(
            codename = "tipo_ajuste_cobrar",
            nombre = "Ajuste por Cobrar",
            description = "Para cobrar",
        ),
        TipoMovimiento(
            codename = "tipo_ajuste_pagar",
            nombre = "Ajuste por Pagar",
            description = "Para pagar",
        ),
        TipoMovimiento(
            codename = "tipo_deposito",
            nombre = "Depósito",
            description = "Para depositar",
        ),
        TipoMovimiento(
            codename = "tipo_pago",
            nombre = "Pago",
            description = "Para pagar",
        )
    ])

class Migration(migrations.Migration):

    dependencies = [
        ('admin_finanzas', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(ResetResumenAdministrativo),
        
        migrations.RemoveField(
            model_name='dimensioncomercializadora',
            name='pk_relate_ref',
        ),
        migrations.AlterModelOptions(
            name='banco',
            options={'verbose_name_plural': 'Bancos', 'ordering': ['nombre'], 'verbose_name': 'Banco'},
        ),
        migrations.AlterModelOptions(
            name='tipocuenta',
            options={'verbose_name_plural': 'Tipos de cuenta', 'ordering': ['nombre'], 'verbose_name': 'Tipo de cuenta'},
        ),
        migrations.AlterModelOptions(
            name='tipomovimiento',
            options={'verbose_name_plural': 'Tipos de movimientos', 'ordering': ['nombre'], 'verbose_name': 'Tipo de movimiento'},
        ),
        migrations.RemoveField(
            model_name='resumenadministrativo',
            name='comercializadora',
        ),
        migrations.DeleteModel(
            name='DimensionComercializadora',
        ),
        migrations.AlterField(
            model_name='banco',
            name='nombre',
            field=models.CharField(max_length=50, verbose_name='Nombre (*)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tipocuenta',
            name='codigo',
            field=models.CharField(max_length=10, verbose_name='Codigo (*)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tipocuenta',
            name='nombre',
            field=models.CharField(max_length=50, verbose_name='Nombre (*)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tipomovimiento',
            name='nombre',
            field=models.CharField(max_length=50, verbose_name='Nombre (*)'),
            preserve_default=True,
        ),
    ]

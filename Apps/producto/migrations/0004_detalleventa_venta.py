# Generated by Django 3.1.7 on 2021-04-13 04:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('producto', '0003_auto_20210410_1817'),
    ]

    operations = [
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_venta', models.DateTimeField(verbose_name='Fecha de Venta')),
                ('valor_total', models.IntegerField()),
                ('nombre', models.CharField(max_length=150)),
                ('apellido', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254)),
                ('direccion', models.CharField(max_length=350)),
                ('ciudad', models.CharField(max_length=50)),
                ('departamento', models.CharField(max_length=50)),
                ('celular', models.CharField(max_length=15)),
                ('forma_pago', models.CharField(choices=[('0', 'PSE'), ('1', 'MercadoPago')], max_length=2, verbose_name='TIPO PAGO')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Venta',
                'verbose_name_plural': 'Ventas',
            },
        ),
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('subtotal', models.IntegerField()),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='producto.producto')),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='producto.venta')),
            ],
            options={
                'verbose_name': 'Producto Vendido',
                'verbose_name_plural': 'Productos vendidos',
            },
        ),
    ]

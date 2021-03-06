# Generated by Django 3.1.7 on 2021-04-14 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0009_auto_20210414_1413'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Color',
                'verbose_name_plural': 'Colores',
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Size',
                'verbose_name_plural': 'Sizes',
            },
        ),
        migrations.CreateModel(
            name='Talla',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('talla', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Talla',
                'verbose_name_plural': 'Tallas',
            },
        ),
        migrations.AddField(
            model_name='detalleventa',
            name='info_extra',
            field=models.CharField(blank=True, default=' ', max_length=150),
        ),
        migrations.AddField(
            model_name='producto',
            name='color',
            field=models.ManyToManyField(blank=True, to='producto.Color'),
        ),
        migrations.AddField(
            model_name='producto',
            name='size',
            field=models.ManyToManyField(blank=True, to='producto.Size'),
        ),
        migrations.AddField(
            model_name='producto',
            name='talla',
            field=models.ManyToManyField(blank=True, to='producto.Talla'),
        ),
    ]

# Generated by Django 3.1.7 on 2021-04-17 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publicaciones', '0003_auto_20210416_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='mensaje',
            field=models.CharField(max_length=300, verbose_name='Mensaje'),
        ),
    ]

# Generated by Django 3.1.7 on 2021-04-18 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_servicio'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicio',
            name='resumen',
            field=models.CharField(default=' ', max_length=250),
        ),
    ]
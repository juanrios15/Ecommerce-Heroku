# Generated by Django 3.1.7 on 2021-04-10 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publicaciones', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicacion',
            name='slug',
            field=models.SlugField(default='', editable=False),
        ),
    ]

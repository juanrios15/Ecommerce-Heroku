# Generated by Django 3.1.7 on 2021-04-20 05:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('producto', '0016_fotoproducto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='size',
        ),
        migrations.AlterField(
            model_name='venta',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 5.1.2 on 2024-10-14 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0004_driver_latitude_driver_longitude_delete_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driver',
            name='email',
        ),
        migrations.RemoveField(
            model_name='driver',
            name='name',
        ),
    ]

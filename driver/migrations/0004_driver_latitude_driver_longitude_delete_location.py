# Generated by Django 5.1.2 on 2024-10-14 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0003_driver_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='driver',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Location',
        ),
    ]

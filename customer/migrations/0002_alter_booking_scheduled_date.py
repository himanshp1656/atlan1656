# Generated by Django 5.1.2 on 2024-10-14 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='scheduled_date',
            field=models.DateField(),
        ),
    ]
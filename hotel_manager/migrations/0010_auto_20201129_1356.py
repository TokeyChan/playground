# Generated by Django 3.1 on 2020-11-29 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_manager', '0009_auto_20201126_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room_key',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
# Generated by Django 3.1 on 2020-11-25 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_manager', '0004_token_is_valid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='value',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
# Generated by Django 4.2.16 on 2024-11-27 15:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('field_mgmt', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='field',
            name='area',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.0001, message='Area must be at least 0.0001 acres.')]),
        ),
    ]

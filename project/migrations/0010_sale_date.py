# Generated by Django 4.1.13 on 2024-03-26 03:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0009_delete_min'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]

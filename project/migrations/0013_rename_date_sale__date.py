# Generated by Django 4.1.13 on 2024-03-28 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0012_sale_items_sold'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sale',
            old_name='date',
            new_name='_date',
        ),
    ]

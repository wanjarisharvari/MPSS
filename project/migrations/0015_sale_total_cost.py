# Generated by Django 4.1.13 on 2024-04-13 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0014_rename__date_sale_sale_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='total_cost',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

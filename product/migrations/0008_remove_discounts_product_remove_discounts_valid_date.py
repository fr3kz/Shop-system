# Generated by Django 5.0.1 on 2024-02-07 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_discounts_valid_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discounts',
            name='product',
        ),
        migrations.RemoveField(
            model_name='discounts',
            name='valid_date',
        ),
    ]

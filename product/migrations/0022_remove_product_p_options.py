# Generated by Django 5.0.1 on 2024-02-24 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0021_product_p_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='p_options',
        ),
    ]
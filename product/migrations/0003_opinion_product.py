# Generated by Django 5.0.1 on 2024-01-13 00:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='opinion',
            name='product',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='product.product'),
        ),
    ]

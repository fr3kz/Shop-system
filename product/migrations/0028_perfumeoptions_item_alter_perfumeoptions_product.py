# Generated by Django 5.0.1 on 2024-02-27 12:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0027_carditem'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfumeoptions',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='perfume_item', to='product.carditem'),
        ),
        migrations.AlterField(
            model_name='perfumeoptions',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='perfume_options', to='product.product'),
        ),
    ]
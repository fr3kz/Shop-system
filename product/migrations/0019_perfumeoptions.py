# Generated by Django 5.0.1 on 2024-02-24 13:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0018_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='PerfumeOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=1)),
                ('price', models.IntegerField(default=0)),
                ('product', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
    ]

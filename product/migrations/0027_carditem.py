# Generated by Django 5.0.1 on 2024-02-27 11:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0026_delete_cartitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=1)),
                ('price', models.IntegerField(blank=True, default=0)),
                ('card', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='product.card')),
                ('product', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
    ]

# Generated by Django 5.0.1 on 2024-02-12 09:43

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_alter_card_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
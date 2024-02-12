# Generated by Django 5.0.1 on 2024-02-12 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_card_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='is_delivered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='card',
            name='is_shipped',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 5.0.1 on 2024-03-08 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0039_card_paczkomat'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='is_paczkomat',
            field=models.BooleanField(default=False),
        ),
    ]
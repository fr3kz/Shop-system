# Generated by Django 5.0.1 on 2024-03-08 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0041_alter_card_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='phone_number',
            field=models.IntegerField(blank=True, default=''),
        ),
    ]
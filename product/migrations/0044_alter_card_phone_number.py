# Generated by Django 5.0.1 on 2024-03-08 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0043_alter_card_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=9),
        ),
    ]
# Generated by Django 5.0.1 on 2024-02-12 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0016_card_is_done'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='is_done',
        ),
    ]

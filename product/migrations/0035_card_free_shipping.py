# Generated by Django 5.0.1 on 2024-03-05 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0034_perfumeoptions_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='free_shipping',
            field=models.BooleanField(default=False),
        ),
    ]

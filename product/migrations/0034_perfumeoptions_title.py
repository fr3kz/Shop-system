# Generated by Django 5.0.1 on 2024-03-03 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0033_carditem_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfumeoptions',
            name='title',
            field=models.CharField(default='', max_length=50),
        ),
    ]

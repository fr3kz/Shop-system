# Generated by Django 5.0.1 on 2024-03-16 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0044_alter_card_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
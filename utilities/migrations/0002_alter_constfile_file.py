# Generated by Django 5.0.1 on 2024-03-07 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='constfile',
            name='file',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
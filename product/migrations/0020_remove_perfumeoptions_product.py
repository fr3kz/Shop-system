# Generated by Django 5.0.1 on 2024-02-24 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0019_perfumeoptions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfumeoptions',
            name='product',
        ),
    ]
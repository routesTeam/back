# Generated by Django 3.2.8 on 2021-11-10 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_create_city_table'),
    ]

    operations = [
        migrations.RenameField(
            model_name='city',
            old_name='city_id',
            new_name='id',
        ),
    ]

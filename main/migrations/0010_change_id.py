# Generated by Django 3.2.8 on 2021-12-05 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_add_field_to_props_relation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citydebug',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
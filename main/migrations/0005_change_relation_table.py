# Generated by Django 3.2.8 on 2021-11-10 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_create_relation_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relation',
            name='first_city_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='first_city', to='main.city'),
        ),
        migrations.AlterField(
            model_name='relation',
            name='second_city_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='second_city', to='main.city'),
        ),
    ]

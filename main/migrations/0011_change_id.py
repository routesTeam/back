# Generated by Django 3.2.8 on 2021-12-05 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_change_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citydebug',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
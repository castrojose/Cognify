# Generated by Django 5.0 on 2024-11-12 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cognify', '0002_alter_simulation_date_run'),
    ]

    operations = [
        migrations.AddField(
            model_name='criminal',
            name='age',
            field=models.IntegerField(null=True),
        ),
    ]

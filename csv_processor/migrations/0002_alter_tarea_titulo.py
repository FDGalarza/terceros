# Generated by Django 5.1.7 on 2025-04-11 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csv_processor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarea',
            name='titulo',
            field=models.CharField(max_length=255),
        ),
    ]

# Generated by Django 3.2.9 on 2024-01-25 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20240125_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalhost',
            name='area',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='host',
            name='area',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]

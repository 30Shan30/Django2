# Generated by Django 3.2.9 on 2024-01-25 05:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20240125_0745'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalhost',
            name='last_seen',
        ),
        migrations.RemoveField(
            model_name='host',
            name='last_seen',
        ),
    ]

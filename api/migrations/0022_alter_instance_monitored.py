# Generated by Django 3.2.9 on 2024-01-26 02:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_alter_instance_monitored'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instance',
            name='monitored',
            field=models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, to='api.cmdbmonitored'),
        ),
    ]

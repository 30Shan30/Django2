# Generated by Django 3.2.9 on 2024-01-29 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_auto_20240128_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='db',
            name='modified_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='historicaldb',
            name='modified_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='historicalinstance',
            name='modified_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='instance',
            name='modified_at',
            field=models.DateTimeField(),
        ),
    ]

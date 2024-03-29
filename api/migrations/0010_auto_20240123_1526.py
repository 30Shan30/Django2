# Generated by Django 3.2.9 on 2024-01-23 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20240123_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='database_accountparameter',
            name='parameter',
            field=models.CharField(choices=[('base', (('max_sessions', 'max_sessions'), ('pw_lifetime', 'pw_lifetime'), ('pw_lifetime_justification', 'pw_lifetime_justification'), ('account_status', 'account_status'), ('expiry_date', 'expiry_date'), ('last_login', 'last_login'), ('ora_acc_type', 'ora_acc_type'), ('ora_profile', 'ora_profile'))), ('contact', (('informee', 'informee'), ('substitute', 'substitute'))), ('idms', (('last_error', 'last_error'),)), ('validation', (('last_validated', 'last_validated'), ('validate_action', 'validate_action'), ('validated_by', 'validated_by')))], max_length=90),
        ),
        migrations.AlterField(
            model_name='historicaldatabase_accountparameter',
            name='parameter',
            field=models.CharField(choices=[('base', (('max_sessions', 'max_sessions'), ('pw_lifetime', 'pw_lifetime'), ('pw_lifetime_justification', 'pw_lifetime_justification'), ('account_status', 'account_status'), ('expiry_date', 'expiry_date'), ('last_login', 'last_login'), ('ora_acc_type', 'ora_acc_type'), ('ora_profile', 'ora_profile'))), ('contact', (('informee', 'informee'), ('substitute', 'substitute'))), ('idms', (('last_error', 'last_error'),)), ('validation', (('last_validated', 'last_validated'), ('validate_action', 'validate_action'), ('validated_by', 'validated_by')))], max_length=90),
        ),
        migrations.AlterField(
            model_name='historicalinstance_accountparameter',
            name='parameter',
            field=models.CharField(choices=[('base', (('max_sessions', 'max_sessions'), ('pw_lifetime', 'pw_lifetime'), ('pw_lifetime_justification', 'pw_lifetime_justification'), ('account_status', 'account_status'), ('expiry_date', 'expiry_date'), ('last_login', 'last_login'), ('ora_acc_type', 'ora_acc_type'), ('ora_profile', 'ora_profile'))), ('contact', (('informee', 'informee'), ('substitute', 'substitute'))), ('idms', (('last_error', 'last_error'),)), ('validation', (('last_validated', 'last_validated'), ('validate_action', 'validate_action'), ('validated_by', 'validated_by')))], max_length=90),
        ),
        migrations.AlterField(
            model_name='instance_accountparameter',
            name='parameter',
            field=models.CharField(choices=[('base', (('max_sessions', 'max_sessions'), ('pw_lifetime', 'pw_lifetime'), ('pw_lifetime_justification', 'pw_lifetime_justification'), ('account_status', 'account_status'), ('expiry_date', 'expiry_date'), ('last_login', 'last_login'), ('ora_acc_type', 'ora_acc_type'), ('ora_profile', 'ora_profile'))), ('contact', (('informee', 'informee'), ('substitute', 'substitute'))), ('idms', (('last_error', 'last_error'),)), ('validation', (('last_validated', 'last_validated'), ('validate_action', 'validate_action'), ('validated_by', 'validated_by')))], max_length=90),
        ),
    ]

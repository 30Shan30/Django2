# Generated by Django 3.2.9 on 2024-01-22 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20240122_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalhostparameter',
            name='parameter',
            field=models.CharField(choices=[('cmdb', (('ci_name', 'ci_name'), ('ci_description', 'ci_description'), ('serial_number', 'serial_number'), ('additional_information', 'additional_information'), ('tag_list', 'tag_list'), ('child_dependency', 'child_dependency'), ('supported_by_relation', 'supported_by_relation'), ('used_by_relation', 'used_by_relation'), ('eva_dependency', 'eva_dependency'), ('model_version', 'model_version'), ('lastupdate', 'lastupdate'))), ('automation', (('backupshare', 'backupshare'), ('script_set_version', 'script_set_version'), ('boostfs', 'boostfs'), ('hostgroup', 'hostgroup'))), ('licenses', (('type', 'type'), ('edition', 'edition')))], max_length=80),
        ),
        migrations.AlterField(
            model_name='historicalhostparameter',
            name='parameter_section',
            field=models.CharField(choices=[('cmdb', 'cmdb'), ('automation', 'automation'), ('contact', 'contact'), ('config', 'config'), ('licenses', 'licenses')], max_length=40),
        ),
        migrations.AlterField(
            model_name='hostparameter',
            name='parameter',
            field=models.CharField(choices=[('cmdb', (('ci_name', 'ci_name'), ('ci_description', 'ci_description'), ('serial_number', 'serial_number'), ('additional_information', 'additional_information'), ('tag_list', 'tag_list'), ('child_dependency', 'child_dependency'), ('supported_by_relation', 'supported_by_relation'), ('used_by_relation', 'used_by_relation'), ('eva_dependency', 'eva_dependency'), ('model_version', 'model_version'), ('lastupdate', 'lastupdate'))), ('automation', (('backupshare', 'backupshare'), ('script_set_version', 'script_set_version'), ('boostfs', 'boostfs'), ('hostgroup', 'hostgroup'))), ('licenses', (('type', 'type'), ('edition', 'edition')))], max_length=80),
        ),
        migrations.AlterField(
            model_name='hostparameter',
            name='parameter_section',
            field=models.CharField(choices=[('cmdb', 'cmdb'), ('automation', 'automation'), ('contact', 'contact'), ('config', 'config'), ('licenses', 'licenses')], max_length=40),
        ),
    ]

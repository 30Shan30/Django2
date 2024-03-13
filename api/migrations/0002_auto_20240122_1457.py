# Generated by Django 3.2.9 on 2024-01-22 06:57

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instance',
            fields=[
                ('cmdbid', models.CharField(max_length=15, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator('^CMDB[0-9]{11}', 'invalid CMDB ID')])),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=125, null=True)),
                ('backup_medium', models.CharField(blank=True, max_length=125, null=True)),
                ('additional_information', models.CharField(blank=True, max_length=125, null=True)),
                ('ci_description', models.CharField(max_length=150, null=True)),
                ('ci_name', models.CharField(max_length=150, null=True)),
                ('model_version', models.CharField(blank=True, max_length=125, null=True)),
                ('serial_number', models.CharField(max_length=125, null=True)),
                ('last_seen', models.DateTimeField(blank=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('modified_by', models.CharField(max_length=50)),
                ('area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.cmdbarea')),
                ('fk_host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.host')),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.cmdbmanufacturer')),
                ('monitored', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.cmdbmonitored')),
                ('multipurpose', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='api.configmultipurpose')),
                ('primary_function', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.cmdbprimaryfunction')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.cmdbinstanceproduct')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.cmdbsite')),
                ('sox_relevance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.cmdbsox_relevance')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.cmdbstatus')),
                ('urgency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.cmdburgency')),
                ('usage_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.cmdbusage')),
            ],
        ),
        migrations.AlterField(
            model_name='historicalhostparameter',
            name='parameter',
            field=models.CharField(choices=[('cmdb', (('ci_name', 'ci_name'), ('ci_description', 'ci_description'), ('serial_number', 'serial_number'), ('additional_information', 'additional_information'), ('tag_list', 'tag_list'), ('child_dependency', 'child_dependency'), ('supported_by_relation', 'supported_by_relation'), ('used_by_relation', 'used_by_relation'), ('eva_dependency', 'eva_dependency'), ('model_version', 'model_version'), ('lastupdate', 'lastupdate'))), ('automation', (('backupshare', 'backupshare'), ('script_set_version', 'script_set_version'), ('boostfs', 'boostfs'), ('hostgroup', 'hostgroup'))), ('lic', (('type', 'type'), ('edition', 'edition')))], max_length=80),
        ),
        migrations.AlterField(
            model_name='historicalhostparameter',
            name='parameter_section',
            field=models.CharField(choices=[('cmdb', 'cmdb'), ('automation', 'automation'), ('contact', 'contact'), ('config', 'config')], max_length=40),
        ),
        migrations.AlterField(
            model_name='hostparameter',
            name='parameter',
            field=models.CharField(choices=[('cmdb', (('ci_name', 'ci_name'), ('ci_description', 'ci_description'), ('serial_number', 'serial_number'), ('additional_information', 'additional_information'), ('tag_list', 'tag_list'), ('child_dependency', 'child_dependency'), ('supported_by_relation', 'supported_by_relation'), ('used_by_relation', 'used_by_relation'), ('eva_dependency', 'eva_dependency'), ('model_version', 'model_version'), ('lastupdate', 'lastupdate'))), ('automation', (('backupshare', 'backupshare'), ('script_set_version', 'script_set_version'), ('boostfs', 'boostfs'), ('hostgroup', 'hostgroup'))), ('lic', (('type', 'type'), ('edition', 'edition')))], max_length=80),
        ),
        migrations.AlterField(
            model_name='hostparameter',
            name='parameter_section',
            field=models.CharField(choices=[('cmdb', 'cmdb'), ('automation', 'automation'), ('contact', 'contact'), ('config', 'config')], max_length=40),
        ),
        migrations.CreateModel(
            name='HistoricalInstanceParameter',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('parameter_section', models.CharField(choices=[('config', 'config'), ('contact', 'contact'), ('config', 'config')], max_length=40)),
                ('parameter', models.CharField(choices=[('config', (('appl', 'appl'), ('backup_type', 'backup_type'), ('backupshare', 'backupshare'), ('binlog_expire_logs_seconds', 'binlog_expire_logs_seconds'), ('binlog_backup', 'binlog_backup'), ('collation', 'collation'), ('expire_logs_days', 'expire_logs_days'), ('filerexport', 'filerexport'), ('filerpath', 'filerpath'), ('filerqtree', 'filerqtree'), ('filersize', 'filersize'), ('filervolume', 'filervolume'), ('fstype', 'fstype'), ('innodb_buffer_pool_instances', 'innodb_buffer_pool_instances'), ('innodb_buffer_pool_size', 'innodb_buffer_pool_size'), ('pkg', 'pkg'), ('pkgmount', 'pkgmount'), ('port', 'port'), ('product', 'product'), ('protection_class', 'protection_class'), ('secure_file_priv', 'secure_file_priv'), ('server_id', 'server_id'), ('site_short', 'site_short'), ('urgency', 'urgency'), ('usage_type', 'usage_type'), ('vserver', 'vserver'), ('wsrep_provider', 'wsrep_provider'), ('local_infile', 'local_infile'), ('max_connections', 'max_connections'), ('max_user_connections', 'max_user_connections'), ('mount_option', 'mount_option'), ('address_alias', 'address_alias'), ('role', 'role'), ('standby_parent_cmdbid', 'standby_parent_cmdbid'))), ('cmdb', (('child_dependency', 'child_dependency'), ('currentWorkflowID', 'currentWorkflowID'), ('eva_dependency', 'eva_dependency'), ('lastCRQ', 'lastCRQ'), ('lastupdate', 'lastupdate'), ('supported_by_relation', 'supported_by_relation'), ('tag_list', 'tag_list'), ('used_by_relation', 'used_by_relation'))), ('contact', (('responsible', 'responsible'), ('script_set_version', 'script_set_version'), ('max_user_connections', 'max_user_connections'), ('hostgroup', 'hostgroup')))], max_length=80)),
                ('parameter_index', models.IntegerField()),
                ('value', models.CharField(max_length=200, null=True)),
                ('modified_at', models.DateTimeField(blank=True, editable=False)),
                ('modified_by', models.CharField(max_length=50)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('fk', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='api.instance')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical instance parameter',
                'verbose_name_plural': 'historical instance parameters',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalInstance',
            fields=[
                ('cmdbid', models.CharField(db_index=True, max_length=15, validators=[django.core.validators.RegexValidator('^CMDB[0-9]{11}', 'invalid CMDB ID')])),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=125, null=True)),
                ('backup_medium', models.CharField(blank=True, max_length=125, null=True)),
                ('additional_information', models.CharField(blank=True, max_length=125, null=True)),
                ('ci_description', models.CharField(max_length=150, null=True)),
                ('ci_name', models.CharField(max_length=150, null=True)),
                ('model_version', models.CharField(blank=True, max_length=125, null=True)),
                ('serial_number', models.CharField(max_length=125, null=True)),
                ('last_seen', models.DateTimeField(blank=True, null=True)),
                ('modified_at', models.DateTimeField(blank=True, editable=False)),
                ('modified_by', models.CharField(max_length=50)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('area', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='api.cmdbarea')),
                ('fk_host', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='api.host')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('manufacturer', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='api.cmdbmanufacturer')),
                ('monitored', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='api.cmdbmonitored')),
                ('multipurpose', models.ForeignKey(blank=True, db_constraint=False, default=0, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='api.configmultipurpose')),
                ('primary_function', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='api.cmdbprimaryfunction')),
                ('product', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='api.cmdbinstanceproduct')),
                ('site', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='api.cmdbsite')),
                ('sox_relevance', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='api.cmdbsox_relevance')),
                ('status', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='api.cmdbstatus')),
                ('urgency', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='api.cmdburgency')),
                ('usage_type', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='api.cmdbusage')),
            ],
            options={
                'verbose_name': 'historical instance',
                'verbose_name_plural': 'historical instances',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='InstanceParameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parameter_section', models.CharField(choices=[('config', 'config'), ('contact', 'contact'), ('config', 'config')], max_length=40)),
                ('parameter', models.CharField(choices=[('config', (('appl', 'appl'), ('backup_type', 'backup_type'), ('backupshare', 'backupshare'), ('binlog_expire_logs_seconds', 'binlog_expire_logs_seconds'), ('binlog_backup', 'binlog_backup'), ('collation', 'collation'), ('expire_logs_days', 'expire_logs_days'), ('filerexport', 'filerexport'), ('filerpath', 'filerpath'), ('filerqtree', 'filerqtree'), ('filersize', 'filersize'), ('filervolume', 'filervolume'), ('fstype', 'fstype'), ('innodb_buffer_pool_instances', 'innodb_buffer_pool_instances'), ('innodb_buffer_pool_size', 'innodb_buffer_pool_size'), ('pkg', 'pkg'), ('pkgmount', 'pkgmount'), ('port', 'port'), ('product', 'product'), ('protection_class', 'protection_class'), ('secure_file_priv', 'secure_file_priv'), ('server_id', 'server_id'), ('site_short', 'site_short'), ('urgency', 'urgency'), ('usage_type', 'usage_type'), ('vserver', 'vserver'), ('wsrep_provider', 'wsrep_provider'), ('local_infile', 'local_infile'), ('max_connections', 'max_connections'), ('max_user_connections', 'max_user_connections'), ('mount_option', 'mount_option'), ('address_alias', 'address_alias'), ('role', 'role'), ('standby_parent_cmdbid', 'standby_parent_cmdbid'))), ('cmdb', (('child_dependency', 'child_dependency'), ('currentWorkflowID', 'currentWorkflowID'), ('eva_dependency', 'eva_dependency'), ('lastCRQ', 'lastCRQ'), ('lastupdate', 'lastupdate'), ('supported_by_relation', 'supported_by_relation'), ('tag_list', 'tag_list'), ('used_by_relation', 'used_by_relation'))), ('contact', (('responsible', 'responsible'), ('script_set_version', 'script_set_version'), ('max_user_connections', 'max_user_connections'), ('hostgroup', 'hostgroup')))], max_length=80)),
                ('parameter_index', models.IntegerField()),
                ('value', models.CharField(max_length=200, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('modified_by', models.CharField(max_length=50)),
                ('fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.instance')),
            ],
            options={
                'unique_together': {('fk', 'parameter_section', 'parameter', 'parameter_index')},
            },
        ),
    ]
# Generated by Django 3.2.9 on 2024-01-22 07:25

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0003_auto_20240122_1513'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instance_account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('accounttype', models.CharField(max_length=20, null=True)),
                ('created_date', models.DateTimeField()),
                ('last_seen', models.DateTimeField(blank=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(max_length=20, null=True)),
                ('owner', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^IF[0-9]{8}', 'invalid Global ID')])),
                ('accountid', models.CharField(max_length=20, null=True)),
                ('fk_instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.instance')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalInstance_accountParameter',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('parameter_section', models.CharField(choices=[('base', 'base'), ('contact', 'contact'), ('idms', 'idms'), ('validation', 'validation')], max_length=40)),
                ('parameter', models.CharField(choices=[('base', (('max_sessions', 'max_sessions'), ('pw_lifetime', 'pw_lifetime'), ('pw_lifetime_justification', 'pw_lifetime_justification'), ('account_status', 'account_status'), ('expiry_date', 'expiry_date'), ('last_login', 'last_login'), ('ora_acc_type', 'ora_acc_type'), ('ora_profile', 'ora_profile'))), ('contact', (('informee', 'informee'), ('substitute', 'substitute'))), ('idms', (('last_error', 'last_error'),)), ('validation', (('responsible', 'responsible'), ('script_set_version', 'script_set_version'), ('max_user_connections', 'max_user_connections'), ('hostgroup', 'hostgroup')))], max_length=90)),
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
                'verbose_name': 'historical instance_account parameter',
                'verbose_name_plural': 'historical instance_account parameters',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalInstance_account',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('accounttype', models.CharField(max_length=20, null=True)),
                ('created_date', models.DateTimeField()),
                ('last_seen', models.DateTimeField(blank=True, null=True)),
                ('modified_at', models.DateTimeField(blank=True, editable=False)),
                ('status', models.CharField(max_length=20, null=True)),
                ('owner', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^IF[0-9]{8}', 'invalid Global ID')])),
                ('accountid', models.CharField(max_length=20, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('fk_instance', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='api.instance')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical instance_account',
                'verbose_name_plural': 'historical instance_accounts',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Instance_accountParameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parameter_section', models.CharField(choices=[('base', 'base'), ('contact', 'contact'), ('idms', 'idms'), ('validation', 'validation')], max_length=40)),
                ('parameter', models.CharField(choices=[('base', (('max_sessions', 'max_sessions'), ('pw_lifetime', 'pw_lifetime'), ('pw_lifetime_justification', 'pw_lifetime_justification'), ('account_status', 'account_status'), ('expiry_date', 'expiry_date'), ('last_login', 'last_login'), ('ora_acc_type', 'ora_acc_type'), ('ora_profile', 'ora_profile'))), ('contact', (('informee', 'informee'), ('substitute', 'substitute'))), ('idms', (('last_error', 'last_error'),)), ('validation', (('responsible', 'responsible'), ('script_set_version', 'script_set_version'), ('max_user_connections', 'max_user_connections'), ('hostgroup', 'hostgroup')))], max_length=90)),
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

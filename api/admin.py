from django.contrib import admin
from .models import *
#Host,HostParameter,Instance,InstanceParameter,Instance_account,Instance_accountParameter,Db,DbParameter,Database_account,Database_accountParameter
from simple_history.admin import SimpleHistoryAdmin

glb_attributefields = ['fk','parameter_section','parameter','parameter_index','value','modified_at','modified_by']
glb_entityHostfields = ['cmdbid','name','product','manufacturer','site','area','status','usage_type','urgency','primary_function','monitored','sox_relevance','dns','domain','ip_address','owner','modified_at','modified_by']
glb_entityInstancefields = ['cmdbid','name','product','address','backup_medium','multipurpose','additional_information','area','ci_description','ci_name','manufacturer','model_version','monitored','primary_function','serial_number','site','sox_relevance','status','urgency','usage_type','last_seen','fk_host','modified_at','modified_by']
glb_entityInstance_accfields = ['fk_instance','name','accounttype','created_date','last_seen','status','owner','accountid','modified_at','modified_by']
glb_entityInstance_accParamfields = ['fk','parameter_section','parameter','parameter_index','value','modified_at','modified_by']

glb_entityDbfields = ['cmdbid','name','protection_class','area','ci_description','ci_name','manufacturer','model_version','monitored','primary_function','product','serial_number','site','status','urgency','usage_type','owner','fk_instance','modified_at','modified_by']
glb_entityDb_accfields = ['fk_database','name','accounttype','created_date','last_seen','status','owner','accountid','modified_at','modified_by']
glb_entityDb_accParamfields = ['fk','parameter_section','parameter','parameter_index','value','modified_at','modified_by']


# Register your models here.
# @admin.register(CMDBInstanceProduct)
# class CMDBInstanceProductAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in CMDBInstanceProduct._meta.fields]
#     search_fields = ['name']
#     list_filter = search_fields


@admin.register(Host)
class HostAdmin(SimpleHistoryAdmin):
    list_display = [field.name for field in Host._meta.fields]
    history_list_display = glb_entityHostfields
    search_fields = ['cmdbid','name','product','manufacturer','site','area','status','usage_type','urgency','primary_function','monitored','sox_relevance','dns','domain','ip_address','owner','last_seen']
    list_filter = search_fields

@admin.register(HostParameter)
class HostParameterAdmin(SimpleHistoryAdmin):
    list_display = [field.name for field in HostParameter._meta.fields]
    history_list_display = glb_attributefields
    search_fields = ['fk','parameter_section','parameter','parameter_index','value']
    list_filter = search_fields

@admin.register(Instance)
class InstanceAdmin(SimpleHistoryAdmin):
    list_display = [field.name for field in Instance._meta.fields]
    history_list_display = glb_entityInstancefields
    search_fields = ['cmdbid','name','product','address','backup_medium','multipurpose','additional_information','area','ci_description','ci_name','manufacturer','model_version','monitored','primary_function','serial_number','site','sox_relevance','status','urgency','usage_type','last_seen','fk_host']
    list_filter = search_fields
    
@admin.register(InstanceParameter)
class InstanceParameterAdmin(SimpleHistoryAdmin):
    list_display = [field.name for field in InstanceParameter._meta.fields]
    search_fields = ['fk','parameter_section','parameter','parameter_index','value']
    list_filter = search_fields
    history_list_display = glb_attributefields

@admin.register(Instance_account)
class Instance_accountAdmin(SimpleHistoryAdmin):
    list_display = [field.name for field in Instance_account._meta.fields]
    history_list_display = glb_entityInstance_accfields
    search_fields = ['fk_instance','name','accounttype','created_date','last_seen','status','owner','accountid']
    list_filter = search_fields
    
    
@admin.register(Instance_accountParameter)
class Instance_accountParameterAdmin(SimpleHistoryAdmin):
    list_display = [field.name for field in Instance_accountParameter._meta.fields]
    search_fields = ['fk','parameter_section','parameter','parameter_index','value']
    list_filter = search_fields
    history_list_display = glb_entityInstance_accParamfields

    
@admin.register(Db)
class DbAdmin(SimpleHistoryAdmin):
    list_display = [field.name for field in Db._meta.fields]
    search_fields = ['cmdbid','name','protection_class','area','ci_description','ci_name','manufacturer','model_version','monitored','primary_function','product','serial_number','site','status','urgency','usage_type','owner','fk_instance']
    list_filter = search_fields
    history_list_display = glb_entityDbfields

@admin.register(DbParameter)
class DbParameterAdmin(SimpleHistoryAdmin):
    list_display = [field.name for field in DbParameter._meta.fields]
    search_fields = ['fk','parameter_section','parameter','parameter_index','value']
    list_filter = search_fields
    history_list_display = glb_entityDbfields

@admin.register(Database_account)
class Database_accountAdmin(SimpleHistoryAdmin):
    list_display = [field.name for field in Database_account._meta.fields]
    history_list_display = glb_entityDb_accfields
    search_fields = ['fk_database','name','accounttype','created_date','last_seen','status','owner','accountid']
    list_filter = search_fields
    
@admin.register(Database_accountParameter)
class Database_accountParameterAdmin(SimpleHistoryAdmin):
    list_display = [field.name for field in Database_accountParameter._meta.fields]
    search_fields = ['fk','parameter_section','parameter','parameter_index','value']
    list_filter = search_fields
    history_list_display = glb_entityDb_accParamfields

@admin.register(OraTablespace)
class OraTablespaceAdmin(SimpleHistoryAdmin):
    list_display = ['cmdbid','db_account','tablespace_name','tablespace_size','modified_at','modified_by']
    history_list_display = ['cmdbid','db_account','tablespace_name','tablespace_size','modified_at','modified_by']
    search_fields = ['cmdbid','db_account','tablespace_name','tablespace_size']
    list_filter = search_fields

# @admin.register(Account)
# class AccountAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in Account._meta.fields]
#     search_fields = ['id']
#     list_filter = ['id']

# @admin.register(AccountParameter)
# class AccountParameterAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in AccountParameter._meta.fields]
#     search_fields = ['parameter_section','parameter']
#     list_filter = search_fields
from django.db import models
from django.core.validators import RegexValidator
from simple_history.models import HistoricalRecords
from django.utils.timezone import now

## Create Static models :

#class CMDBHostProduct(models.Models):

class CMDBHostProduct(models.Model):
    name = models.CharField(primary_key=True, max_length=50)

    def __str__(self):
        return self.name
    
class CMDBStatus(models.Model):
    name = models.CharField(primary_key=True, max_length=50)

    def __str__(self):
        return self.name    
    
class CMDBUsage(models.Model):
    name = models.CharField(primary_key=True, max_length=50)

    def __str__(self):
        return self.name      
    
class CMDBUrgency(models.Model):
    name = models.CharField(primary_key=True, max_length=50)

    def __str__(self):
        return self.name

class CMDBPrimaryfunction(models.Model):
    name = models.CharField(primary_key=True, max_length=50)

    def __str__(self):
        return self.name        
    
class CMDBManufacturer(models.Model):
    name = models.CharField(primary_key=True, max_length=50)

    def __str__(self):
        return self.name      

class CMDBSite(models.Model):
    name = models.CharField(primary_key=True, max_length=50)

    def __str__(self):
        return self.name

class CMDBMonitored(models.Model):
    name = models.CharField(primary_key=True, max_length=50)

    def __str__(self):
        return self.name     

class CMDBInstanceProduct(models.Model):
    name = models.CharField(primary_key=True, max_length=50)

    def __str__(self):
        return self.name

class ConfigMultipurpose(models.Model):
    name = models.IntegerField(primary_key=True)

    def __str__(self):
        return self.name

class CMDBDatabaseProduct(models.Model):
    name = models.CharField(primary_key=True, max_length=50)

    def __str__(self):
        return self.name

# Create your models here.
class Host(models.Model):
    # Microsoft_Cluster_Instance = "Microsoft Cluster Instance"
    # PRODUCT_CHOICES = [(Microsoft_Cluster_Instance,'Microsoft Cluster Instance')]
    cmdbid            = models.CharField(primary_key=True, max_length=15, validators=[RegexValidator('^CMDB[0-9]{11}','invalid CMDB ID')])
    name              = models.CharField(max_length=80) ## by default blank=False, null=False
    product           = models.ForeignKey(CMDBHostProduct, on_delete=models.CASCADE) ###models.CharField(max_length=50, choices=PRODUCT_CHOICES) #product           = models.CharField(max_length=50, choices=PRODUCT_CHOICES)
    manufacturer      = models.ForeignKey(CMDBManufacturer, on_delete=models.CASCADE)
    site              = models.ForeignKey(CMDBSite, on_delete=models.CASCADE)
    area              = models.CharField(max_length=15, null=True,blank=True)
    status            = models.ForeignKey(CMDBStatus, on_delete=models.CASCADE)
    usage_type        = models.ForeignKey(CMDBUsage, on_delete=models.CASCADE)
    urgency           = models.ForeignKey(CMDBUrgency, on_delete=models.CASCADE)
    primary_function  = models.ForeignKey(CMDBPrimaryfunction, on_delete=models.CASCADE)
    monitored         = models.ForeignKey(CMDBMonitored, on_delete=models.CASCADE, default= False)
    sox_relevance     = models.CharField(max_length=20, null=True,blank=True)
    dns               = models.CharField(max_length=100)
    domain            = models.CharField(max_length=30)
    ip_address        = models.GenericIPAddressField()
    owner             = models.CharField(max_length=10, validators=[RegexValidator('^IF[0-9]{8}','invalid Global ID')])
    last_seen         = models.DateTimeField(null=True, blank=True)  
    modified_at       = models.DateTimeField()
    modified_by       = models.CharField(max_length=50)
    history = HistoricalRecords()

    def __str__(self):
        return self.cmdbid
     
class HostParameter(models.Model):
    cmdb ='cmdb'
    config='config'
    licenses = 'licenses'

    PARAMETER_SECTION_CHOICES=[(cmdb,'cmdb'),(config,'config'),(licenses,'licenses')]
    PARAMETER_CHOICES = [('cmdb', (('ci_name', 'ci_name'),('ci_description', 'ci_description'),('serial_number', 'serial_number'),('additional_information', 'additional_information'),
                                   ('tag_list', 'tag_list'),('child_dependency', 'child_dependency'),('supported_by_relation', 'supported_by_relation'),('used_by_relation', 'used_by_relation'),
                                   ('eva_dependency', 'eva_dependency'),('model_version', 'model_version'),('lastupdate', 'lastupdate'))),
                    ('config', (('backupshare', 'backupshare'),('script_set_version', 'script_set_version'),('boostfs', 'boostfs'),('hostgroup', 'hostgroup'))),  
                    ('licenses', (('type', 'type'),('edition', 'edition'))),
                    ]

    fk                = models.ForeignKey(Host, on_delete=models.CASCADE)
    parameter_section = models.CharField(max_length=40, choices=PARAMETER_SECTION_CHOICES)
    parameter         = models.CharField(max_length=80, choices=PARAMETER_CHOICES)
    parameter_index   = models.IntegerField()
    value             = models.CharField(max_length=200, null=True)
    modified_at       = models.DateTimeField(auto_now=True)
    modified_by       = models.CharField(max_length=50)
    history = HistoricalRecords()

    class Meta:
        unique_together = [('fk', 'parameter_section', 'parameter', 'parameter_index')]

    # def __str__(self):
    #     return self.id

class Instance(models.Model):

    cmdbid                  = models.CharField(primary_key=True, max_length=15, validators=[RegexValidator('^CMDB[0-9]{11}','invalid CMDB ID')])
    name                    = models.CharField(max_length=100) ## by default blank=False, null=False
    product                 = models.ForeignKey(CMDBInstanceProduct, on_delete=models.CASCADE) 
    address                 = models.CharField(max_length=125, null=True,blank=True)
    backup_medium           = models.CharField(max_length=125, null=True,blank=True)
    multipurpose            = models.ForeignKey(ConfigMultipurpose, on_delete=models.CASCADE, default=0) 
    additional_information  = models.CharField(max_length=125, null=True,blank=True)
    area                    = models.CharField(max_length=15, null=True,blank=True)
    ci_description          = models.CharField(max_length=150)
    ci_name                 = models.CharField(max_length=150)
    manufacturer            = models.ForeignKey(CMDBManufacturer, on_delete=models.CASCADE)
    model_version           = models.CharField(max_length=125, null=True,blank=True)
    monitored               = models.ForeignKey(CMDBMonitored, on_delete=models.CASCADE,default=False)
    primary_function        = models.ForeignKey(CMDBPrimaryfunction, on_delete=models.CASCADE)
    serial_number           = models.CharField(max_length=125)
    site                    = models.ForeignKey(CMDBSite, on_delete=models.CASCADE)
    sox_relevance           = models.CharField(max_length=20, null=True,blank=True)
    status                  = models.ForeignKey(CMDBStatus, on_delete=models.CASCADE)
    urgency                 = models.ForeignKey(CMDBUrgency, on_delete=models.CASCADE)
    usage_type              = models.ForeignKey(CMDBUsage, on_delete=models.CASCADE)
    last_seen               = models.DateTimeField(null=True,blank=True)
    modified_at             = models.DateTimeField()
    modified_by             = models.CharField(max_length=50)
    fk_host                 = models.ForeignKey(Host, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return self.cmdbid 

class InstanceParameter(models.Model):

    config ='config'
    contact ='contact'
    cmdb='cmdb'

    PARAMETER_SECTION_CHOICES=[(config,'config'),(contact, 'contact'),(cmdb,'cmdb')]
    PARAMETER_CHOICES = [('config', (('appl', 'appl'),('backup_type', 'backup_type'),('backupshare', 'backupshare'),('binlog_expire_logs_seconds', 'binlog_expire_logs_seconds'),('binlog_backup', 'binlog_backup'),('collation', 'collation'),
                                   ('expire_logs_days', 'expire_logs_days'),('filerexport', 'filerexport'),('filerpath', 'filerpath'),('filerqtree', 'filerqtree'),
                                   ('filersize', 'filersize'),('filervolume', 'filervolume'),('fstype', 'fstype'),('innodb_buffer_pool_instances', 'innodb_buffer_pool_instances'),('innodb_buffer_pool_size', 'innodb_buffer_pool_size'),
                                   ('pkg', 'pkg'),('pkgmount', 'pkgmount'),('port', 'port'),('product', 'product'),('protection_class', 'protection_class'),('secure_file_priv', 'secure_file_priv'),('server_id', 'server_id'),
                                   ('site_short', 'site_short'),('urgency', 'urgency'),('usage_type', 'usage_type'),('vserver', 'vserver'),('wsrep_provider', 'wsrep_provider'),
                                   ('local_infile', 'local_infile'),('max_connections', 'max_connections'),('max_user_connections', 'max_user_connections'),('mount_option', 'mount_option'),('address_alias', 'address_alias'),
                                   ('role', 'role'),('standby_parent_cmdbid', 'standby_parent_cmdbid'))),
                    ('cmdb', (('child_dependency', 'child_dependency'),('currentWorkflowID', 'currentWorkflowID'),('eva_dependency', 'eva_dependency'),('lastCRQ', 'lastCRQ'),('lastupdate', 'lastupdate'),
                              ('supported_by_relation', 'supported_by_relation'),('tag_list', 'tag_list'),('used_by_relation', 'used_by_relation'))), 
                    ('contact', (('responsible', 'responsible'),('script_set_version', 'script_set_version'),('max_user_connections', 'max_user_connections'),('hostgroup', 'hostgroup')))]

    fk                = models.ForeignKey(Instance, on_delete=models.CASCADE)
    parameter_section = models.CharField(max_length=40 , choices=PARAMETER_SECTION_CHOICES)
    parameter         = models.CharField(max_length=80, choices=PARAMETER_CHOICES)
    parameter_index   = models.IntegerField()
    value             = models.CharField(max_length=200, null=True)
    modified_at       = models.DateTimeField(auto_now=True)
    modified_by       = models.CharField(max_length=50)
    history = HistoricalRecords()

    class Meta:
        unique_together = [('fk', 'parameter_section', 'parameter', 'parameter_index')]

    # def __str__(self):
    #     return self.fk

class Instance_account(models.Model): 
    fk_instance         = models.ForeignKey(Instance, on_delete=models.CASCADE)
    name                = models.CharField(max_length=200)
    accounttype         = models.CharField(max_length=20, null=True)
    created_date        = models.DateTimeField()
    last_seen           = models.DateTimeField(null=True,blank=True)
    modified_at         = models.DateTimeField()
    status              = models.CharField(max_length=20, null=True)
    owner               = models.CharField(max_length=10, validators=[RegexValidator('^IF[0-9]{8}','invalid Global ID')])  
    accountid           = models.CharField(max_length=20, null=True,blank=True)  
    modified_by         = models.CharField(max_length=50)
    history = HistoricalRecords()    

    # def __str__(self):
    #     return self.fk_instance  

class Instance_accountParameter(models.Model):
    base ='base'
    contact='contact'
    idms = 'idms'
    validation = 'validation'

    PARAMETER_SECTION_CHOICES=[(base, 'base'),(contact,'contact'),(idms,'idms'),(validation,'validation')]
    PARAMETER_CHOICES = [('base', (('max_sessions', 'max_sessions'),('pw_lifetime', 'pw_lifetime'),('pw_lifetime_justification', 'pw_lifetime_justification'),('account_status', 'account_status'),('expiry_date', 'expiry_date'),('last_login', 'last_login'),
                                   ('ora_acc_type', 'ora_acc_type'),('ora_profile', 'ora_profile'))),
                        ('contact', (('informee', 'informee'),('substitute', 'substitute'))),
                        ('idms', (('last_error', 'last_error'),)),
                        ('validation', (('last_validated', 'last_validated'),('validate_action', 'validate_action'),('validated_by', 'validated_by')))]

    fk                = models.ForeignKey(Instance, on_delete=models.CASCADE)
    parameter_section = models.CharField(max_length=40, choices=PARAMETER_SECTION_CHOICES)
    parameter         = models.CharField(max_length=90, choices=PARAMETER_CHOICES)
    parameter_index   = models.IntegerField()
    value             = models.CharField(max_length=200, null=True)
    modified_at       = models.DateTimeField(auto_now=True)
    modified_by       = models.CharField(max_length=50)
    history = HistoricalRecords()

    class Meta:
        unique_together = [('fk', 'parameter_section', 'parameter', 'parameter_index')]


class Db(models.Model):
    cmdbid                  = models.CharField(primary_key=True, max_length=15, validators=[RegexValidator('^CMDB[0-9]{11}','invalid CMDB ID')])
    name                    = models.CharField(max_length=200)
    protection_class        = models.CharField(max_length=25, null=True, blank=True)
    created_date            = models.DateTimeField()
    area                    = models.CharField(max_length=15, null=True,blank=True)
    ci_description          = models.CharField(max_length=150)
    ci_name                 = models.CharField(max_length=150)
    last_seen               = models.DateTimeField(null=True,blank=True)
    manufacturer            = models.ForeignKey(CMDBManufacturer, on_delete=models.CASCADE)
    model_version           = models.CharField(max_length=125, null=True,blank=True)
    monitored               = models.ForeignKey(CMDBMonitored, on_delete=models.CASCADE,null=True)
    primary_function        = models.ForeignKey(CMDBPrimaryfunction, on_delete=models.CASCADE)
    product                 = models.ForeignKey(CMDBDatabaseProduct, on_delete=models.CASCADE)
    serial_number           = models.CharField(max_length=125)
    site                    = models.ForeignKey(CMDBSite, on_delete=models.CASCADE) 
    status                  = models.ForeignKey(CMDBStatus, on_delete=models.CASCADE)
    urgency                 = models.ForeignKey(CMDBUrgency, on_delete=models.CASCADE)
    usage_type              = models.ForeignKey(CMDBUsage, on_delete=models.CASCADE)
    owner                   = models.CharField(max_length=10, validators=[RegexValidator('^IF[0-9]{8}','invalid Global ID')])  
    modified_at             = models.DateTimeField()
    modified_by             = models.CharField(max_length=50)
    fk_instance             = models.ForeignKey(Instance, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return self.cmdbid 
    #def __str__(self):
    #    return self.name+" @ "+self.fk_instance.name

class DbParameter(models.Model):

    base = 'base'
    cmdb = 'cmdb'
    contact = 'contact'
    config = 'config'
    validation = 'validation'

    PARAMETER_SECTION_CHOICES=[(base, 'base'),(cmdb, 'cmdb'),(contact,'contact'),(config,'config'),(validation,'validation')]
    PARAMETER_CHOICES = [('config', (('characterset', 'characterset'),('collation', 'collation'),('protection_class', 'protection_class'),('size_requested', 'size_requested'),('status', 'status'),
                                   ('ora_acc_type', 'ora_acc_type'),('ora_profile', 'ora_profile'))),
                        ('base', (('created_date', 'created_date'),)),
                        ('cmdb', (('additional_information', 'additional_information'),('child_dependency', 'child_dependency'),('currentWorkflowID', 'currentWorkflowID'),
                        ('eva_dependency', 'eva_dependency'),('lastCRQ', 'lastCRQ'),('last_cmdbupdate', 'last_cmdbupdate'),('sox_relevance', 'sox_relevance'),('supported_by_relation', 'supported_by_relation'),
                        ('tag_list', 'tag_list'),('used_by_relation', 'used_by_relation'))),
                        ('contact', (('informee,' 'informee'),('substitute','substitute'))),
                        ('validation', (('last_validated,' 'last_validated'),('validate_action,' 'validate_action'),('validated_by,' 'validated_by'),('validation_action,' 'validation_action'),('validation_crq,' 'validation_crq')))]
    

    fk                = models.ForeignKey(Db, on_delete=models.CASCADE)
    parameter_section = models.CharField(max_length=40)
    parameter         = models.CharField(max_length=80)
    parameter_index   = models.IntegerField()
    value             = models.CharField(max_length=200, null=True)
    modified_at       = models.DateTimeField(auto_now=True)
    modified_by       = models.CharField(max_length=50)
    history = HistoricalRecords()

    class Meta:
        unique_together = [('fk', 'parameter_section', 'parameter', 'parameter_index')]
    # def __str__(self):
    #     return self.fk    
        
class Database_account(models.Model): 
    fk_database         = models.ForeignKey(Db, on_delete=models.CASCADE)
    name                = models.CharField(max_length=200)
    accounttype         = models.CharField(max_length=20, null=True)
    created_date        = models.DateTimeField()
    last_seen           = models.DateTimeField(null=True,blank=True)
    modified_at         = models.DateTimeField()
    status              = models.CharField(max_length=20, null=True)
    owner               = models.CharField(max_length=10, validators=[RegexValidator('^IF[0-9]{8}','invalid Global ID')])  
    accountid           = models.CharField(max_length=20, null=True,blank=True)  
    modified_by         = models.CharField(max_length=50)
    history = HistoricalRecords()    

    def __str__(self):
        return self.fk_database  

class Database_accountParameter(models.Model):
    base ='base'
    contact='contact'
    idms = 'idms'
    validation = 'validation'

    PARAMETER_SECTION_CHOICES=[(base, 'base'),(contact,'contact'),(idms,'idms'),(validation,'validation')]
    PARAMETER_CHOICES = [('base', (('max_sessions', 'max_sessions'),('pw_lifetime', 'pw_lifetime'),('pw_lifetime_justification', 'pw_lifetime_justification'),('account_status', 'account_status'),('expiry_date', 'expiry_date'),('last_login', 'last_login'),
                                   ('ora_acc_type', 'ora_acc_type'),('ora_profile', 'ora_profile'))),
                        ('contact', (('informee', 'informee'),('substitute', 'substitute'))),
                        ('idms', (('last_error', 'last_error'),)),
                        ('validation', (('last_validated', 'last_validated'),('validate_action', 'validate_action'),('validated_by', 'validated_by')))]

    fk                = models.ForeignKey(Db, on_delete=models.CASCADE)
    parameter_section = models.CharField(max_length=40, choices=PARAMETER_SECTION_CHOICES)
    parameter         = models.CharField(max_length=90, choices=PARAMETER_CHOICES)
    parameter_index   = models.IntegerField()
    value             = models.CharField(max_length=200, null=True)
    modified_at       = models.DateTimeField(auto_now=True)
    modified_by       = models.CharField(max_length=50)
    history = HistoricalRecords()

    class Meta:
        unique_together = [('fk', 'parameter_section', 'parameter', 'parameter_index')]

###### Oracle tablespace ######

class OraTablespace(models.Model):
    cmdbid          = models.ForeignKey(Instance,on_delete=models.CASCADE, max_length=15, validators=[RegexValidator('^CMDB[0-9]{11}','invalid CMDB ID')])
    db_account      = models.CharField(max_length=200)
    tablespace_name = models.CharField(max_length=200)
    tablespace_size = models.BigIntegerField()
    modified_at     = models.DateTimeField(auto_now=True)
    modified_by     = models.CharField(max_length=50)
    history = HistoricalRecords()

    def __str__(self):
        return self.cmdbid 

# class Account(models.Model):
#     id                = models.CharField(primary_key=True, max_length=15, validators=[RegexValidator('^AC[0-9]{10}','invalid AC ID')])
#     name              = models.CharField(max_length=200)
#     modified_at       = models.DateTimeField()
#     modified_by       = models.CharField(max_length=50)
#     fk_db             = models.ForeignKey(Db, on_delete=models.CASCADE)
#     history = HistoricalRecords()

#     def __str__(self):
#         return self.id 

# class AccountParameter(models.Model):
#     fk                = models.ForeignKey(Account, on_delete=models.CASCADE)
#     parameter_section = models.CharField(max_length=40)
#     parameter         = models.CharField(max_length=80)
#     parameter_index   = models.IntegerField()
#     value             = models.CharField(max_length=200, null=True)
#     modified_at       = models.DateTimeField()
#     modified_by       = models.CharField( max_length=50)
#     history = HistoricalRecords()

    # def __str__(self):
    #     return self.fk 
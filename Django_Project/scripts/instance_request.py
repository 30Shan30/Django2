import os
import subprocess
from api.models import *
from django.core.exceptions import ValidationError
from api.serializers import *

import re

def instance_request(data,in_executer,in_datetime):
    for item in data:
        fkhost = Host.objects.get(cmdbid=item['fk_host'])
        print (fkhost)
        if Instance.objects.filter(cmdbid=item['cmdbid']).exists():
            if not Instance.objects.filter(cmdbid=item['cmdbid'],name = item['name'],product = item['product'],address = item['address'],backup_medium = item['backup_medium'],multipurpose = item['multipurpose'],additional_information = item['additional_information'],area = item['area'],ci_description = item['ci_description'],ci_name = item['ci_name'],manufacturer = item['manufacturer'],model_version = item['model_version'],monitored = item['monitored'],primary_function = item['primary_function'],serial_number = item['serial_number'],site = item['site'],sox_relevance = item['sox_relevance'],status = item['status'],usage_type = item['usage_type'],urgency = item['urgency'],fk_host = fkhost).exists():
                #print (Instance.objects.filter(cmdbid=item['cmdbid'],name = item['name'],product = item['product'],address = item['address'],backup_medium = item['backup_medium'],multipurpose = item['multipurpose'],additional_information = item['additional_information'],area = item['area'],ci_description = item['ci_description'],ci_name = item['ci_name'],manufacturer = item['manufacturer'],model_version = item['model_version'],monitored = item['monitored']).exists())
                instanceid = Instance.objects.get(pk=item['cmdbid'])
                #print (instanceid)
                serializer = InstanceSerializer(instanceid, data={"cmdbid":item['cmdbid'],"name": item['name'],"product": item['product'],"address": item['address'],"backup_medium": item['backup_medium'],"multipurpose": item['multipurpose'],"additional_information": item['additional_information'],"area": item['area'],"ci_description": item['ci_description'],"ci_name": item['ci_name'],"manufacturer": item['manufacturer'],"model_version": item['model_version'],"monitored" : item['monitored'],"primary_function" : item['primary_function'],"serial_number" : item['serial_number'],"site": item['site'],"sox_relevance" : item['sox_relevance'],"status": item['status'],"usage_type": item['usage_type'],"urgency": item['urgency'],"last_seen": item['last_seen'],"modified_at":in_datetime,"modified_by": in_executer,"fk_host": fkhost})
                #print (serializer)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    print('Object instance entity update')
                else:
                    print("Not valid update ") 
            else: 
                instanceid = Instance.objects.get(pk=item['cmdbid'])
                modifydate = Instance.objects.get(pk=item['cmdbid']).modified_at
                serializer = InstanceSerializer(instanceid, data={"cmdbid":item['cmdbid'],"name": item['name'],"product": item['product'],"address": item['address'],"backup_medium": item['backup_medium'],"multipurpose": item['multipurpose'],"additional_information": item['additional_information'],"area": item['area'],"ci_description": item['ci_description'],"ci_name": item['ci_name'],"manufacturer": item['manufacturer'],"model_version": item['model_version'],"monitored" : item['monitored'],"primary_function" : item['primary_function'],"serial_number" : item['serial_number'],"site": item['site'],"sox_relevance" : item['sox_relevance'],"status": item['status'],"usage_type": item['usage_type'],"urgency": item['urgency'],"last_seen": item['last_seen'],"modified_at":modifydate,"modified_by": in_executer,"fk_host": fkhost})
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    print('Object instance else entity update last seen')
                else:
                    print("Not valid update ")
        else:
            serializer = InstanceSerializer(data={"cmdbid":item['cmdbid'],"name": item['name'],"product": item['product'],"address": item['address'],"backup_medium": item['backup_medium'],"multipurpose": item['multipurpose'],"additional_information": item['additional_information'],"area": item['area'],"ci_description": item['ci_description'],"ci_name": item['ci_name'],"manufacturer": item['manufacturer'],"model_version": item['model_version'],"monitored" : item['monitored'],"primary_function" : item['primary_function'],"serial_number" : item['serial_number'],"site": item['site'],"sox_relevance" : item['sox_relevance'],"status": item['status'],"usage_type": item['usage_type'],"urgency": item['urgency'],"last_seen": item['last_seen'],"modified_at":in_datetime,"modified_by": in_executer,"fk_host": fkhost})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            else: 
                print("Not valid insert")             
        r = Instance.objects.get(cmdbid=item['cmdbid'])
        if 'cmdb' in item:
            for key, value in (item['cmdb'].items()):
                    for i in range(len(value)):
                        if key in ['child_dependency','currentWorkflowID','eva_dependency','lastCRQ','tag_list','supported_by_relation','used_by_relation','eva_dependency']:
                            if InstanceParameter.objects.filter(fk=r,parameter_section='cmdb',parameter=key).exists():
                                if InstanceParameter.objects.filter(fk=r,parameter_section='cmdb',parameter=key,parameter_index=i).exists():
                                    if not InstanceParameter.objects.filter(fk=r,parameter_section='cmdb',parameter=key,parameter_index=i,value=value[i]).exists():
                                        queryset= InstanceParameter.objects.filter(fk=r,parameter_section='cmdb',parameter=key,parameter_index=i).values()
                                        for obj in queryset:
                                            update = InstanceParameter.objects.get(pk=obj['id'])
                                            update.value = value[i]
                                            update.modified_at = in_datetime
                                            update.modified_by = in_executer
                                            update.save()
                                        print('Object cmdb attribute update') 
                                    else: 
                                        print('Skip cmdb attribute')
                                else: 
                                    InstanceParameter.objects.create(fk=r, parameter_section='cmdb',parameter=key, parameter_index=i,value=value[i],modified_at=in_datetime,modified_by=in_executer)
                            else:        
                                InstanceParameter.objects.create(fk=r, parameter_section='cmdb',parameter=key, parameter_index=i,value=value[i],modified_at=in_datetime,modified_by=in_executer)
                                print('Object cmdb attribute insert')
                        else:
                            raise ValidationError("Invalid parameter as '"+key+"' in cmdb group")
        if 'contact' in item:    
        #if item['contact']:
            for key, value in (item['contact'].items()):
                    for i in range(len(value)):
                        if key in ['responsible']:
                            if InstanceParameter.objects.filter(fk=r,parameter_section='contact',parameter=key).exists():
                                if InstanceParameter.objects.filter(fk=r,parameter_section='contact',parameter=key,parameter_index=i).exists():
                                    if not InstanceParameter.objects.filter(fk=r,parameter_section='contact',parameter=key,parameter_index=i,value=value[i]).exists():
                                        queryset= InstanceParameter.objects.filter(fk=r,parameter_section='contact',parameter=key,parameter_index=i).values()
                                        for obj in queryset:
                                            update = InstanceParameter.objects.get(pk=obj['id'])
                                            update.value = value[i]
                                            update.modified_at = in_datetime
                                            update.modified_by = in_executer
                                            update.save()
                                        print('Object contact attribute update') 
                                    else: 
                                        print('Skip contact attribute')
                                else: 
                                    InstanceParameter.objects.create(fk=r, parameter_section='contact',parameter=key, parameter_index=i,value=value[i],modified_at=in_datetime,modified_by=in_executer)
                            else:        
                                InstanceParameter.objects.create(fk=r, parameter_section='contact',parameter=key, parameter_index=i,value=value[i],modified_at=in_datetime,modified_by=in_executer)
                                print('Object contact attribute insert')
                        else:
                            raise ValidationError("Invalid parameter as '"+key+"' in contact group")
        if 'config' in item:    
            for key, value in (item['config'].items()):
                    for i in range(len(value)):
                        if key in ['appl','backupshare','backup_type','binlog_expire_logs_seconds','binlog_backup','collation','expire_logs_days','filerexport','filerpath','filerqtree','filersize','filervolume','fstype','innodb_buffer_pool_instances','innodb_buffer_pool_size','pkg','pkgmount','port','product','protection_class','secure_file_priv','server_id','site_short','urgency','usage_type','vserver','wsrep_provider','local_infile','max_connections','max_user_connections','mount_option','address_alias','role','standby_parent_cmdbid']:
                            if InstanceParameter.objects.filter(fk=r,parameter_section='config',parameter=key).exists():
                                if InstanceParameter.objects.filter(fk=r,parameter_section='config',parameter=key,parameter_index=i).exists():
                                    if not InstanceParameter.objects.filter(fk=r,parameter_section='config',parameter=key,parameter_index=i,value=value[i]).exists():
                                        queryset= InstanceParameter.objects.filter(fk=r,parameter_section='contact',parameter=key,parameter_index=i).values()
                                        for obj in queryset:
                                            update = InstanceParameter.objects.get(pk=obj['id'])
                                            update.value = value[i]
                                            update.modified_at = in_datetime
                                            update.modified_by = in_executer
                                            update.save()
                                        print('Object config attribute update') 
                                    else: 
                                        print('Skip config attribute')
                                else: 
                                    InstanceParameter.objects.create(fk=r, parameter_section='config',parameter=key, parameter_index=i,value=value[i],modified_at=in_datetime,modified_by=in_executer)
                            else:        
                                InstanceParameter.objects.create(fk=r, parameter_section='config',parameter=key, parameter_index=i,value=value[i],modified_at=in_datetime,modified_by=in_executer)
                                print('Object config attribute insert')
                        else:
                            raise ValidationError("Invalid parameter as '"+key+"' in config group")                        
    return True   
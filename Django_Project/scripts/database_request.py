import os
import subprocess
from api.models import *
from django.core.exceptions import ValidationError
from api.serializers import *

import re

def database_request(data,in_executer,in_datetime):
    for item in data:
        fkinstance = Instance.objects.get(cmdbid=item['fk_instance'])
        print (fkinstance)
        if Db.objects.filter(cmdbid=item['cmdbid']).exists():
            if not Db.objects.filter(cmdbid=item['cmdbid'],name = item['name'],protection_class = item['protection_class'],created_date = item['created_date'],area = item['area'],ci_description = item['ci_description'],ci_name = item['ci_name'],manufacturer = item['manufacturer'],model_version = item['model_version'],monitored = item['monitored'],primary_function = item['primary_function'],product = item['product'],serial_number = item['serial_number'],site = item['site'],status = item['status'],usage_type = item['usage_type'],urgency = item['urgency'],owner = item['owner'],fk_instance = fkinstance).exists():
                instanceid = Db.objects.get(pk=item['cmdbid'])
                serializer = DbSerializer(instanceid, data={"cmdbid":item['cmdbid'],"name": item['name'],"protection_class": item['protection_class'],"created_date": item['created_date'],"area": item['area'],"ci_description": item['ci_description'],"ci_name": item['ci_name'],"last_seen": item['last_seen'],"manufacturer": item['manufacturer'],"model_version": item['model_version'],"monitored": item['monitored'],"primary_function": item['primary_function'],"product": item['product'],"serial_number" : item['serial_number'],"site": item['site'],"status": item['status'],"usage_type": item['usage_type'],"urgency": item['urgency'],"owner" : item['owner'],"last_seen": item['last_seen'],"modified_at":in_datetime,"modified_by": in_executer,"fk_instance": fkinstance})
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    print('Object instance entity update')
                else:
                    print("Not valid update ") 
            else: 
                print('Skip instance entity')
                instanceid = Db.objects.get(pk=item['cmdbid'])
                modifydate = Db.objects.get(pk=item['cmdbid']).modified_at
                serializer = DbSerializer(instanceid, data={"cmdbid":item['cmdbid'],"name": item['name'],"protection_class": item['protection_class'],"created_date": item['created_date'],"area": item['area'],"ci_description": item['ci_description'],"ci_name": item['ci_name'],"manufacturer": item['manufacturer'],"model_version": item['model_version'],"monitored": item['monitored'],"primary_function": item['primary_function'],"product": item['product'],"serial_number" : item['serial_number'],"site": item['site'],"status": item['status'],"usage_type": item['usage_type'],"urgency": item['urgency'],"owner" : item['owner'],"last_seen": item['last_seen'],"modified_at":modifydate,"modified_by": in_executer,"fk_instance": fkinstance})
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    print('Object instance else entity update')
                else:
                    print("Not valid update ")  
        else:
            serializer = DbSerializer(data={"cmdbid":item['cmdbid'],"name": item['name'],"protection_class": item['protection_class'],"created_date": item['created_date'],"area": item['area'],"ci_description": item['ci_description'],"ci_name": item['ci_name'],"last_seen": item['last_seen'],"manufacturer": item['manufacturer'],"model_version": item['model_version'],"monitored": item['monitored'],"primary_function": item['primary_function'],"product": item['product'],"serial_number" : item['serial_number'],"site": item['site'],"status": item['status'],"usage_type": item['usage_type'],"urgency": item['urgency'],"owner" : item['owner'],"last_seen": item['last_seen'],"modified_at":in_datetime,"modified_by": in_executer,"fk_instance": fkinstance})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            else: 
                print("Not valid insert")             
        r = Db.objects.get(cmdbid=item['cmdbid'])
        if 'cmdb' in item:
            for key, value in (item['cmdb'].items()):
                    for i in range(len(value)):
                        if key in ['additional_information','child_dependency','currentWorkflowID','eva_dependency','lastCRQ','last_cmdbupdate','sox_relevance','supported_by_relation','tag_list','used_by_relation']:
                            if DbParameter.objects.filter(fk=r,parameter_section='cmdb',parameter=key).exists():
                                if DbParameter.objects.filter(fk=r,parameter_section='cmdb',parameter=key,parameter_index=i).exists():
                                    if not DbParameter.objects.filter(fk=r,parameter_section='cmdb',parameter=key,parameter_index=i,value=value[i]).exists():
                                        queryset= DbParameter.objects.filter(fk=r,parameter_section='cmdb',parameter=key,parameter_index=i).values()
                                        for obj in queryset:
                                            update = DbParameter.objects.get(pk=obj['id'])
                                            update.value = value[i]
                                            update.modified_at = in_datetime
                                            update.modified_by = in_executer
                                            update.save()
                                        print('Object cmdb attribute update') 
                                    else: 
                                        print('Skip cmdb attribute')
                                else: 
                                    DbParameter.objects.create(fk=r, parameter_section='cmdb',parameter=key, parameter_index=i,value=value[i],modified_at=in_datetime,modified_by=in_executer)
                            else:        
                                DbParameter.objects.create(fk=r, parameter_section='cmdb',parameter=key, parameter_index=i,value=value[i],modified_at=in_datetime,modified_by=in_executer)
                                print('Object cmdb attribute insert')
                        else:
                            raise ValidationError("Invalid parameter as '"+key+"' in cmdb group")
        if 'contact' in item:    
        #if item['contact']:
            for key, value in (item['contact'].items()):
                    for i in range(len(value)):
                        if key in ['informee','substitute']:
                            if DbParameter.objects.filter(fk=r,parameter_section='contact',parameter=key).exists():
                                if DbParameter.objects.filter(fk=r,parameter_section='contact',parameter=key,parameter_index=i).exists():
                                    if not DbParameter.objects.filter(fk=r,parameter_section='contact',parameter=key,parameter_index=i,value=value[i]).exists():
                                        queryset= DbParameter.objects.filter(fk=r,parameter_section='contact',parameter=key,parameter_index=i).values()
                                        for obj in queryset:
                                            update = DbParameter.objects.get(pk=obj['id'])
                                            update.value = value[i]
                                            update.modified_at = in_datetime
                                            update.modified_by = in_executer
                                            update.save()
                                        print('Object contact attribute update') 
                                    else: 
                                        print('Skip contact attribute')
                                else: 
                                    DbParameter.objects.create(fk=r, parameter_section='contact',parameter=key, parameter_index=i,value=value[i],modified_at=in_datetime,modified_by=in_executer)
                            else:        
                                DbParameter.objects.create(fk=r, parameter_section='contact',parameter=key, parameter_index=i,value=value[i],modified_at=in_datetime,modified_by=in_executer)
                                print('Object contact attribute insert')
                        else:
                            raise ValidationError("Invalid parameter as '"+key+"' in contact group")
        if 'config' in item:    
            for key, value in (item['config'].items()):
                    for i in range(len(value)):
                        if key in ['characterset','collation','protection_class','size_requested','status','collation','ora_acc_type','ora_profile']:
                            if DbParameter.objects.filter(fk=r,parameter_section='config',parameter=key).exists():
                                if DbParameter.objects.filter(fk=r,parameter_section='config',parameter=key,parameter_index=i).exists():
                                    if not DbParameter.objects.filter(fk=r,parameter_section='config',parameter=key,parameter_index=i,value=value[i]).exists():
                                        queryset= DbParameter.objects.filter(fk=r,parameter_section='contact',parameter=key,parameter_index=i).values()
                                        for obj in queryset:
                                            update = DbParameter.objects.get(pk=obj['id'])
                                            update.value = value[i]
                                            update.modified_at = in_datetime
                                            update.modified_by = in_executer
                                            update.save()
                                        print('Object config attribute update') 
                                    else: 
                                        print('Skip config attribute')
                                else: 
                                    DbParameter.objects.create(fk=r, parameter_section='config',parameter=key, parameter_index=i,value=value[i],modified_at=in_datetime,modified_by=in_executer)
                            else:        
                                DbParameter.objects.create(fk=r, parameter_section='config',parameter=key, parameter_index=i,value=value[i],modified_at=in_datetime,modified_by=in_executer)
                                print('Object config attribute insert')
                        else:
                            raise ValidationError("Invalid parameter as '"+key+"' in config group")
        if 'base' in item:    
            for key, value in (item['base'].items()):
                    for i in range(len(value)):
                        if key in ['created_date']:
                            if DbParameter.objects.filter(fk=r,parameter_section='base',parameter=key).exists():
                                if DbParameter.objects.filter(fk=r,parameter_section='base',parameter=key,parameter_index=i).exists():
                                    if not DbParameter.objects.filter(fk=r,parameter_section='base',parameter=key,parameter_index=i,value=value[i]).exists():
                                        queryset= DbParameter.objects.filter(fk=r,parameter_section='base',parameter=key,parameter_index=i).values()
                                        for obj in queryset:
                                            update = DbParameter.objects.get(pk=obj['id'])
                                            update.value = value[i]
                                            update.modified_at = in_datetime
                                            update.modified_by = in_executer
                                            update.save()
                                        print('Object base attribute update') 
                                    else: 
                                        print('Skip base attribute')
                                else: 
                                    DbParameter.objects.create(fk=r, parameter_section='base',parameter=key, parameter_index=i,value=value[i],modified_at=in_datetime,modified_by=in_executer)
                            else:        
                                DbParameter.objects.create(fk=r, parameter_section='base',parameter=key, parameter_index=i,value=value[i],modified_at=in_datetime,modified_by=in_executer)
                                print('Object base attribute insert')
                        else:
                            raise ValidationError("Invalid parameter as '"+key+"' in base group")                                              
    return True   
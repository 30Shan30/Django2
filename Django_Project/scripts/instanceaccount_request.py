import os
import subprocess
from api.models import *
from django.core.exceptions import ValidationError
from api.serializers import *
#from datetime 
from datetime import datetime, timedelta 

import re

def instanceaccount_request(data,in_executer,in_datetime):
    for item in data:
        fkinstance = Instance.objects.get(cmdbid=item['fk_instance'])
        print (fkinstance)
        if Instance_account.objects.filter(fk_instance=item['fk_instance'],name=item['name']).exists():
            if not Instance_account.objects.filter(name = item['name'],accounttype = item['accounttype'],created_date = item['created_date'],status = item['status'],owner = item['owner'],accountid = item['accountid'],fk_instance = fkinstance).exists():
                #instanceid = Instance_account.objects.get(pk=item['cmdbid'])
                queryset= Instance_account.objects.filter(fk_instance=item['fk_instance'],name=item['name']).values()
                print (queryset)
                for obj in queryset:                 
                    update = Instance_account.objects.get(pk=obj['id'])
                    update.name         = item['name']
                    update.accounttype  = item['accounttype']
                    update.created_date = item['created_date']
                    update.last_seen    = item['last_seen']
                    update.status       = item['status']
                    update.owner        = item['owner']
                    update.accountid    = item['accountid']
                    update.fk_instance  = fkinstance
                    update.modified_at  = in_datetime
                    update.modified_by  = in_executer
                    update.save()
            else: 
                print('Skip instance entity')
                modifydate = Instance_account.objects.get(fk_instance=item['fk_instance'],name=item['name']).modified_at
                
                #print (modifydate.year'-'modifydate.month'-',modifydate.day,' ',modifydate.hour,':',modifydate.minute,':',modifydate.second)
                queryset= Instance_account.objects.filter(fk_instance=item['fk_instance'],name=item['name']).values()
                for obj in queryset:
                    update = Instance_account.objects.get(pk=obj['id'])
                    update.name         = item['name']
                    update.accounttype  = item['accounttype']
                    update.created_date = item['created_date']
                    update.last_seen    = item['last_seen']
                    update.status       = item['status']
                    update.owner        = item['owner']
                    update.accountid    = item['accountid']
                    update.fk_instance  = fkinstance
                    update.modified_at  = modifydate
                    update.modified_by  = in_executer
                    update.save()
        else:
            serializer = Instance_accountSerializer(data={"fk_instance":item['fk_instance'],"name": item['name'],"accounttype": item['accounttype'],"created_date": item['created_date'],"last_seen": item['last_seen'],"status": item['status'],"owner": item['owner'],"accountid": item['accountid'],"modified_at": in_datetime,"modified_by": in_executer})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            else: 
                print("Not valid insert")             
        r = Instance.objects.get(cmdbid=item['fk_instance'])
        if 'base' in item:
            for key, value in (item['base'].items()):
                    for i in range(len(value)):
                        if key in ['max_sessions','pw_lifetime','pw_lifetime_justification','account_status','expiry_date','last_login','ora_acc_type','ora_profile']:
                            if Instance_accountParameter.objects.filter(fk=r,parameter_section='base',parameter=key).exists():
                                if Instance_accountParameter.objects.filter(fk=r,parameter_section='base',parameter=key,parameter_index=i).exists():
                                    if not Instance_accountParameter.objects.filter(fk=r,parameter_section='base',parameter=key,parameter_index=i,value=value[i]).exists():
                                        queryset= Instance_accountParameter.objects.filter(fk=r,parameter_section='base',parameter=key,parameter_index=i).values()
                                        for obj in queryset:
                                            update = Instance_accountParameter.objects.get(pk=obj['id'])
                                            update.value = value[i]
                                            update.modified_at = in_datetime
                                            update.modified_by = in_executer
                                            update.save()
                                        print('Object base attribute update') 
                                    else: 
                                        print('Skip base attribute')
                                else: 
                                    Instance_accountParameter.objects.create(fk=r, parameter_section='base',parameter=key, parameter_index=i,value=value[i],modified_at=in_datetime,modified_by=in_executer)
                            else:        
                                Instance_accountParameter.objects.create(fk=r, parameter_section='base',parameter=key, parameter_index=i,value=value[i],modified_at=in_datetime,modified_by=in_executer)
                                print('Object base attribute insert')
                        else:
                            raise ValidationError("Invalid parameter as '"+key+"' in base group")
        if 'contact' in item:    
        #if item['contact']:
            for key, value in (item['contact'].items()):
                    for i in range(len(value)):
                        if key in ['informee','substitute']:
                            if Instance_accountParameter.objects.filter(fk=r,parameter_section='contact',parameter=key).exists():
                                if Instance_accountParameter.objects.filter(fk=r,parameter_section='contact',parameter=key,parameter_index=i).exists():
                                    if not Instance_accountParameter.objects.filter(fk=r,parameter_section='contact',parameter=key,parameter_index=i,value=value[i]).exists():
                                        queryset= Instance_accountParameter.objects.filter(fk=r,parameter_section='contact',parameter=key,parameter_index=i).values()
                                        for obj in queryset:
                                            update = Instance_accountParameter.objects.get(pk=obj['id'])
                                            update.value = value[i]
                                            update.modified_at = in_datetime
                                            update.modified_by = in_executer
                                            update.save()
                                        print('Object contact attribute update') 
                                    else: 
                                        print('Skip contact attribute')
                                else: 
                                    Instance_accountParameter.objects.create(fk=r, parameter_section='contact',parameter=key, parameter_index=i,value=value[i],modified_at=in_datetime,modified_by=in_executer)
                            else:        
                                Instance_accountParameter.objects.create(fk=r, parameter_section='contact',parameter=key, parameter_index=i,value=value[i],modified_at=in_datetime,modified_by=in_executer)
                                print('Object contact attribute insert')
                        else:
                            raise ValidationError("Invalid parameter as '"+key+"' in contact group")
        if 'idms' in item:    
            for key, value in (item['idms'].items()):
                    for i in range(len(value)):
                        if key in ['last_error']:
                            if Instance_accountParameter.objects.filter(fk=r,parameter_section='idms',parameter=key).exists():
                                if Instance_accountParameter.objects.filter(fk=r,parameter_section='idms',parameter=key,parameter_index=i).exists():
                                    if not Instance_accountParameter.objects.filter(fk=r,parameter_section='idms',parameter=key,parameter_index=i,value=value[i]).exists():
                                        queryset= Instance_accountParameter.objects.filter(fk=r,parameter_section='idms',parameter=key,parameter_index=i).values()
                                        for obj in queryset:
                                            update = Instance_accountParameter.objects.get(pk=obj['id'])
                                            update.value = value[i]
                                            update.modified_at = in_datetime
                                            update.modified_by = in_executer
                                            update.save()
                                        print('Object idms attribute update') 
                                    else: 
                                        print('Skip idms attribute')
                                else: 
                                    Instance_accountParameter.objects.create(fk=r, parameter_section='idms',parameter=key, parameter_index=i,value=value[i],modified_at=in_datetime,modified_by=in_executer)
                            else:        
                                Instance_accountParameter.objects.create(fk=r, parameter_section='idms',parameter=key, parameter_index=i,value=value[i],modified_at=in_datetime,modified_by=in_executer)
                                print('Object idms attribute insert')
                        else:
                            raise ValidationError("Invalid parameter as '"+key+"' in idms group")                        
    return True   
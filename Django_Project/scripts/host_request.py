import os
import subprocess
from api.models import *
from django.core.exceptions import ValidationError

from api.serializers import *



import re

### i would like to know before insert/update into host and hostparameter table , i would like to check the data exist or not 
# if data exists 
## Modified_at (only there is changes and insert new entry will be django auto defined date and time )
##FIRST json request trigger at Dec. 12, 2023, 3 a.m.
# {
#     "rawdata": [
#         {
#             "cmdbid": "CMDB32489720670",
#             "name": "MKZSQLT99",
#             "product": "testproduct"
#             "cmdb": {
#                 "ci_name":          ["first_test_trigger"],
#                 "serial_number":    ["MKZSQLT99_Isecure"]
#             }
#         }
#     ]
# }


    #first check data exist if not insert  into host table

    # CMDBID            NAME        PRODUCT         MODIFIED AT             MODIFIED BY
    # CMDB32489720670	MKZSQLT99	testproduct	    Dec. 12, 2023, 3 a.m.	shan


    #first  check data exist if not insert hostparameter table
    # ID    FK                  PARAMETER_SECTION   PARAMETER           PARAMETER_INDEX     VALUE               MODIFIED_AT             MODIFIED BY
    # 129	CMDB32489720670	    cmdb                serial_number	    0	                MKZSQLT99_Isecure	Dec. 12, 2023, 3 a.m.	shan
    # 128	CMDB32489720670	    cmdb	            ci_name             0	                first_test_trigger	Dec. 12, 2023, 3 a.m.	shan
    ######


##Second request trigger at Dec. 15, 2023, 8 a.m.
# {
#     "rawdata": [
#         {
#             "cmdbid": "CMDB32489720670",
#             "name": "MKZSQLT99",
#             "product": "testproduct"
#             "cmdb": {
#                 "ci_name":          ["first_test_trigger"],
#                 "serial_number":    ["MKZSQLT99_IsecureTest"],
#                 "child_dependency": ["CMDB0987654321","CMDB1233465688"]
#             }
#         }
#     ]
# }

    ## second request: check there is same value given by request never update modified_at because there is no update in host table skip update.

        # CMDBID            NAME        PRODUCT         MODIFIED AT             MODIFIED BY
        # CMDB32489720670	MKZSQLT99	testproduct	    Dec. 12, 2023, 3 a.m.	shan


        #second request : update hostparameter table (only update value has been change for MKZSQLT99_IsecureTest where CMDB32489720670,cmdb,serial_number )
        ## insert new entry child_dependency data not exist at all 

        # ID    FK                  PARAMETER_SECTION   PARAMETER           PARAMETER_INDEX     VALUE                   MODIFIED_AT             MODIFIED BY
        # 129	CMDB32489720670	    cmdb                serial_number	    0	                MKZSQLT99_IsecureTest	Dec. 15, 2023, 8 a.m.	shan
        # 128	CMDB32489720670	    cmdb	            ci_name             0	                first_test_trigger	    Dec. 12, 2023, 3 a.m.	shan
        # 130	CMDB32489720670	    cmdb	            child_dependency    0	                CMDB0987654321	        Dec. 15, 2023, 8 a.m.	shan       
        # 131	CMDB32489720670	    cmdb	            child_dependency    1	                CMDB1233465688	        Dec. 15, 2023, 8 a.m.	shan                
        ######

def host_request(data,in_executer,in_datetime):
    for item in data:
        if Host.objects.filter(cmdbid=item['cmdbid']).exists():
            #print (Host.objects.filter(cmdbid=item['cmdbid']).exists())
            if not Host.objects.filter(cmdbid=item['cmdbid'],name = item['name'],product = item['product'],manufacturer = item['manufacturer'],site = item['site'],area = item['area'],status = item['status'],usage_type = item['usage_type'],urgency = item['urgency'],primary_function = item['primary_function'],monitored = item['monitored'],sox_relevance = item['sox_relevance'],dns = item['dns'],domain = item['domain'],ip_address = item['ip_address'],owner = item['owner']).exists():
                #print (Host.objects.filter(cmdbid=item['cmdbid'],name = item['name'],product = item['product'],manufacturer = item['manufacturer'],site = item['site']).exists())
                #print (Host.objects.filter(cmdbid=item['cmdbid'],area = item['area'],status = item['status'],usage_type = item['usage_type'],urgency = item['urgency'],primary_function = item['primary_function']).exists())
                #print (Host.objects.filter(cmdbid=item['cmdbid'],monitored = item['monitored'],sox_relevance = item['sox_relevance']).exists())
                hostid = Host.objects.get(pk=item['cmdbid'])
                serializer = HostSerializer(hostid, data={"cmdbid":item['cmdbid'],"name": item['name'],"product": item['product'],"manufacturer": item['manufacturer'],"site": item['site'],"area": item['area'],"status": item['status'],"usage_type": item['usage_type'],"urgency": item['urgency'],"primary_function": item['primary_function'],"monitored": item['monitored'],"sox_relevance": item['sox_relevance'],"dns": item['dns'],"domain": item['domain'],"ip_address": item['ip_address'],"owner": item['owner'],"last_seen": item['last_seen'],"modified_at": in_datetime,"modified_by": in_executer})
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    print('Object host entity update')
                else:
                    print("Not valid update ")
            else:
                hostid = Host.objects.get(pk=item['cmdbid'])
                modifydate = Host.objects.get(pk=item['cmdbid']).modified_at
                #print (modifydate)
                serializer = HostSerializer(hostid, data={"cmdbid":item['cmdbid'],"name": item['name'],"product": item['product'],"manufacturer": item['manufacturer'],"site": item['site'],"area": item['area'],"status": item['status'],"usage_type": item['usage_type'],"urgency": item['urgency'],"primary_function": item['primary_function'],"monitored": item['monitored'],"sox_relevance": item['sox_relevance'],"dns": item['dns'],"domain": item['domain'],"ip_address": item['ip_address'],"owner": item['owner'],"last_seen": item['last_seen'],"modified_at": modifydate,"modified_by": in_executer})
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    print('Object host else entity update')
                else:
                    print("Not valid update ") 
        else:
            serializer = HostSerializer(data={"cmdbid":item['cmdbid'],"name": item['name'],"product": item['product'],"manufacturer": item['manufacturer'],"area": item['area'],"site": item['site'],"status": item['status'],"usage_type": item['usage_type'],"urgency": item['urgency'],"primary_function": item['primary_function'],"monitored": item['monitored'],"sox_relevance": item['sox_relevance'],"dns": item['dns'],"domain": item['domain'],"ip_address": item['ip_address'],"owner": item['owner'],"last_seen": item['last_seen'],"modified_at": in_datetime,"modified_by": in_executer})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            else: 
                print("Not valid insert")                   
        r = Host.objects.get(cmdbid=item['cmdbid'])
        if 'cmdb' in item:
            for key, value in (item['cmdb'].items()):
                    for i in range(len(value)):
                        if key in ['ci_name','ci_description','serial_number','additional_information','tag_list','child_dependency','supported_by_relation','used_by_relation','eva_dependency','model_version','lastupdate']:
                            if HostParameter.objects.filter(fk=r,parameter_section='cmdb',parameter=key).exists():
                                if HostParameter.objects.filter(fk=r,parameter_section='cmdb',parameter=key,parameter_index=i).exists():
                                    if not HostParameter.objects.filter(fk=r,parameter_section='cmdb',parameter=key,parameter_index=i,value=value[i]).exists():
                                        queryset= HostParameter.objects.filter(fk=r,parameter_section='cmdb',parameter=key,parameter_index=i).values()
                                        for obj in queryset:
                                            update = HostParameter.objects.get(pk=obj['id'])
                                            update.value = value[i]
                                            update.modified_at = in_datetime
                                            update.modified_by = in_executer
                                            update.save()
                                        #HostParameter.objects.filter(fk=r,parameter_section='cmdb',parameter=key,parameter_index=i).update(value=value[i],modified_at = in_datetime,modified_by = in_executer)
                                        print('Object cmdb attribute update') 
                                    else: 
                                        print('Skip cmdb attribute')
                                else: 
                                    HostParameter.objects.create(fk=r, parameter_section='cmdb',parameter=key, parameter_index=i,value=value[i],modified_at=in_datetime,modified_by=in_executer)
                            else:        
                                HostParameter.objects.create(fk=r, parameter_section='cmdb',parameter=key, parameter_index=i,value=value[i],modified_at=in_datetime,modified_by=in_executer)
                                print('Object cmdb attribute insert')
                        else:
                            raise ValidationError("Invalid parameter as '"+key+"' in cmdb group")
        if 'config' in item:    
        #if item['config']:
            for key, value in (item['config'].items()):
                    for i in range(len(value)):
                        if key in ['backupshare','script_set_version','boostfs','hostgroup']:
                            if HostParameter.objects.filter(fk=r,parameter_section='config',parameter=key).exists():
                                if HostParameter.objects.filter(fk=r,parameter_section='config',parameter=key,parameter_index=i).exists():
                                    if not HostParameter.objects.filter(fk=r,parameter_section='config',parameter=key,parameter_index=i,value=value[i]).exists():
                                        queryset= HostParameter.objects.filter(fk=r,parameter_section='config',parameter=key,parameter_index=i).values()
                                        for obj in queryset:
                                            update = HostParameter.objects.get(pk=obj['id'])
                                            update.value = value[i]
                                            update.modified_at = in_datetime
                                            update.modified_by = in_executer
                                            update.save()
                                        #HostParameter.objects.filter(fk=r,parameter_section='automation',parameter=key,parameter_index=i).update(value=value[i],modified_at = in_datetime,modified_by = in_executer)
                                        print('Object config attribute update') 
                                    else: 
                                        print('Skip config attribute')
                                else: 
                                    HostParameter.objects.create(fk=r, parameter_section='config',parameter=key, parameter_index=i,value=value[i],modified_at=in_datetime,modified_by=in_executer)
                            else:        
                                HostParameter.objects.create(fk=r, parameter_section='config',parameter=key, parameter_index=i,value=value[i],modified_at=in_datetime,modified_by=in_executer)
                                print('Object config attribute insert')
                        else:
                            raise ValidationError("Invalid parameter as '"+key+"' in config group")

        if 'licenses' in item:    
            for key, value in (item['licenses'].items()):
                    for i in range(len(value)):
                        if key in ['type','edition']:
                            if HostParameter.objects.filter(fk=r,parameter_section='licenses',parameter=key).exists():
                                if HostParameter.objects.filter(fk=r,parameter_section='licenses',parameter=key,parameter_index=i).exists():
                                    if not HostParameter.objects.filter(fk=r,parameter_section='licenses',parameter=key,parameter_index=i,value=value[i]).exists():
                                        queryset= HostParameter.objects.filter(fk=r,parameter_section='licenses',parameter=key,parameter_index=i).values()
                                        for obj in queryset:
                                            update = HostParameter.objects.get(pk=obj['id'])
                                            update.value = value[i]
                                            update.modified_at = in_datetime
                                            update.modified_by = in_executer
                                            update.save()
                                        print('Object licenses attribute update') 
                                    else: 
                                        print('Skip licenses attribute')
                                else: 
                                    HostParameter.objects.create(fk=r, parameter_section='licenses',parameter=key, parameter_index=i,value=value[i],modified_at=in_datetime,modified_by=in_executer)
                            else:        
                                HostParameter.objects.create(fk=r, parameter_section='licenses',parameter=key, parameter_index=i,value=value[i],modified_at=in_datetime,modified_by=in_executer)
                                print('Object licenses attribute insert')
                        else:
                            raise ValidationError("Invalid parameter as '"+key+"' in licenses group")              
    return True    
    #     for item in data:
    #         # Fcheck =Host.objects.filter(cmdbid=item['cmdbid'],product = item['product']).exists()
    #         # print (Fcheck)
    #         # if Fcheck is True: 
    #         #     Scheck =Host.objects.filter(cmdbid=item['cmdbid'],product = item['product'],name=item['name']).exists()
    #         #     print(Scheck)
    #         #     if Scheck is False:
    #         #         Host.objects.filter(cmdb=item['cmdbid']).update(**item)
    #         #         print("82")
    #         #     else:
    #         #         print("Nothing to update")
    #         # else:  
    #             Host.objects.create(cmdbid = item['cmdbid'], name = item['name'],product = item['product'],modified_at = in_datetime,modified_by = in_executer)
    #             r = Host.objects.get(cmdbid=item['cmdbid'])
    #             if item['cmdb']:
    #                     for key, value in (item['cmdb'].items()):
    #                             for i in range(len(value)):
    #                                 HostParameter.objects.create(fk=r, parameter_section='cmdb',
    #                                                     parameter=key, parameter_index=i,
    #                                                     value=value[i],
    #                                                     modified_at=in_datetime,
    #                                                     modified_by=in_executer
    #                                                 )
    #             print(item['cmdb'].items())
    #             response_data={"error":False,"Message":"Updated Successfully"}
    # except:
    #     response_data = {"error": True, "Message": "Failed to Update Data"}
    #     return response_data
    


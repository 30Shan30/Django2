
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import FilterSet
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.views import APIView

from django.core import serializers
import requests
import json
from django.conf import settings
from .serializers import HostSerializer,HostParameterSerializer,InstanceSerializer,InstanceParameterSerializer,Instance_accountSerializer,Instance_accountParameterSerializer, DbSerializer,DbParameterSerializer,OraTablespaceSerializer
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly, DjangoModelPermissions, IsAdminUser
from django.http import JsonResponse
from rest_framework.decorators import action

from .models import *
from Django_Project.scripts.host_request import *
from Django_Project.scripts.instance_request import *
from Django_Project.scripts.instanceaccount_request import *
from Django_Project.scripts.database_request import *
from Django_Project.scripts.databaseaccount_request import *
from django.db.models import Q

import datetime
from django.utils import timezone
from django.http import HttpResponse


schema_view = get_schema_view(
    openapi.Info(
        title="VIWEB API Interface (" + settings.ENV_SYSTEM + ")",
        default_version="v1",
        description="This page will show you all VI APIS you're allowed to execute!",
        contact=openapi.Contact(email=""),
    )
)

## only sample openapi schema , will be  dynamic json 
@swagger_auto_schema(method='post',
    request_body = openapi.Schema(
        title="Host and HostParameter Entries",
        type=openapi.TYPE_OBJECT,
        required=['rawdata'],
        properties={
            'rawdata': openapi.Schema(type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_OBJECT,
                    properties={
                        'cmdbid':openapi.Schema(type=openapi.TYPE_STRING, description='Asset ID computer object in CMDB', pattern="^CMDB[0-9]{11}", required='cmdbid'),   
                        'name':openapi.Schema(type=openapi.TYPE_STRING, description='Computer object CI Name' , required='name'),    
                        'product':openapi.Schema(type=openapi.TYPE_STRING, description='Product of computer object' , required='product'),
                        'manufacturer':openapi.Schema(type=openapi.TYPE_STRING, description='Manufacturer of computer object' , required='manufacturer'),
                        'site':openapi.Schema(type=openapi.TYPE_STRING, description='Site of computer object' , required='site'),
                        'area':openapi.Schema(type=openapi.TYPE_STRING, description='Area of computer object' , required='area'),
                        'status':openapi.Schema(type=openapi.TYPE_STRING, description='Status of computer object' , required='status'),
                        'usage_type':openapi.Schema(type=openapi.TYPE_STRING, description='Usage type of computer object' , required='usage_type'),
                        'urgency':openapi.Schema(type=openapi.TYPE_STRING, description='Urgency of computer object' , required='urgency'),
                        'primary_function':openapi.Schema(type=openapi.TYPE_STRING, description='Primary function of computer object' , required='primary_function'),
                        'monitored':openapi.Schema(type=openapi.TYPE_STRING, description='Monitored of computer object' , required='monitored'),
                        'dns':openapi.Schema(type=openapi.TYPE_STRING, description='Dns of computer object' , required='dns'),
                        'domain':openapi.Schema(type=openapi.TYPE_STRING, description='Domain of computer object' , required='domain'),
                        'ip_address':openapi.Schema(type=openapi.TYPE_STRING, description='IPV4 address of computer object' , required='ip_address'),
                        'owner':openapi.Schema(type=openapi.TYPE_STRING, description='Owner of computer object' ,pattern="^IF[0-9]{8}", required='owner'),
                        'last_seen':openapi.Schema(type=openapi.TYPE_STRING, description='last_seen of computer object trigger via Product owner' , required='last_seen'),
                        'cmdb': openapi.Schema(type=openapi.TYPE_OBJECT,                
                                            properties={
                                                'ci_name':openapi.Schema(type=openapi.TYPE_ARRAY,description='CMDB item name',required='ci_name' ,items=openapi.Schema(type=openapi.TYPE_STRING )),
                                                'serial_number':openapi.Schema(type=openapi.TYPE_ARRAY,description='CMDB item serial number ',required='serial_number', items=openapi.Schema(type=openapi.TYPE_STRING))
                                                        }
                        )
                    }

                )
            ),
        }
    )
)                           
@api_view(('POST',))
def hostrequest(request):
    data=request.data.get('rawdata')
    #print(data)
    in_datetime = datetime.datetime.now(timezone.utc)
    in_executer= "DjangoAPI_cmdbupsync"
    result= host_request(data,in_executer,in_datetime)

    if result:
        my_return = '{"status":"ok"}'
        output = status.HTTP_201_CREATED
    else:
        my_return = '{"status":"error"}'
        output = status.HTTP_400_BAD_REQUEST
    
    return Response(my_return, status=output)


### instance request 

@swagger_auto_schema(method='post',
    request_body = openapi.Schema(
        title="Instance and InstanceParameter Tables",
        type=openapi.TYPE_OBJECT,
        required=['rawdata'],
        properties={
            'rawdata': openapi.Schema(type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_OBJECT,
                    properties={
                        'cmdbid':openapi.Schema(type=openapi.TYPE_STRING, description='Asset ID database instance in CMDB', pattern="^CMDB[0-9]{11}", required='cmdbid'),   
                        'name':openapi.Schema(type=openapi.TYPE_STRING, description='Database instance name' , required='name'),    
                        'product':openapi.Schema(type=openapi.TYPE_STRING, description='Product of database instance object in CMDB' , required='product'),
                        'address':openapi.Schema(type=openapi.TYPE_STRING, description='Address of database instance object E.g. "" ' , required='address'),
                        'backup_medium':openapi.Schema(type=openapi.TYPE_STRING, description='Backup medium of database instance object E.g. "" ' , required='backup_medium'),
                        'multipurpose':openapi.Schema(type=openapi.TYPE_STRING, description='Multipurpose of database instance object E.g. "0" ' , required='multipurpose'),
                        'additional_information':openapi.Schema(type=openapi.TYPE_STRING, description='additional_information of database instance object in CMDB E.g. "" ' , required='additional_information'),
                        'area':openapi.Schema(type=openapi.TYPE_STRING, description='area of database instance object in CMDB E.g. "" only for Intranet' , required='area'),
                        'ci_description':openapi.Schema(type=openapi.TYPE_STRING, description='CI Description of database instance object in CMDB' , required='ci_description'),
                        'ci_name':openapi.Schema(type=openapi.TYPE_STRING, description='CI Name of database instance object in CMDB' , required='ci_name'),
                        'manufacturer':openapi.Schema(type=openapi.TYPE_STRING, description='Manufacturer of database instance object in CMDB' , required='manufacturer'),
                        'model_version':openapi.Schema(type=openapi.TYPE_STRING, description='Model version of database instance object in CMDB if empty E.g. "" ' , required='model_version'),
                        'monitored':openapi.Schema(type=openapi.TYPE_STRING, description='Monitored of database instance object in CMDB  E.g. "False" ' , required='monitored'),
                        'primary_function':openapi.Schema(type=openapi.TYPE_STRING, description='Primary function of database instance object in CMDB ' , required='primary_function'),
                        'serial_number':openapi.Schema(type=openapi.TYPE_STRING, description='Serial number of database instance object in CMDB ' , required='serial_number'),
                        'site':openapi.Schema(type=openapi.TYPE_STRING, description='Site of database instance object in CMDB ' , required='site'),
                        'sox_relevance':openapi.Schema(type=openapi.TYPE_STRING, description='SOX relevance of database instance object in CMDB if empty E.g. ""' , required='sox_relevance'),
                        'status':openapi.Schema(type=openapi.TYPE_STRING, description='Status of database instance object in CMDB' , required='status'),
                        'urgency':openapi.Schema(type=openapi.TYPE_STRING, description='Urgency of database instance object in CMDB' , required='urgency'),
                        'usage_type':openapi.Schema(type=openapi.TYPE_STRING, description='Usage type of database instance object in CMDB' , required='usage_type'),
                        'last_seen':openapi.Schema(type=openapi.TYPE_STRING, description='Last seen of database instance object only (Internal purpose)' , required='last_seen'),
                        'fk_host':openapi.Schema(type=openapi.TYPE_STRING, description='foreign key of host cmdid' , pattern="^CMDB[0-9]{11}", required='fk_host'),
                        'cmdb': openapi.Schema(type=openapi.TYPE_OBJECT,                
                                            properties={
                                                'supported_by_relation':openapi.Schema(type=openapi.TYPE_ARRAY,description='Must be group only in CMDB item',required='supported_by_relation' ,items=openapi.Schema(type=openapi.TYPE_STRING )),
                                                'used_by_relation':openapi.Schema(type=openapi.TYPE_ARRAY,description='Must be people ID (Eg: IF98765432) in CMDB item ',required='used_by_relation', items=openapi.Schema(type=openapi.TYPE_STRING))
                                                        }
                        ),
                        'contact': openapi.Schema(type=openapi.TYPE_OBJECT,                
                                            properties={
                                                'responsible':openapi.Schema(type=openapi.TYPE_ARRAY,description='Must be AD-group for approval responsible',required='responsible' ,items=openapi.Schema(type=openapi.TYPE_STRING ))
                                                        }
                        )
                    }

                )
            ),
        }
    )
)                           
@api_view(('POST',))
def instancerequest(request):
    data=request.data.get('rawdata')
    #print(data)
    in_datetime = datetime.datetime.now(timezone.utc)
    in_executer= "DjangoAPI_cmdbupsync"
    result= instance_request(data,in_executer,in_datetime)

    if result:
        my_return = '{"status":"ok"}'
        output = status.HTTP_201_CREATED
    else:
        my_return = '{"status":"error"}'
        output = status.HTTP_400_BAD_REQUEST
    
    return Response(my_return, status=output)


### instanceaccount request 

@swagger_auto_schema(method='post',
    request_body = openapi.Schema(
        title="Instanceaccount and InstanceaccountParameter Tables",
        type=openapi.TYPE_OBJECT,
        required=['rawdata'],
        properties={
            'rawdata': openapi.Schema(type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_OBJECT,
                    properties={
                        'fk_instance':openapi.Schema(type=openapi.TYPE_STRING, description='Instance CMDID', pattern="^CMDB[0-9]{11}", required='cmdbid'),   
                        'name':openapi.Schema(type=openapi.TYPE_STRING, description='Instance account name' , required='name'),    
                        'accounttype':openapi.Schema(type=openapi.TYPE_STRING, description='Account type' , required='accounttype'),
                        'created_date':openapi.Schema(type=openapi.TYPE_STRING, description='Create date and time of instance account' , required='created_date'),
                        'last_seen':openapi.Schema(type=openapi.TYPE_STRING, description='Last seen date and time of instance account' , required='last_seen'),
                        'status':openapi.Schema(type=openapi.TYPE_STRING, description='Status of instance account' , required='status'),
                        'owner':openapi.Schema(type=openapi.TYPE_STRING, description='Owner Global ID' ,pattern="^IF[0-9]{8}", required='owner'),
                        'contact': openapi.Schema(type=openapi.TYPE_OBJECT,                
                                            properties={
                                                'substitute':openapi.Schema(type=openapi.TYPE_ARRAY,description='Substitute Global ID', required='substitute' ,items=openapi.Schema(type=openapi.TYPE_STRING,pattern="^IF[0-9]{8}" ))
                                                        }
                        )
                    }

                )
            ),
        }
    )
)                           
@api_view(('POST',))
def instanceaccountrequest(request):
    data=request.data.get('rawdata')
    #print(data)
    in_datetime = datetime.datetime.now(timezone.utc)
    in_executer= "DjangoAPI_cmdbupsync"
    result= instanceaccount_request(data,in_executer,in_datetime)

    if result:
        my_return = '{"status":"ok"}'
        output = status.HTTP_201_CREATED
    else:
        my_return = '{"status":"error"}'
        output = status.HTTP_400_BAD_REQUEST
    
    return Response(my_return, status=output)


### database request 
@swagger_auto_schema(method='post',
    request_body = openapi.Schema(
        title="Database and DatabaseParameter Tables",
        type=openapi.TYPE_OBJECT,
        required=['rawdata'],
        properties={
            'rawdata': openapi.Schema(type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_OBJECT,
                    properties={
                        'cmdbid':openapi.Schema(type=openapi.TYPE_STRING, description='Asset ID database in CMDB', pattern="^CMDB[0-9]{11}", required='cmdbid'),   
                        'name':openapi.Schema(type=openapi.TYPE_STRING, description='Database name' , required='name'),
                        'protection_class':openapi.Schema(type=openapi.TYPE_STRING, description='Protection class of database' , required='protection_class'),
                        'created_date':openapi.Schema(type=openapi.TYPE_STRING, description='Creation date&time of database' , required='created_date'),
                        'area':openapi.Schema(type=openapi.TYPE_STRING, description='Area of database in CMDB E.g. "" only for Intranet' , required='area'),   
                        'ci_description':openapi.Schema(type=openapi.TYPE_STRING, description='CI Description of database in CMDB' , required='ci_description'), 
                        'ci_name':openapi.Schema(type=openapi.TYPE_STRING, description='CI Name of database in CMDB' , required='ci_name'),  
                        'last_seen':openapi.Schema(type=openapi.TYPE_STRING, description='Last seen of database object only (Internal purpose)' , required='last_seen'),
                        'model_version':openapi.Schema(type=openapi.TYPE_STRING, description='Model version of database object in CMDB if empty E.g. "" ' , required='model_version'),
                        'monitored':openapi.Schema(type=openapi.TYPE_STRING, description='Monitored of database object in CMDB  E.g. "False" ' , required='monitored'),
                        'primary_function':openapi.Schema(type=openapi.TYPE_STRING, description='Primary function of database instance object in CMDB ' , required='primary_function'), 
                        'product':openapi.Schema(type=openapi.TYPE_STRING, description='Product of database object' , required='product'),
                        'serial_number':openapi.Schema(type=openapi.TYPE_STRING, description='Serial number of database object in CMDB ' , required='serial_number'),
                        'site':openapi.Schema(type=openapi.TYPE_STRING, description='Site of database object in CMDB ' , required='site'),
                        'status':openapi.Schema(type=openapi.TYPE_STRING, description='Status of database object in CMDB' , required='status'),
                        'urgency':openapi.Schema(type=openapi.TYPE_STRING, description='Urgency of database object in CMDB' , required='urgency'),
                        'usage_type':openapi.Schema(type=openapi.TYPE_STRING, description='Usage type of database object in CMDB' , required='usage_type'),
                        'owner':openapi.Schema(type=openapi.TYPE_STRING, description='Owner of database object' ,pattern="^IF[0-9]{8}", required='owner'),
                        'fk_instance':openapi.Schema(type=openapi.TYPE_STRING, description='foreign key of instance id' , pattern="^CMDB[0-9]{11}", required='fk_instance'),
                        'cmdb': openapi.Schema(type=openapi.TYPE_OBJECT,                
                                            properties={
                                                'ci_name':openapi.Schema(type=openapi.TYPE_ARRAY,description='Configuration item name',required='ci_name' ,items=openapi.Schema(type=openapi.TYPE_STRING )),
                                                'serial_number':openapi.Schema(type=openapi.TYPE_ARRAY,description='Configuration item serial number ',required='serial_number', items=openapi.Schema(type=openapi.TYPE_STRING))
                                                        }
                        )
                    }

                )
            ),
        }
    )
)                           
@api_view(('POST',))
def databaserequest(request):
    data=request.data.get('rawdata')
    #print(data)
    in_datetime = datetime.datetime.now(timezone.utc)
    in_executer= "DjangoAPI_cmdbupsync"
    result= database_request(data,in_executer,in_datetime)

    if result:
        my_return = '{"status":"ok"}'
        output = status.HTTP_201_CREATED
    else:
        my_return = '{"status":"error"}'
        output = status.HTTP_400_BAD_REQUEST
    
    return Response(my_return, status=output)

### databaseaccount request 

@swagger_auto_schema(method='post',
    request_body = openapi.Schema(
        title="Databaseaccount and DatabaseaccountParameter Tables",
        type=openapi.TYPE_OBJECT,
        required=['rawdata'],
        properties={
            'rawdata': openapi.Schema(type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_OBJECT,
                    properties={
                        'fk_instance':openapi.Schema(type=openapi.TYPE_STRING, description='Instance CMDID', pattern="^CMDB[0-9]{11}", required='cmdbid'),   
                        'name':openapi.Schema(type=openapi.TYPE_STRING, description='Instance account name' , required='name'),    
                        'accounttype':openapi.Schema(type=openapi.TYPE_STRING, description='Account type' , required='accounttype'),
                        'created_date':openapi.Schema(type=openapi.TYPE_STRING, description='Create date and time of instance account' , required='created_date'),
                        'last_seen':openapi.Schema(type=openapi.TYPE_STRING, description='Last seen date and time of instance account' , required='last_seen'),
                        'status':openapi.Schema(type=openapi.TYPE_STRING, description='Status of instance account' , required='status'),
                        'owner':openapi.Schema(type=openapi.TYPE_STRING, description='Owner Global ID' ,pattern="^IF[0-9]{8}", required='owner'),
                        'contact': openapi.Schema(type=openapi.TYPE_OBJECT,                
                                            properties={
                                                'substitute':openapi.Schema(type=openapi.TYPE_ARRAY,description='Substitute Global ID', required='substitute' ,items=openapi.Schema(type=openapi.TYPE_STRING,pattern="^IF[0-9]{8}" ))
                                                        }
                        )
                    }

                )
            ),
        }
    )
)                           
@api_view(('POST',))
def databaseaccountrequest(request):
    data=request.data.get('rawdata')
    #print(data)
    in_datetime = datetime.datetime.now(timezone.utc)
    in_executer= "DjangoAPI_cmdbupsync"
    result= databaseaccount_request(data,in_executer,in_datetime)

    if result:
        my_return = '{"status":"ok"}'
        output = status.HTTP_201_CREATED
    else:
        my_return = '{"status":"error"}'
        output = status.HTTP_400_BAD_REQUEST
    
    return Response(my_return, status=output)


class HostViewFilter(FilterSet):
    """
    Filter for Host
    """

    class Meta:
        model = Host
        fields = '__all__'         
class HostView(viewsets.ModelViewSet):
    """
    GET...  Will list all available Host
    POST... Will create a new Instance parameters entry
    PUT...  Will update a existing Instance parameters entry
    """

    permission_classes = [DjangoModelPermissions]
    queryset = Host.objects.all()
    serializer_class = HostSerializer
    filter_class = HostViewFilter
    http_method_names = ["get","post","delete","put"] 

    def update(self, request, *args, **kwargs):
        hostid = self.get_object()
        if not Host.objects.filter(cmdbid=hostid,name=request.data['name'],product=request.data['product'],manufacturer=request.data['manufacturer'],site=request.data['site'],area=request.data['area'],status=request.data['status'],usage_type=request.data['usage_type'],urgency=request.data['urgency'],primary_function=request.data['primary_function'],monitored=request.data['monitored'],sox_relevance=request.data['sox_relevance'],dns=request.data['dns'],domain=request.data['domain'],ip_address=request.data['ip_address'],owner=request.data['owner']).exists():
            serializer = self.get_serializer(hostid, data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            self.perform_update(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            response_data={"Message":"Nothing to Update"}
            return Response(response_data, status=status.HTTP_200_OK)   

class HostParameterViewFilter(FilterSet):
    """
    Filter for HostParameter
    """

    class Meta:
        model = HostParameter
        fields = '__all__'         
class HostParameterView(viewsets.ModelViewSet):
    """
    GET...  Will list all available Host
    POST... Will create a new Instance parameters entry
    PUT...  Will update a existing Instance parameters entry
    """

    permission_classes = [DjangoModelPermissions]

    queryset = HostParameter.objects.all()
    serializer_class = HostParameterSerializer
    filter_class = HostParameterViewFilter
    http_method_names = ["get","post","put","delete"] 

    def create(self, request, *args, **kwargs):
        print (request.data['parameter'])
        if request.data['parameter_section'] in 'cmdb':
            if request.data['parameter'] in ['ci_name','ci_description','serial_number','additional_information','tag_list','child_dependency','supported_by_relation','used_by_relation','eva_dependency','model_version','lastupdate']:
                serializer = self.get_serializer(data=request.data)
                print(serializer)
                serializer.is_valid(raise_exception=True)
                data = serializer.validated_data
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                response_data={"Message":"Invalid parameter as '"+request.data['parameter']+"' in cmdb group"}
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            
        elif request.data['parameter_section'] in 'automation':
            if request.data['parameter'] in ['backupshare','script_set_version','boostfs','hostgroup']:
                serializer = self.get_serializer(data=request.data)
                print(serializer)
                serializer.is_valid(raise_exception=True)
                data = serializer.validated_data
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                response_data={"Message":"Invalid parameter as '"+request.data['parameter']+"' in automation group"}
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.data['parameter_section'] in 'licenses':
            if request.data['parameter'] in ['type','edition']:
                serializer = self.get_serializer(data=request.data)
                print(serializer)
                serializer.is_valid(raise_exception=True)
                data = serializer.validated_data
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                response_data={"Message":"Invalid parameter as '"+request.data['parameter']+"' in licenses group"}
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        else:
            response_data={"Message":"Invalid parameter_section as '"+request.data['parameter_section']+"' in group"}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        

    def update(self, request, *args, **kwargs):
        hostparameterid = self.get_object()
        if not HostParameter.objects.filter(fk=request.data['fk'],parameter_section=request.data['parameter_section'],parameter=request.data['parameter'],parameter_index=request.data['parameter_index'],value=request.data['value']).exists():
            serializer = self.get_serializer(hostparameterid, data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            self.perform_update(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            response_data={"Message":"Nothing to Update"}
            return Response(response_data, status=status.HTTP_200_OK)   

#####Instance####
class InstanceViewFilter(FilterSet):
    """
    Filter for Instance
    """

    class Meta:
        model = Instance
        fields = '__all__'   

class InstanceView(viewsets.ModelViewSet):
    """
    GET...  Will list all available Host
    POST... Will create a new Instance parameters entry
    PUT...  Will update a existing Instance parameters entry
    """

    permission_classes = [DjangoModelPermissions]

    queryset = Instance.objects.all()
    serializer_class = InstanceSerializer
    filter_class = InstanceViewFilter
    http_method_names = ["get","post","put","delete"]  

    def update(self, request, *args, **kwargs):
        instanceid = self.get_object()
        if not Instance.objects.filter(cmdbid=instanceid,name=request.data['name'],product=request.data['product'],address=request.data['address'],backup_medium=request.data['backup_medium'],multipurpose=request.data['multipurpose'],additional_information=request.data['additional_information'],area=request.data['area'],ci_description=request.data['ci_description'],ci_name=request.data['ci_name'],manufacturer=request.data['manufacturer'],model_version=request.data['model_version'],monitored=request.data['monitored'],primary_function=request.data['primary_function'],serial_number=request.data['serial_number'],site=request.data['site'],sox_relevance=request.data['sox_relevance'],status=request.data['status'],usage_type=request.data['usage_type'],urgency=request.data['urgency'],fk_host=request.data['fk_host']).exists():
            serializer = self.get_serializer(instanceid, data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            self.perform_update(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            response_data={"Message":"Nothing to Update"}
            return Response(response_data, status=status.HTTP_200_OK)   


class InstanceParameterViewFilter(FilterSet):
    """
    Filter for InstanceParameter
    """

    class Meta:
        model = InstanceParameter
        fields = '__all__'         
class InstanceParameterView(viewsets.ModelViewSet):
    """
    GET...  Will list all available Host
    POST... Will create a new Instance parameters entry
    PUT...  Will update a existing Instance parameters entry
    """

    permission_classes = [DjangoModelPermissions]

    queryset = InstanceParameter.objects.all()
    serializer_class = InstanceParameterSerializer
    filter_class = InstanceParameterViewFilter
    http_method_names = ["get","post","put","delete"]  

    def create(self, request, *args, **kwargs):
        print (request.data['parameter'])
        if request.data['parameter_section'] in 'cmdb':
            if request.data['parameter'] in ['child_dependency','currentWorkflowID','eva_dependency','lastCRQ','tag_list','supported_by_relation','used_by_relation','eva_dependency']:
                serializer = self.get_serializer(data=request.data)
                print(serializer)
                serializer.is_valid(raise_exception=True)
                data = serializer.validated_data
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                response_data={"Message":"Invalid parameter as '"+request.data['parameter']+"' in cmdb group"}
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            
        elif request.data['parameter_section'] in 'config':
            if request.data['parameter'] in ['appl','backup_type','backupshare','binlog_expire_logs_seconds','binlog_backup','collation','expire_logs_days','filerexport','filerpath','filerqtree','filersize','filervolume','fstype','innodb_buffer_pool_instances','innodb_buffer_pool_size','pkg','pkgmount','port','product','protection_class','secure_file_priv','server_id','site_short','urgency','usage_type','vserver','wsrep_provider','local_infile','max_connections','max_user_connections','mount_option','address_alias','role','standby_parent_cmdbid']:
                serializer = self.get_serializer(data=request.data)
                print(serializer)
                serializer.is_valid(raise_exception=True)
                data = serializer.validated_data
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                response_data={"Message":"Invalid parameter as '"+request.data['parameter']+"' in config group"}
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.data['parameter_section'] in 'contact':
            if request.data['parameter'] in ['responsible']:
                serializer = self.get_serializer(data=request.data)
                print(serializer)
                serializer.is_valid(raise_exception=True)
                data = serializer.validated_data
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                response_data={"Message":"Invalid parameter as '"+request.data['parameter']+"' in contact group"}
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        else:
            response_data={"Message":"Invalid parameter_section as '"+request.data['parameter_section']+"' in group"}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        

    def update(self, request, *args, **kwargs):
        instanceparameterid = self.get_object()
        if not InstanceParameter.objects.filter(fk=request.data['fk'],parameter_section=request.data['parameter_section'],parameter=request.data['parameter'],parameter_index=request.data['parameter_index'],value=request.data['value']).exists():
            serializer = self.get_serializer(instanceparameterid, data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            self.perform_update(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            response_data={"Message":"Nothing to Update"}
            return Response(response_data, status=status.HTTP_200_OK)   

#####Instance_account####
class Instance_accountViewFilter(FilterSet):
    """
    Filter for Instance_account
    """

    class Meta:
        model = Instance_account
        fields = '__all__'   

class Instance_accountView(viewsets.ModelViewSet):
    """
    GET...  Will list all available Instance_account
    POST... Will create a new Instance_account parameters entry
    PUT...  Will update a existing Instance_account parameters entry
    """

    permission_classes = [DjangoModelPermissions]

    queryset = Instance_account.objects.all()
    serializer_class = Instance_accountSerializer
    filter_class = Instance_accountViewFilter
    http_method_names = ["get","post","put","delete"]  

    def update(self, request, *args, **kwargs):
        instanceaccid = self.get_object()
        print (instanceaccid)
        if not Instance_account.objects.filter(fk_instance=request.data['fk_instance'],name=request.data['name'],accounttype=request.data['accounttype'],last_seen=request.data['last_seen'],status=request.data['status'],owner=request.data['owner'],accountid=request.data['accountid']).exists():
            serializer = self.get_serializer(instanceaccid, data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            self.perform_update(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            response_data={"Message":"Nothing to Update"}
            return Response(response_data, status=status.HTTP_200_OK)   

class Instance_accountParameterViewFilter(FilterSet):
    """
    Filter for Instance_accountParameter
    """

    class Meta:
        model = Instance_accountParameter
        fields = '__all__'   

class Instance_accountParameterView(viewsets.ModelViewSet):
    """
    GET...  Will list all available Instance_accountParameter
    POST... Will create a new Instance_accountParameter parameters entry
    PUT...  Will update a existing Instance_accountParameter parameters entry
    """

    permission_classes = [DjangoModelPermissions]

    queryset = Instance_accountParameter.objects.all()
    serializer_class = Instance_accountParameterSerializer
    filter_class = Instance_accountParameterViewFilter
    http_method_names = ["get","post","put","delete"]

    def create(self, request, *args, **kwargs):
        print (request.data['parameter'])
        if request.data['parameter_section'] in 'base':
            if request.data['parameter'] in ['max_sessions','pw_lifetime','pw_lifetime_justification','account_status','expiry_date','last_login','ora_acc_type','ora_profile']:
                serializer = self.get_serializer(data=request.data)
                print(serializer)
                serializer.is_valid(raise_exception=True)
                data = serializer.validated_data
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                response_data={"Message":"Invalid parameter as '"+request.data['parameter']+"' in base group"}
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            
        elif request.data['parameter_section'] in 'contact':
            if request.data['parameter'] in ['informee','substitute']:
                serializer = self.get_serializer(data=request.data)
                print(serializer)
                serializer.is_valid(raise_exception=True)
                data = serializer.validated_data
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                response_data={"Message":"Invalid parameter as '"+request.data['parameter']+"' in contact group"}
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.data['parameter_section'] in 'idms':
            if request.data['parameter'] in ['last_error']:
                serializer = self.get_serializer(data=request.data)
                print(serializer)
                serializer.is_valid(raise_exception=True)
                data = serializer.validated_data
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                response_data={"Message":"Invalid parameter as '"+request.data['parameter']+"' in idms group"}
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.data['parameter_section'] in 'validation':
            if request.data['parameter'] in ['last_validated','validate_action','validated_by','validation_action','validation_comment','validation_crq','validation_id','validation_sox']:
                serializer = self.get_serializer(data=request.data)
                print(serializer)
                serializer.is_valid(raise_exception=True)
                data = serializer.validated_data
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                response_data={"Message":"Invalid parameter as '"+request.data['parameter']+"' in validation group"}
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        else:
            response_data={"Message":"Invalid parameter_section as '"+request.data['parameter_section']+"' in group"}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        

    def update(self, request, *args, **kwargs):
        instanceaccountid = self.get_object()
        if not Instance_accountParameter.objects.filter(fk=request.data['fk'],parameter_section=request.data['parameter_section'],parameter=request.data['parameter'],parameter_index=request.data['parameter_index'],value=request.data['value']).exists():
            serializer = self.get_serializer(instanceaccountid, data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            self.perform_update(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            response_data={"Message":"Nothing to Update"}
            return Response(response_data, status=status.HTTP_200_OK) 

#####Db####
class DbViewFilter(FilterSet):
    """
    Filter for Db
    """

    class Meta:
        model = Db
        fields = '__all__'   

class DbView(viewsets.ModelViewSet):
    """
    GET...  Will list all available Db
    POST... Will create a new Db parameters entry
    PUT...  Will update a existing Db parameters entry
    """

    permission_classes = [DjangoModelPermissions]

    queryset = Db.objects.all()
    serializer_class = DbSerializer
    filter_class = DbViewFilter
    http_method_names = ["get","post","put","delete"]
    
    def update(self, request, *args, **kwargs):
        databaseid = self.get_object()
        if not Db.objects.filter(cmdbid=databaseid,name=request.data['name'],protection_class=request.data['protection_class'],area=request.data['area'],ci_description=request.data['ci_description'],ci_name=request.data['ci_name'],manufacturer=request.data['manufacturer'],model_version=request.data['model_version'],monitored=request.data['monitored'],primary_function=request.data['primary_function'],serial_number=request.data['serial_number'],site=request.data['site'],status=request.data['status'],usage_type=request.data['usage_type'],urgency=request.data['urgency'],owner=request.data['owner'],fk_instance=request.data['fk_instance']).exists():
            serializer = self.get_serializer(databaseid, data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            self.perform_update(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            response_data={"Message":"Nothing to Update"}
            return Response(response_data, status=status.HTTP_200_OK)     

class DbParameterViewFilter(FilterSet):
    """
    Filter for DbParameter
    """

    class Meta:
        model = DbParameter
        fields = '__all__'         
class DbParameterView(viewsets.ModelViewSet):
    """
    GET...  Will list all available Db
    POST... Will create a new Db parameters entry
    PUT...  Will update a existing Db parameters entry
    """

    permission_classes = [DjangoModelPermissions]

    queryset = DbParameter.objects.all()
    serializer_class = DbParameterSerializer
    filter_class = DbParameterViewFilter
    http_method_names = ["get","post","put","delete"]  

    def create(self, request, *args, **kwargs):
        print (request.data['parameter'])
        if request.data['parameter_section'] in 'cmdb':
            if request.data['parameter'] in ['additional_information','child_dependency','currentWorkflowID','eva_dependency','lastCRQ','last_cmdbupdate','sox_relevance','supported_by_relation','tag_list','used_by_relation']:
                serializer = self.get_serializer(data=request.data)
                print(serializer)
                serializer.is_valid(raise_exception=True)
                data = serializer.validated_data
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                response_data={"Message":"Invalid parameter as '"+request.data['parameter']+"' in cmdb group"}
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            
        elif request.data['parameter_section'] in 'contact':
            if request.data['parameter'] in ['informee','substitute']:
                serializer = self.get_serializer(data=request.data)
                print(serializer)
                serializer.is_valid(raise_exception=True)
                data = serializer.validated_data
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                response_data={"Message":"Invalid parameter as '"+request.data['parameter']+"' in contact group"}
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.data['parameter_section'] in 'base':
            if request.data['parameter'] in ['created_date']:
                serializer = self.get_serializer(data=request.data)
                print(serializer)
                serializer.is_valid(raise_exception=True)
                data = serializer.validated_data
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                response_data={"Message":"Invalid parameter as '"+request.data['parameter']+"' in contact group"}
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        elif request.data['parameter_section'] in 'config':
            if request.data['parameter'] in ['characterset','collation','protection_class','size_requested','status','collation','ora_acc_type','ora_profile']:
                serializer = self.get_serializer(data=request.data)
                print(serializer)
                serializer.is_valid(raise_exception=True)
                data = serializer.validated_data
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                response_data={"Message":"Invalid parameter as '"+request.data['parameter']+"' in contact group"}
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        else:
            response_data={"Message":"Invalid parameter_section as '"+request.data['parameter_section']+"' in group"}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        

    def update(self, request, *args, **kwargs):
        databaseparameterid = self.get_object()
        if not DbParameter.objects.filter(fk=request.data['fk'],parameter_section=request.data['parameter_section'],parameter=request.data['parameter'],parameter_index=request.data['parameter_index'],value=request.data['value']).exists():
            serializer = self.get_serializer(databaseparameterid, data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            self.perform_update(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            response_data={"Message":"Nothing to Update"}
            return Response(response_data, status=status.HTTP_200_OK)   


#####Database_account####
class Database_accountViewFilter(FilterSet):
    """
    Filter for Database_account
    """

    class Meta:
        model = Database_account
        fields = '__all__'   

class Database_accountView(viewsets.ModelViewSet):
    """
    GET...  Will list all available Database_account
    POST... Will create a new Database_account parameters entry
    PUT...  Will update a existing Database_account parameters entry
    """

    permission_classes = [DjangoModelPermissions]

    queryset = Database_account.objects.all()
    serializer_class = Database_accountSerializer
    filter_class = Database_accountViewFilter
    http_method_names = ["get","post","put","delete"]

    def update(self, request, *args, **kwargs):
        databaseaccid = self.get_object()
        print (databaseaccid)
        if not Database_account.objects.filter(fk_database=request.data['fk_database'],name=request.data['name'],accounttype=request.data['accounttype'],last_seen=request.data['last_seen'],status=request.data['status'],owner=request.data['owner'],accountid=request.data['accountid']).exists():
            serializer = self.get_serializer(databaseaccid, data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            self.perform_update(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            response_data={"Message":"Nothing to Update"}
            return Response(response_data, status=status.HTTP_200_OK) 

class Database_accountParameterViewFilter(FilterSet):
    """
    Filter for Instance_accountParameter
    """

    class Meta:
        model = Database_accountParameter
        fields = '__all__'   

class Database_accountParameterView(viewsets.ModelViewSet):
    """
    GET...  Will list all available Database_account
    POST... Will create a new Database_account parameters entry
    PUT...  Will update a existing Database_account parameters entry
    """

    permission_classes = [DjangoModelPermissions]

    queryset = Database_accountParameter.objects.all()
    serializer_class = Database_accountParameterSerializer
    filter_class = Database_accountParameterViewFilter
    http_method_names = ["get","post","put","delete"]

    def create(self, request, *args, **kwargs):
        print (request.data['parameter'])
        if request.data['parameter_section'] in 'base':
            if request.data['parameter'] in ['max_sessions','pw_lifetime','pw_lifetime_justification','account_status','expiry_date','last_login','ora_acc_type','ora_profile']:
                serializer = self.get_serializer(data=request.data)
                print(serializer)
                serializer.is_valid(raise_exception=True)
                data = serializer.validated_data
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                response_data={"Message":"Invalid parameter as '"+request.data['parameter']+"' in base group"}
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            
        elif request.data['parameter_section'] in 'contact':
            if request.data['parameter'] in ['informee','substitute']:
                serializer = self.get_serializer(data=request.data)
                print(serializer)
                serializer.is_valid(raise_exception=True)
                data = serializer.validated_data
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                response_data={"Message":"Invalid parameter as '"+request.data['parameter']+"' in contact group"}
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.data['parameter_section'] in 'idms':
            if request.data['parameter'] in ['last_error']:
                serializer = self.get_serializer(data=request.data)
                print(serializer)
                serializer.is_valid(raise_exception=True)
                data = serializer.validated_data
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                response_data={"Message":"Invalid parameter as '"+request.data['parameter']+"' in idms group"}
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.data['parameter_section'] in 'validation':
            if request.data['parameter'] in ['last_validated','validate_action','validated_by','validation_action','validation_comment','validation_crq','validation_id','validation_sox']:
                serializer = self.get_serializer(data=request.data)
                print(serializer)
                serializer.is_valid(raise_exception=True)
                data = serializer.validated_data
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                response_data={"Message":"Invalid parameter as '"+request.data['parameter']+"' in validation group"}
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        else:
            response_data={"Message":"Invalid parameter_section as '"+request.data['parameter_section']+"' in group"}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        

    def update(self, request, *args, **kwargs):
        databaseaccountid = self.get_object()
        if not Database_accountParameter.objects.filter(fk=request.data['fk'],parameter_section=request.data['parameter_section'],parameter=request.data['parameter'],parameter_index=request.data['parameter_index'],value=request.data['value']).exists():
            serializer = self.get_serializer(databaseaccountid, data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            self.perform_update(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            response_data={"Message":"Nothing to Update"}
            return Response(response_data, status=status.HTTP_200_OK) 


# #####Account####
# class AccountViewFilter(FilterSet):
#     """
#     Filter for Account
#     """

#     class Meta:
#         model = Account
#         fields = '__all__'   

# class AccountView(viewsets.ModelViewSet):
#     """
#     GET...  Will list all available Account
#     POST... Will create a new Account parameters entry
#     PUT...  Will update a existing Account parameters entry
#     """

#     permission_classes = [DjangoModelPermissions]

#     queryset = Account.objects.all()
#     serializer_class = AccountSerializer
#     filter_class = AccountViewFilter
#     http_method_names = ["get","post","put","delete"]  

# class AccountParameterViewFilter(FilterSet):
#     """
#     Filter for AccountParameter
#     """

#     class Meta:
#         model = AccountParameter
#         fields = '__all__'         
# class AccountParameterView(viewsets.ModelViewSet):
#     """
#     GET...  Will list all available Account
#     POST... Will create a new Account parameters entry
#     PUT...  Will update a existing Account parameters entry
#     """

#     permission_classes = [DjangoModelPermissions]

#     queryset = AccountParameter.objects.all()
#     serializer_class = AccountParameterSerializer
#     filter_class = AccountParameterViewFilter
#     http_method_names = ["get","post","put","delete"]  


#####CMDBHostProduct####
class CMDBHostProductViewFilter(FilterSet):
    """
    Filter for CMDB Host Product (Computer Object in CMDB)
    """

    class Meta:
        model = CMDBHostProduct
        fields = '__all__'   

class CMDBHostProductView(viewsets.ModelViewSet):
    """
    GET...      Will list all available CMDB Host Product (E.g.Lnwsoft Cluster, Lnwsoft Cluster Instance, Microsoft Cluster, Microsoft Cluster Instance)
    POST...     Will create a new CMDB Host Product entry
    DELETE...   Will update a existing CMDB Host Product entry
    """

    permission_classes = [DjangoModelPermissions]

    queryset = CMDBHostProduct.objects.all()
    serializer_class = CMDBHostProductSerializer
    filter_class = CMDBHostProductViewFilter
    http_method_names = ["get","post","delete"]  


    #####CMDBStatus####
class CMDBStatusViewFilter(FilterSet):
    """
    Filter for CMDBStatus
    """

    class Meta:
        model = CMDBStatus
        fields = '__all__'   

class CMDBStatusView(viewsets.ModelViewSet):
    """
    GET...  Will list all available Account
    POST... Will create a new Account parameters entry
    PUT...  Will update a existing Account parameters entry
    """

    permission_classes = [DjangoModelPermissions]

    queryset = CMDBStatus.objects.all()
    serializer_class = CMDBStatusSerializer
    filter_class = CMDBStatusViewFilter
    http_method_names = ["get","post","delete"]  

    
    #####CMDBUsage####
class CMDBUsageViewFilter(FilterSet):
    """
    Filter for CMDBUsage
    """

    class Meta:
        model = CMDBUsage
        fields = '__all__'   

class CMDBUsageView(viewsets.ModelViewSet):
    """
    GET...  Will list all available Account
    POST... Will create a new Account parameters entry
    PUT...  Will update a existing Account parameters entry
    """

    permission_classes = [DjangoModelPermissions]

    queryset = CMDBUsage.objects.all()
    serializer_class = CMDBUsageSerializer
    filter_class = CMDBUsageViewFilter
    http_method_names = ["get","post","delete"]  


    #####CMDBUrgency####
class CMDBUrgencyViewFilter(FilterSet):
    """
    Filter for CMDBUrgency
    """

    class Meta:
        model = CMDBUrgency
        fields = '__all__'   

class CMDBUrgencyView(viewsets.ModelViewSet):
    """
    GET...  Will list all available Account
    POST... Will create a new Account parameters entry
    PUT...  Will update a existing Account parameters entry
    """

    permission_classes = [DjangoModelPermissions]

    queryset = CMDBUrgency.objects.all()
    serializer_class = CMDBUrgencySerializer
    filter_class = CMDBUrgencyViewFilter
    http_method_names = ["get","post","delete"]  

    #####CMDBPrimaryfunctionView####
class CMDBPrimaryfunctionViewFilter(FilterSet):
    """
    Filter for CMDBPrimaryfunctionView
    """

    class Meta:
        model = CMDBPrimaryfunction
        fields = '__all__'   

class CMDBPrimaryfunctionView(viewsets.ModelViewSet):
    """
    GET...  Will list all available Account
    POST... Will create a new Account parameters entry
    PUT...  Will update a existing Account parameters entry
    """

    permission_classes = [DjangoModelPermissions]

    queryset = CMDBPrimaryfunction.objects.all()
    serializer_class = CMDBPrimaryfunctionSerializer
    filter_class = CMDBPrimaryfunctionViewFilter
    http_method_names = ["get","post","delete"]  

        
        #####CMDBManufacturerView####
class CMDBManufacturerViewFilter(FilterSet):
    """
    Filter for CMDBManufacturerView
    """

    class Meta:
        model = CMDBManufacturer
        fields = '__all__'   

class CMDBManufacturerView(viewsets.ModelViewSet):
    """
    GET...  Will list all available Account
    POST... Will create a new Account parameters entry
    PUT...  Will update a existing Account parameters entry
    """

    permission_classes = [DjangoModelPermissions]

    queryset = CMDBManufacturer.objects.all()
    serializer_class = CMDBManufacturerSerializer
    filter_class = CMDBManufacturerViewFilter
    http_method_names = ["get","post","delete"]  

        #####CMDBSiteView####
class CMDBSiteViewFilter(FilterSet):
    """
    Filter for CMDBSiteView
    """

    class Meta:
        model = CMDBSite
        fields = '__all__'   

class CMDBSiteView(viewsets.ModelViewSet):
    """
    GET...  Will list all available Account
    POST... Will create a new Account parameters entry
    PUT...  Will update a existing Account parameters entry
    """

    permission_classes = [DjangoModelPermissions]

    queryset = CMDBSite.objects.all()
    serializer_class = CMDBSiteSerializer
    filter_class = CMDBSiteViewFilter
    http_method_names = ["get","post","delete"]  
    
            #####CMDBMonitoredView####
class CMDBMonitoredViewFilter(FilterSet):
    """
    Filter for CMDBMonitoredView
    """

    class Meta:
        model = CMDBMonitored
        fields = '__all__'   

class CMDBMonitoredView(viewsets.ModelViewSet):
    """
    GET...  Will list all available Account
    POST... Will create a new Account parameters entry
    PUT...  Will update a existing Account parameters entry
    """

    permission_classes = [DjangoModelPermissions]

    queryset = CMDBMonitored.objects.all()
    serializer_class = CMDBMonitoredSerializer
    filter_class = CMDBMonitoredViewFilter
    http_method_names = ["get","post","delete"]  


#####CMDBInstanceProductView####
class CMDBInstanceProductViewFilter(FilterSet):
    """
    Filter for CMDBInstanceProductView
    """

    class Meta:
        model = CMDBInstanceProduct
        fields = '__all__'   

class CMDBInstanceProductView(viewsets.ModelViewSet):
    """
    GET...  Will list all available Account
    POST... Will create a new Account parameters entry
    PUT...  Will update a existing Account parameters entry
    """

    permission_classes = [DjangoModelPermissions]

    queryset = CMDBInstanceProduct.objects.all()
    serializer_class = CMDBInstanceProductSerializer
    filter_class = CMDBInstanceProductViewFilter
    http_method_names = ["get","post","delete"]   

#####ConfigMultipurposeView####
class ConfigMultipurposeViewFilter(FilterSet):
    """
    Filter for CMDBInstanceProductView
    """

    class Meta:
        model = ConfigMultipurpose
        fields = '__all__'   

class ConfigMultipurposeView(viewsets.ModelViewSet):
    """
    GET...  Will list all available Account
    POST... Will create a new Account parameters entry
    PUT...  Will update a existing Account parameters entry
    """

    permission_classes = [DjangoModelPermissions]

    queryset = ConfigMultipurpose.objects.all()
    serializer_class = ConfigMultipurposeSerializer
    filter_class = ConfigMultipurposeViewFilter
    http_method_names = ["get","post","delete"]   


#####CMDBDBProductView####
class CMDBDatabaseProductViewFilter(FilterSet):
    """
    Filter for CMDBDatabaseProductView
    """

    class Meta:
        model = CMDBDatabaseProduct
        fields = '__all__'   

class CMDBDatabaseProductView(viewsets.ModelViewSet):
    """
    GET...  Will list all available CMDBDatabaseProduct
    POST... Will create a new CMDBDatabaseProduct parameters entry
    PUT...  Will update a existing CMDBDatabaseProduct parameters entry
    """

    permission_classes = [DjangoModelPermissions]

    queryset = CMDBDatabaseProduct.objects.all()
    serializer_class = CMDBDatabaseProductSerializer
    filter_class = CMDBDatabaseProductViewFilter
    http_method_names = ["get","post","delete"]   

    #####OraTablespaceView####
class OraTablespaceViewFilter(FilterSet):
    """
    Filter for Oracle Tablespace 
    """

    class Meta:
        model = OraTablespace
        fields = '__all__'   

class OraTablespaceView(viewsets.ModelViewSet):
    """
    GET...  Will list all available Oracle Tablespace
    POST... Will create a new Oracle Tablespace entry
    PUT...  Will update a existing Oracle Tablespace entry
    """

    permission_classes = [DjangoModelPermissions]

    queryset = OraTablespace.objects.all()
    serializer_class = OraTablespaceSerializer
    filter_class = OraTablespaceViewFilter
    http_method_names = ["get","post","put","delete"]  

Product = openapi.Parameter(
    'product', 
    openapi.IN_QUERY, 
    description="product", 
    type=openapi.TYPE_STRING,
    #required = True,
)

@swagger_auto_schema(method='GET', 
    manual_parameters=[
        Product
    ]
)                        
@api_view(('GET',))
def accountlist(request):  
    print (request.GET.get('product'))
    ##accountlists = Instance_account.objects.filter(Q(product = request.GET.get('product'))).select_related('fk_instance')
    #accountlists = Instance_account.objects.filter(request.GET.get('product')).prefetch_related('fk_instance')   ##       .all().prefetch_related('fk_instance')  
    accountlists = Instance_account.objects.all().prefetch_related('fk_instance')
    # accountlists = Instance_account.objects.filter(product=request.GET.get('product')).select_related('fk_instance')
    # print (accountlists)
    # return
    #accountlists = Instance_account.select_related(Instance).filter(product=request.GET.get('product'))
    dict = {}
    records=[]
    for account_list in accountlists:
        product = account_list.fk_instance.product
    #     print(request.GET.get('product'))
        print(product)
        print(account_list.fk_instance.product)
        list = {"name":account_list.name,"ci_name": account_list.fk_instance.ci_name, "product": product.name, "hostname" : account_list.fk_instance.fk_host.name}
        print (list)
        records.append(list)
        
        dict["Data"]=records
    return JsonResponse(dict)



    # accountlists = Instance_account.objects.all().prefetch_related('fk_instance')
    # records=[]
    # for account_list in accountlists:
    #     print(account_list.name)
    #     list = {"name":account_list.name,"ci_name": account_list.fk_instance.ci_name}
    #     records.append(list)
        
    #     records = json.dumps({'pickups': records}, indent=4) 
    #     pickup_response={"pickup":records}
    
    # return HttpResponse(pickup_response, content_type="application/json")

    # return JsonResponse(account_list.name, safe=False) 
    # result= accountlist(data)

    # if result:
    #     my_return = '{"status":"ok"}'
    #     output = status.HTTP_201_CREATED
    # else:
    #     my_return = '{"status":"error"}'
    #     output = status.HTTP_400_BAD_REQUEST
    
    # return Response(my_return, status=output)


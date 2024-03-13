from rest_framework import serializers, status
from rest_framework.response import Response

import requests
import json
from django.conf import settings
from .models import Host,HostParameter,Instance,InstanceParameter,Instance_account,Instance_accountParameter,Db,DbParameter,Database_account,Database_accountParameter
from .models import CMDBHostProduct,CMDBStatus,CMDBUsage,CMDBUrgency,CMDBPrimaryfunction,CMDBManufacturer,CMDBSite,CMDBMonitored,CMDBInstanceProduct,ConfigMultipurpose,CMDBDatabaseProduct
from .models import OraTablespace

###Host###
class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = "__all__"
        #read_only_fields = ["modified_at","modified_by"]  

class HostParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostParameter
        fields = "__all__" 
 

###Instance###
class InstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instance
        fields = "__all__" 

class InstanceParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstanceParameter
        fields = "__all__" 


###Instance_account###
class Instance_accountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instance_account
        fields = "__all__" 

class Instance_accountParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instance_accountParameter
        fields = "__all__" 


##Db###
class DbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Db
        fields = "__all__" 

class DbParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = DbParameter
        fields = "__all__" 

###Instance_account###
class Database_accountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Database_account
        fields = "__all__" 

class Database_accountParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Database_accountParameter
        fields = "__all__" 


# ###Account###
# class AccountSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Account
#         fields = "__all__" 

# class AccountParameterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AccountParameter
#         fields = "__all__" 


###CMDBHostProduct###
class CMDBHostProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CMDBHostProduct
        fields =  "__all__" 


 ###CMDBStatus###
class CMDBStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CMDBStatus
        fields =  "__all__"        

        
         ###CMDBUsage###
class CMDBUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CMDBUsage
        fields =  "__all__"        


         ###CMDBUrgency###
class CMDBUrgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = CMDBUrgency
        fields =  "__all__"     
           

         ###CMDBPrimaryfunction###
class CMDBPrimaryfunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CMDBPrimaryfunction
        fields =  "__all__"    
        
        
         ###CMDBManufacturer###
class CMDBManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CMDBManufacturer
        fields =  "__all__"    


          ###CMDBSite###
class CMDBSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CMDBSite
        fields =  "__all__"    
        
          ###CMDBMonitored###
class CMDBMonitoredSerializer(serializers.ModelSerializer):
    class Meta:
        model = CMDBMonitored
        fields =  "__all__"  

###CMDBInstanceProduct###
class CMDBInstanceProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CMDBInstanceProduct
        fields =  "__all__" 

###ConfigMultipurpose###
class ConfigMultipurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigMultipurpose
        fields =  "__all__"  

###CMDBDBProduct###
class CMDBDatabaseProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CMDBDatabaseProduct
        fields =  "__all__"  

###OraTablespace###
class OraTablespaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OraTablespace
        fields = "__all__"  

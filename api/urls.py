from django.urls import include, path, re_path
from django.views.generic.base import RedirectView
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token  # <-- Here

from . import views


router = routers.SimpleRouter()
#router.register(r"vmguard", views.GuardianofthevgalaxyView)  
router.register(r"CMDBDatabaseProduct", views.CMDBDatabaseProductView) 
router.register(r"ConfigMultipurpose", views.ConfigMultipurposeView) 
router.register(r"CMDBInstanceProduct", views.CMDBInstanceProductView) 
router.register(r"CMDBMonitored", views.CMDBMonitoredView) 
router.register(r"CMDBSite", views.CMDBSiteView)
router.register(r"CMDBManufacturer", views.CMDBManufacturerView)
router.register(r"CMDBPrimaryfunction", views.CMDBPrimaryfunctionView)
router.register(r"CMDBUrgency", views.CMDBUrgencyView)
router.register(r"CMDBUsage", views.CMDBUsageView)
router.register(r"CMDBStatus", views.CMDBStatusView)
router.register(r"CMDBHostProduct", views.CMDBHostProductView)
router.register(r"Host", views.HostView)
router.register(r"HostParameter", views.HostParameterView)
router.register(r"Instance", views.InstanceView)
router.register(r"InstanceParameter", views.InstanceParameterView)
router.register(r"Instance_account", views.Instance_accountView)
router.register(r"Instance_accountParameter", views.Instance_accountParameterView)
router.register(r"Db", views.DbView)
router.register(r"DbParameter", views.DbParameterView)
router.register(r"Database_account", views.Database_accountView)
router.register(r"Database_accountParameter", views.Database_accountParameterView)
router.register(r"OraTablespace", views.OraTablespaceView)

urlpatterns = [
    re_path(r'^(?P<version>v1)/swagger(?P<format>\.json|\.yaml)$',
        views.schema_view.without_ui(cache_timeout=0), 
        name='schema-json'),
    re_path(r'^(?P<version>v1)/swagger/$', 
        views.schema_view.with_ui('swagger', cache_timeout=0), 
        name='schema-swagger-ui'),
    re_path(r'^v1/redoc/$', 
        views.schema_view.with_ui('redoc', cache_timeout=0), 
        name='schema-redoc'),
    re_path(r"(?P<version>v1)/", include(router.urls), name="v1"),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r"(?P<version>v1)/generateApiToken/", obtain_auth_token, name='api_token_auth'),
   # re_path(r"v1/insertcmdbhost/",views.insertcmdbhost),
   # re_path(r"v1/put/",views.put),
    re_path(r"v1/host_request/",views.hostrequest),
    re_path(r"v1/instance_request/",views.instancerequest),
    re_path(r"v1/instanceaccount_request/", views.instanceaccountrequest),
    re_path(r"v1/database_request/", views.databaserequest),
    re_path(r"v1/databaseaccount_request/", views.databaseaccountrequest),
    re_path(r"v1/account_list/", views.accountlist),
]
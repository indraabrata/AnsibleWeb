from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static
from .views import PostInventoryGroup, dhcp_all, ipstatic, ospf_all, conf_vlan, PostInventoryHost, namecisco, vlancisco, ospfcisco, backupcisco, restorecisco, namehuawei, ospfhuawei, ivlan_huawei, backuphuawei, namemikrotik, ipaddmtk, ospf_mikrotik, backupmikrotik, topologi, restorehuawei, restoremikrotik, infodevice, addportdevice, prekonfig, prenewdevice,arpconfig

urlpatterns = [
    path('', views.home, name='Ansible-home'),
    path('topologi/', views.topologi, name='topologi'),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('group/', views.addgroup, name='group-create'),
    path('host/', views.addhost, name='host-create'),
    path('vlan/', views.conf_vlan, name='vlan'),
    path('ipstatic/', views.ipstatic, name='ipstatic'),
    path('ospf/', views.ospf_all, name='ospf'),
    path('dhcp/', views.dhcp_all, name='dhcp'),
    path('playbook/', views.addPlaybook, name='playbook-create'),
    path('about/', views.about, name='Ansible-about'),
    path('addportdevice/', views.addportdevice, name='port-device'),
    path('device/', views.devicess, name='device'),
    path('autoconfig/', views.arpconfig, name='arp'),
    path('prenewdevice/<str:pk>/', views.prenewdevice, name='prenewdevice'),
    path('preconf/<str:pk>/', views.prekonfig, name='prekonfig'),
    path('infodevice/<str:pk>/', views.infodevice, name='info-device'),
    path('update_device/<str:pk>/', views.updatedevice, name='update-device'),
    path('delete_device/<int:id>/', views.deletedevice, name='delete-device'),
    path('log/', views.log_info, name='log-report'),
    path('update_group/<str:pk>/', views.updategroup, name='update-group'),
    path('delete_group/<int:id>/', views.deletegroup, name='delete-group'),
    path('namecisco/', views.namecisco, name='name-cisco'),
    path('vlancisco/', views.vlancisco, name='vlan-cisco'),
    path('ospfcisco/', views.ospfcisco, name='ospf-cisco'),
    path('backupcisco/', views.backupcisco, name='backup-cisco'),
    path('restorecisco/', views.restorecisco, name='restore-cisco'),
    path('namehuawei/', views.namehuawei, name='name-huawei'),
    path('ospfhuawei/', views.ospfhuawei, name='ospf-huawei'),
    path('ivlanhuawei/', views.ivlan_huawei, name='ivlan-huawei'),
    path('backuphuawei/', views.backuphuawei, name='backup-huawei'),
    path('restorehuawei/', views.restorehuawei, name='restore-huawei'),
    path('namemikrotik/', views.namemikrotik, name='name-mikrotik'),
    path('ipaddmtk/', views.ipaddmtk, name='ipadd-mikrotik'),
    path('ospf_mikrotik/', views.ospfmikrotik, name='ospf-mikrotik'),
    path('backupmikrotik/', views.backupmikrotik, name='backup-mikrotik'),
    path('restoremikrotik/', views.restoremikrotik, name='restore-mikrotik')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
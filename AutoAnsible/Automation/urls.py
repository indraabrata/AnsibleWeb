from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static 
from .view import intervlan, dhcp, ospf, ipstatic, vlan, device, autoconfig, backup, restore

urlpatterns = [
    path('', views.home, name='Ansible-home'),
    path('topologi/', views.topologi, name='topologi'),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('group/', views.addgroup, name='group-create'),
    path('host/', device.addhost, name='host-create'),
    path('vlan/', vlan.conf_vlan, name='vlan'),
    path('ipstatic/', ipstatic.ipstatic, name='ipstatic'),
    path('ospf/', ospf.ospf_all, name='ospf'),
    path('ivlan/', intervlan.ivlan_all, name='ivlan'),
    path('dhcp/', dhcp.dhcp_all, name='dhcp'),
    path('about/', views.about, name='Ansible-about'),
    path('addportdevice/', device.addportdevice, name='port-device'),
    path('device/', views.devicess, name='device'),
    path('autoconfig/', autoconfig.arpconfig, name='arp'),
    path('prenewdevice/<str:pk>/', views.prenewdevice, name='prenewdevice'),
    path('preconf/<str:pk>/', views.prekonfig, name='prekonfig'),
    path('infodevice/<str:pk>/', views.infodevice, name='info-device'),
    path('update_device/<str:pk>/', views.updatedevice, name='update-device'),
    path('delete_device/<int:id>/', views.deletedevice, name='delete-device'),
    path('log/', views.log_info, name='log-report'),
    path('update_group/<str:pk>/', views.updategroup, name='update-group'),
    path('delete_group/<int:id>/', views.deletegroup, name='delete-group'),
    path('restorecisco/', restore.restorecisco, name='restore-cisco'),
    path('backuphuawei/', backup.backup_all, name='backup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
import django_filters

from .models import *

class DeviceFilter(django_filters.FilterSet):
    class Meta:
        model = AnsibleNetworkHost
        fields = '__all__'
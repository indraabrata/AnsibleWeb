from django.db import models
from dj_ansible.models import AnsibleNetworkHost,AnsibleNetworkGroup
from django.forms import ModelForm ,CheckboxInput, ModelChoiceField
from django import forms
from .models import c_hostname

class hostnamecisco(ModelForm):
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkGroup.objects.all().filter(ansible_network_os='ios'), to_field_name="name")
    class Meta:
        model = c_hostname
        fields = ['name','hosts']
        widgets = {
            'name': forms.Textarea(attrs={'cols':100, 'rows':1})
        }

class vlan_cisco(forms.Form):
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkGroup.objects.all().filter(ansible_network_os='ios'), to_field_name="name")
    vlan_id = forms.CharField()
    vlan_name = forms.CharField()

class ospf_cisco(forms.Form):
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkGroup.objects.all().filter(ansible_network_os='ios'), to_field_name="name")
    parents = forms.CharField()
    lines = forms.CharField()

class ciscobackup(forms.Form):
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkGroup.objects.all().filter(ansible_network_os='ios'), to_field_name="name")

class ciscorestore(forms.Form):
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkGroup.objects.all().filter(ansible_network_os='ios'), to_field_name="name")

#HUAWEI FORM ----------------------------------------

class hostnamehuawei(forms.Form):
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkGroup.objects.all().filter(ansible_network_os='ce'), to_field_name="name")
    hostname = forms.CharField()

class ospf_huawei(forms.Form):
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkGroup.objects.all().filter(ansible_network_os='ce'), to_field_name="name")
    area = forms.CharField()
    network = forms.CharField()

class intervlan_huawei(forms.Form):
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkGroup.objects.all().filter(ansible_network_os='ce'), to_field_name="name")
    interface = forms.CharField()
    ipadd = forms.CharField()
    cmd = forms.CharField()

class huaweibackup(forms.Form):
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkGroup.objects.all().filter(ansible_network_os='ce'), to_field_name="name")

class huaweirestore(forms.Form):
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkGroup.objects.all().filter(ansible_network_os='ce'), to_field_name="name")


#MIKROTIK FORM -------------------------------------
class hostnamemikrotik(forms.Form):
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkGroup.objects.all().filter(ansible_network_os='routeros'), to_field_name="name")
    hostname = forms.CharField()

class ipaddmikrotik(forms.Form):
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkGroup.objects.all().filter(ansible_network_os='routeros'), to_field_name="name")
    ipadd = forms.CharField()
    interface = forms.CharField()

AREA_OSPF = (
    ('backbone', 'backbone'),
    ('standart', 'standart'),
    ('nssa', 'nssa'),
    ('stub', 'stub')
)

class ospf_mikrotik(forms.Form):
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkGroup.objects.all().filter(ansible_network_os='routeros'), to_field_name="name")
    network = forms.CharField()
    area = forms.ChoiceField(choices=AREA_OSPF) 

class mikrotikbackup(forms.Form):
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkGroup.objects.all().filter(ansible_network_os='routeros'), to_field_name="name")

class mikrotikrestore(forms.Form):
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkGroup.objects.all().filter(ansible_network_os='routeros'), to_field_name="name")


#AUTOCONFIGURATION FORM------------
class autoconfig(forms.Form):
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkHost.objects.all())


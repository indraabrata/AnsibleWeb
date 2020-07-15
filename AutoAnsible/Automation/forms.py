from django.db import models
from dj_ansible.models import AnsibleNetworkHost,AnsibleNetworkGroup
from django.forms import ModelForm ,CheckboxInput, ModelChoiceField, formset_factory
from django import forms
from .models import c_hostname

class hostnamecisco(ModelForm):
    oss = AnsibleNetworkGroup.objects.all().filter(ansible_network_os='ios')
    os = oss[0]
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkHost.objects.all().filter(group_id=os), to_field_name="host")
    class Meta:
        model = c_hostname
        fields = ['name','hosts']
        widgets = {
            'name': forms.Textarea(attrs={'cols':100, 'rows':1})
        }

class vlan_cisco(forms.Form):
    oss = AnsibleNetworkGroup.objects.all().filter(ansible_network_os='ios')
    os = oss[0]
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkHost.objects.all().filter(group_id=os), to_field_name="host")
    vlan_id = forms.CharField()
    vlan_name = forms.CharField()

class ospf_cisco(forms.Form):
    oss = AnsibleNetworkGroup.objects.all().filter(ansible_network_os='ios')
    os = oss[0]
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkHost.objects.all().filter(group_id=os), to_field_name="host")
    parents = forms.CharField()
    lines = forms.CharField()

class ciscobackup(forms.Form):
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkGroup.objects.all().filter(ansible_network_os='ios'), to_field_name="name")

class ciscorestore(forms.Form):
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkGroup.objects.all().filter(ansible_network_os='ios'), to_field_name="name")

#HUAWEI FORM ----------------------------------------

class hostnamehuawei(forms.Form):
    oss = AnsibleNetworkGroup.objects.all().filter(ansible_network_os='ce')
    os = oss[0]
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkHost.objects.all().filter(group_id=os), to_field_name="host")
    hostname = forms.CharField()

class ospf_huawei(forms.Form):
    oss = AnsibleNetworkGroup.objects.all().filter(ansible_network_os='ce')
    os = oss[0]
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkHost.objects.all().filter(group_id=os), to_field_name="host")
    area = forms.CharField()
    network = forms.CharField()

class intervlan_huawei(forms.Form):
    oss = AnsibleNetworkGroup.objects.all().filter(ansible_network_os='ce')
    os = oss[0]
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkHost.objects.all().filter(group_id=os), to_field_name="host")
    interface = forms.CharField()
    ipadd = forms.CharField()
    cmd = forms.CharField()

class huaweibackup(forms.Form):
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkGroup.objects.all().filter(ansible_network_os='ce'), to_field_name="name")

class huaweirestore(forms.Form):
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkGroup.objects.all().filter(ansible_network_os='ce'), to_field_name="name")


#MIKROTIK FORM -------------------------------------
class hostnamemikrotik(forms.Form):
    oss = AnsibleNetworkGroup.objects.all().filter(ansible_network_os='routeros')
    os = oss[0]
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkHost.objects.all().filter(group_id=os), to_field_name="host")
    hostname = forms.CharField()

class ipaddmikrotik(forms.Form):
    oss = AnsibleNetworkGroup.objects.all().filter(ansible_network_os='routeros')
    os = oss[0]
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkHost.objects.all().filter(group_id=os), to_field_name="host")
    ipadd = forms.CharField()
    interface = forms.CharField()

AREA_OSPF = (
    ('backbone', 'backbone'),
    ('standart', 'standart'),
    ('nssa', 'nssa'),
    ('stub', 'stub')
)

class ospf_mikrotik(forms.Form):
    oss = AnsibleNetworkGroup.objects.all().filter(ansible_network_os='routeros')
    os = oss[0]
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkHost.objects.all().filter(group_id=os), to_field_name="host")
    network = forms.CharField()
    area = forms.ChoiceField(choices=AREA_OSPF) 

class mikrotikbackup(forms.Form):
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkGroup.objects.all().filter(ansible_network_os='routeros'), to_field_name="name")

class mikrotikrestore(forms.Form):
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkGroup.objects.all().filter(ansible_network_os='routeros'), to_field_name="name")


#AUTOCONFIGURATION FORM------------
class autoconfig(forms.Form):
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkHost.objects.all())


class host_all(forms.Form):
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkHost.objects.all(), to_field_name="host")

class vlan(forms.Form):
    vlan_id = forms.CharField(required=False)
    vlan_name = forms.CharField(required=False)
    interface = forms.CharField(required=False)

class vlan_int(forms.Form):
    int_vlan = forms.CharField(required=False)
    c_vlan = forms.CharField(required=False)

class ip_static(forms.Form):
    interface = forms.CharField(required=False)
    ip_add = forms.CharField(required=False)

class ospf(forms.Form):
    area = forms.CharField(required=False)
    network = forms.CharField(required=False)

class dhcp(forms.Form):
    pool = forms.CharField(required=False)
    interface = forms.CharField(required=False)
    network = forms.CharField(required=False)
    mask = forms.CharField(required=False)
    gateway = forms.CharField(required=False)
    excluded = forms.CharField(required=False)

dhcpset = formset_factory(dhcp, extra=1)
ospfset = formset_factory(ospf, extra=1)
ip_staticset = formset_factory(ip_static, extra=1)
    
vlanset = formset_factory(vlan, extra=1)
vlanint = formset_factory(vlan_int, extra=1)
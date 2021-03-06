from django.db import models
from dj_ansible.models import AnsibleNetworkHost,AnsibleNetworkGroup
from django.forms import ModelForm ,CheckboxInput, ModelChoiceField
from django import forms
from .playbook import Actions, PlayBook
# Create your models here.

#class MyModelChoiceField(ModelChoiceField):
#    def label_from_instance(self, obj):
#        return "My Object #%i" % obj.name
OS_CHOICES =(
    ('ios', 'Cisco'),
    ('routeros', 'Mikrotik'),
    ('ce', 'Huawei')
)

DEVICE_CHOICES=(
    ('router', 'Router'),
    ('switch', 'Switch')
)

class PostInventoryGroup(ModelForm):
    ansible_network_os = forms.ChoiceField(choices = OS_CHOICES)
    class Meta:
        model = AnsibleNetworkGroup
        fields = ['name', 'ansible_connection', 'ansible_network_os', 'ansible_become']
        widgets = {
            'name': forms.Textarea(attrs={'cols':100, 'rows':1}),
        #   'ansible_connection': forms.Textarea(attrs={'cols':100, 'rows':1}),
            'ansible_network_os': forms.Textarea(attrs={'cols':100, 'rows':1}),
            'ansible_become': forms.Textarea(attrs={'cols':100, 'rows':1})
        }

class PostInventoryHost(ModelForm):
    group = forms.ModelChoiceField(queryset=AnsibleNetworkGroup.objects.all())
    device_type = forms.ChoiceField(choices = DEVICE_CHOICES)
    class Meta:
        model = AnsibleNetworkHost
        fields = ['host', 'ansible_ssh_host', 'ansible_user', 'ansible_ssh_pass', 'ansible_become_pass', 'device_type', 'group']
        widgets = {
            'host': forms.Textarea(attrs={'cols':100, 'rows':1}),
            'ansible_ssh_host': forms.Textarea(attrs={'cols':100, 'rows':1}),
            'ansible_user': forms.Textarea(attrs={'cols':100, 'rows':1}),
            'ansible_ssh_pass': forms.Textarea(attrs={'cols':100, 'rows':1}),
            'ansible_become_pass': forms.Textarea(attrs={'cols':100, 'rows':1})
        }
    
class PostPlayBookForm(ModelForm):
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkGroup.objects.all(), to_field_name="name")
    class Meta:
        model = PlayBook
        fields = ['name', 'hosts', 'become','become_method','gather_facts']
        exclude = ('task',)
        widgets = {
            'name': forms.Textarea(attrs={'cols':100, 'rows':1}),
            'become': forms.Textarea(attrs={'cols':100, 'rows':1}),
            'become_method': forms.Textarea(attrs={'cols':100, 'rows':1}),
            'gather_facts': forms.Textarea(attrs={'cols':100, 'rows':1})
        }

class TaskForm(ModelForm):
    class Meta:
        model = Actions
        fields = ['module', 'commands']
        widgets = {
            'module': forms.Textarea(attrs={'cols':100, 'rows':1}),
            'commands': forms.Textarea(attrs={'cols':100, 'rows':1})
        }

class log(models.Model):
    account = models.CharField(max_length=255, default="")
    targetss = models.CharField(max_length=255, default="")
    action = models.CharField(max_length=255, default="")
    status = models.CharField(max_length=255, default="")
    time = models.CharField(max_length=255, default="")
    messages = models.CharField(max_length=255, default="")

    def __str__(self):
        return "{} - {} - {}".format(self.targetss, self.action, self.status)

class c_hostname(models.Model):
    name = models.CharField(max_length=255)
    hosts = models.CharField(max_length=255)

class group(forms.Form):
    name = forms.CharField(max_length=255)
    os = forms.ChoiceField(choices = OS_CHOICES)

class addinfodevice(forms.Form):
    hosts = forms.ModelChoiceField(queryset=AnsibleNetworkHost.objects.all())

class ios_router(forms.Form):
    name = forms.CharField()
    mac = forms.CharField()

    port_ip = forms.CharField()
    port_cmd = forms.CharField()
    port_mask = forms.CharField()

    i_vlan_int = forms.CharField()
    i_vlan_enc = forms.CharField()
    i_vlan_cmd = forms.CharField()
    i_vlan_mask = forms.CharField()

    i_vlan_int2 = forms.CharField()
    i_vlan_enc2 = forms.CharField()
    i_vlan_cmd2 = forms.CharField()
    i_vlan_mask2 = forms.CharField()


    ospf_area = forms.CharField()
    ospf_network = forms.CharField()
    ospf_mask = forms.CharField()

    ospf_area2 = forms.CharField()
    ospf_network2 = forms.CharField()
    ospf_mask2 = forms.CharField()

    ospf_area3 = forms.CharField()
    ospf_network3 = forms.CharField()
    ospf_mask3 = forms.CharField()


    dhcp_pool = forms.CharField()
    default_router = forms.CharField()
    dhcp_network = forms.CharField()
    dhcp_mask = forms.CharField()
    dhcp_excluded = forms.CharField()

    dhcp_pool2 = forms.CharField()
    default_router2 = forms.CharField()
    dhcp_network2 = forms.CharField()
    dhcp_mask2 = forms.CharField()
    dhcp_excluded2 = forms.CharField()

    dhcp_pool3 = forms.CharField()
    default_router3 = forms.CharField()
    dhcp_network3 = forms.CharField()
    dhcp_mask3 = forms.CharField()
    dhcp_excluded3 = forms.CharField()

    default_gateway = forms.CharField()
    


class preconfdevice(forms.Form):
    tipe = forms.ChoiceField(choices= DEVICE_CHOICES)

class arp(models.Model):
    ipadd = models.CharField(max_length=255, default="")
    mac = models.CharField(max_length=255, default="")
    port = models.CharField(max_length=255, default="")
    device_id = models.ForeignKey(AnsibleNetworkHost, on_delete=models.CASCADE)

class devices(models.Model):
    port = models.CharField(max_length=100)
    ipadd = models.CharField(max_length=100, default="")
    physical = models.CharField(max_length=100, default="")
    protocol = models.CharField(max_length=100, default="")
    preconf = models.CharField(max_length=100, default='empty')
    stats = models.CharField(max_length=100, default='Not Booked')
    new_device_type = models.CharField(max_length=100, default="")
    new_device_mac = models.CharField(max_length=100, default="")
    device_id = models.ForeignKey(AnsibleNetworkHost, on_delete=models.CASCADE)

class iosrouter(models.Model):
    name = models.CharField(max_length=100, default="")
    hostname = models.CharField(max_length=100, default="")

    port_ip = models.CharField(max_length=100, default="")
    port_cmd = models.CharField(max_length=100, default="")
    port_mask = models.CharField(max_length=100, default="")

    i_vlan_int = models.CharField(max_length=100, default="")
    i_vlan_enc = models.CharField(max_length=100, default="")
    i_vlan_cmd = models.CharField(max_length=100, default="")
    i_vlan_mask = models.CharField(max_length=10, default="")

    i_vlan_int2 = models.CharField(max_length=100, default="")
    i_vlan_enc2 = models.CharField(max_length=100, default="")
    i_vlan_cmd2 = models.CharField(max_length=100, default="")
    i_vlan_mask2 = models.CharField(max_length=10, default="")

    ospf_area = models.CharField(max_length=100, default="")
    ospf_network = models.CharField(max_length=100, default="")
    ospf_mask = models.CharField(max_length=100, default="")

    ospf_area2 = models.CharField(max_length=100, default="")
    ospf_network2 = models.CharField(max_length=100, default="")
    ospf_mask2 = models.CharField(max_length=100, default="")

    ospf_area3 = models.CharField(max_length=100, default="")
    ospf_network3 = models.CharField(max_length=100, default="")
    ospf_mask3 = models.CharField(max_length=100, default="")


    dhcp_pool = models.CharField(max_length=100, default="")
    default_router = models.CharField(max_length=100, default="")
    dhcp_network = models.CharField(max_length=100, default="")
    dhcp_mask = models.CharField(max_length=100, default="")
    dhcp_excluded = models.CharField(max_length=100, default="")

    dhcp_pool2 = models.CharField(max_length=100, default="")
    default_router2 = models.CharField(max_length=100, default="")
    dhcp_network2 = models.CharField(max_length=100, default="")
    dhcp_mask2 = models.CharField(max_length=100, default="")
    dhcp_excluded2 = models.CharField(max_length=100, default="")

    dhcp_pool3 = models.CharField(max_length=100, default="")
    default_router3 = models.CharField(max_length=100, default="")
    dhcp_network3 = models.CharField(max_length=100, default="")
    dhcp_mask3 = models.CharField(max_length=100, default="")
    dhcp_excluded3 = models.CharField(max_length=100, default="")

    default_gateway = models.CharField(max_length=100, default="")

    port_id = models.ForeignKey(devices, on_delete=models.CASCADE)

class kamusport(models.Model):
    portarp = models.CharField(max_length=255)
    portint = models.CharField(max_length=255)

class ios_switch(models.Model):
    name = models.CharField(max_length=100, default="")
    hostname = models.CharField(max_length=100, default="")
    mac = models.CharField(max_length=100, default="")

    vlan_id = models.CharField(max_length=100, default="")
    vlan_name = models.CharField(max_length=100, default="")

    vlan_id2 = models.CharField(max_length=100, default="")
    vlan_name2 = models.CharField(max_length=100, default="")

    vlan_id3 = models.CharField(max_length=100, default="")
    vlan_name3 = models.CharField(max_length=100, default="")

    interface = models.CharField(max_length=100, default="")
    mode = models.CharField(max_length=100, default="")
    vlan = models.CharField(max_length=100, default="")

    interface2 = models.CharField(max_length=100, default="")
    mode2 = models.CharField(max_length=100, default="")
    vlan2 = models.CharField(max_length=100, default="")

    interface3 = models.CharField(max_length=100, default="")
    mode3 = models.CharField(max_length=100, default="")
    vlan3 = models.CharField(max_length=100, default="")

    gateway = models.CharField(max_length=100, default="")

    port_id = models.ForeignKey(devices, on_delete=models.CASCADE)


class switchservice(models.Model):
    namefile = models.CharField(max_length=100, default="")
    vlan_id = models.CharField(max_length=100, default="")
    vlan_name = models.CharField(max_length=100, default="")

    vlan_id2 = models.CharField(max_length=100, default="")
    vlan_name2 = models.CharField(max_length=100, default="")

    vlan_id3 = models.CharField(max_length=100, default="")
    vlan_name3 = models.CharField(max_length=100, default="")

    interface = models.CharField(max_length=100, default="")
    mode = models.CharField(max_length=100, default="")
    vlan = models.CharField(max_length=100, default="")

    interface2 = models.CharField(max_length=100, default="")
    mode2 = models.CharField(max_length=100, default="")
    vlan2 = models.CharField(max_length=100, default="")

    interface3 = models.CharField(max_length=100, default="")
    mode3 = models.CharField(max_length=100, default="")
    vlan3 = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.namefile

class ios_switch_form(forms.Form):
    name = forms.CharField()
    mac = forms.CharField()
    form = forms.ModelChoiceField(queryset=switchservice.objects.all(), to_field_name="namefile")
    gateway = forms.CharField()


class formswitch(forms.Form):
    namefile = forms.CharField()
    vlan_id = forms.CharField()
    vlan_name = forms.CharField()

    vlan_id2 = forms.CharField()
    vlan_name2 = forms.CharField()

    vlan_id3 = forms.CharField()
    vlan_name3 = forms.CharField()

    interface = forms.CharField()
    mode = forms.CharField()
    vlan = forms.CharField()

    interface2 = forms.CharField()
    mode2 = forms.CharField()
    vlan2 = forms.CharField()

    interface3 = forms.CharField()
    mode3 = forms.CharField()
    vlan3 = forms.CharField()


class mac_os(models.Model):
    oui = models.CharField(max_length=50)
    vendor = models.CharField(max_length=50)

    @classmethod
    def create(cls, **kwargs):
        macos= cls.objects.create(
            oui=kwargs['oui'],
            vendor=kwargs['vendor']
        )











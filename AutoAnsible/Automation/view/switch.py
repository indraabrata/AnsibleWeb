from __future__ import absolute_import, unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from ..models import mac_os, switchservice, formswitch, PostInventoryGroup, PostInventoryHost ,PostPlayBookForm, TaskForm, log, group, addinfodevice , ios_router, preconfdevice, arp, kamusport, ios_switch, ios_switch_form, devices, iosrouter
from ..forms import ivlanset, hostnamecisco, dhcpset, ospfset, ip_staticset, vlanint, vlan_cisco, ospf_cisco, ciscobackup, ciscorestore, hostnamehuawei, ospf_huawei, intervlan_huawei, hostnamemikrotik, ipaddmikrotik, ospf_mikrotik, mikrotikbackup, huaweirestore, mikrotikrestore, autoconfig , vlanset, host_all
from django.contrib import messages
#from djansible.models import PlayBooks
from itertools import chain
from dj_ansible.models import AnsibleNetworkHost
from dj_ansible.ansible_kit import execute
import json
from datetime import datetime
import time
import threading
from django.contrib.auth.models import User

@login_required
def serviceswitch(request):
    if request.method == 'POST':
        form = formswitch(request.POST, request.user)
        if form.is_valid():
            data = request.POST
            akun = request.user
            service = switchservice(
                namefile=data['namefile'],
                vlan_id=data['vlan_id'],
                vlan_name=data['vlan_name'],
                vlan_id2=data['vlan_id2'],
                vlan_name2=data['vlan_name2'],
                vlan_id3=data['vlan_id3'],
                vlan_name3=data['vlan_name3'],
                interface=data['interface'],
                mode=data['mode'],
                vlan=data['vlan'],
                interface2=data['interface2'],
                mode2=data['mode2'],
                vlan2=data['vlan2'],
                interface3=data['interface3'],
                mode3=data['mode3'],
                vlan3=data['vlan3'])
            service.save()
            logs = log(account=akun, targetss="Preconf Switch", action='Add Switch Service', status='Success', time=datetime.now(), messages='No Error')
            logs.save()
            messages.success(request, f'Success creating switch service')
            context = {
                'form': form
            }
            return render(request, 'ansibleweb/switchform.html', context)
    else:
        form = formswitch()
    
    context = {
        'form': form
    }
    return render(request, 'ansibleweb/switchform.html', context)



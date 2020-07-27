from __future__ import absolute_import, unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from ..models import mac_os, PostInventoryGroup, PostInventoryHost ,PostPlayBookForm, TaskForm, log, group, addinfodevice , ios_router, preconfdevice, arp, ce_router_form, ce_router, kamusport, ios_switch, ios_switch_form, devices, iosrouter, ce_switch, ce_switch_form, routeros_router, routeros_router_form
from ..forms import ivlanset, hostnamecisco, dhcpset, ospfset, ip_staticset, vlanint, vlan_cisco, ospf_cisco, ciscobackup, ciscorestore, hostnamehuawei, ospf_huawei, intervlan_huawei,hostnamemikrotik, ipaddmikrotik, ospf_mikrotik, mikrotikbackup, huaweirestore, mikrotikrestore, autoconfig , vlanset, host_all
from django.contrib import messages
from itertools import chain
from dj_ansible.models import AnsibleNetworkHost
from dj_ansible.ansible_kit import execute
import json
from datetime import datetime
import time
import threading
from django.contrib.auth.models import User

@login_required
def ospf_all(request):
    if request.method == 'POST':
        form_host = host_all(request.POST, request.user)
        ospfs = ospfset(request.POST)
        if form_host.is_valid() and ospfs.is_valid():
            output = []
            data = request.POST
            akun = request.user
            hoss = AnsibleNetworkHost.objects.get(host=data['hosts'])
            os = hoss.group.ansible_network_os
            if os == 'ce':
                for form in ospfs:
                    area = form.cleaned_data.get('area')
                    network = form.cleaned_data.get('network')
                    mask = form.cleaned_data.get('mask')
                    my_play = dict(
                        name="Config OSPF",
                        hosts=data['hosts'],
                        become='yes',
                        become_method='enable',
                        gather_facts='no',
                        vars=[
                            dict(ansible_command_timeout=120)
                        ],
                        tasks=[
                            dict(action=dict(module='ce_config', lines=['ospf', 'area '+area, 'network '+network+' '+mask]))
                        ]
                    )
                    print(my_play)
                    result = execute(my_play)
                    kond = result.stats
                    kondisi = kond['hosts'][0]['status']
                    hos = kond['hosts'][0]['host']
                    if kondisi == 'ok':
                        dataport = result.results                
                        command = dataport['success'][0]['tasks'][0]['result']['commands'][0]
                        berhasil = dataport['success'][0]['tasks'][0]['result']['changed']
                        logs = log(account=akun, targetss=hos, action='Configure OSPF '+hos, status='Success', time=datetime.now(), messages='No Error')
                        logs.save()
                        jadi = "Device   :"+hos+"    Commands:"+command+"    Changed: True"
                        output.append(jadi)      
                    else:
                        dataport = result.results
                        err = dataport['failed'][0]['tasks'][0]['result']['msg']
                        logs = log(account=akun, targetss=hos, action='Configure OSPF '+hos, status='Failed', time=datetime.now(), messages=err)
                        logs.save()
                        gagal = "Device   :"+hos+"    Output:"+err
                        output.append(gagal)
                context = {
                    'form_host': form_host,
                    'ospfs': ospfs,
                    'output': output
                }
                return render(request, 'ansibleweb/ospf.html', context)
            if os == 'ios':
                for form in ospfs:
                    area = form.cleaned_data.get('area')
                    network = form.cleaned_data.get('network')
                    mask = form.cleaned_data.get('mask')
                    my_play = dict(
                        name="Config OSPF",
                        hosts=data['hosts'],
                        become='yes',
                        become_method='enable',
                        gather_facts='no',
                        vars=[
                            dict(ansible_command_timeout=120)
                        ],
                        tasks=[
                            dict(action=dict(module='ios_config', lines=['network '+network+' '+mask+' area '+area], parents='router ospf 1'))
                        ]
                    )
                    print(my_play)
                    result = execute(my_play)
                    kond = result.stats
                    kondisi = kond['hosts'][0]['status']
                    hos = kond['hosts'][0]['host']
                    if kondisi == 'ok':
                        dataport = result.results                
                        command = dataport['success'][0]['tasks'][0]['result']['commands'][0]
                        berhasil = dataport['success'][0]['tasks'][0]['result']['changed']
                        logs = log(account=akun, targetss=hos, action='Configure OSPF '+hos, status='Success', time=datetime.now(), messages='No Error')
                        logs.save()
                        jadi = "Device   :"+hos+"    Commands:"+command+"    Changed: True"
                        output.append(jadi)      
                    else:
                        dataport = result.results
                        err = dataport['failed'][0]['tasks'][0]['result']['msg']
                        logs = log(account=akun, targetss=hos, action='Configure OSPF '+hos, status='Failed', time=datetime.now(), messages=err)
                        logs.save()
                        gagal = "Device   :"+hos+"    Output:"+err
                        output.append(gagal)
                context = {
                    'form_host': form_host,
                    'ospfs': ospfs,
                    'output': output
                }
                return render(request, 'ansibleweb/ospf.html', context)
            if os == 'routeros':
                for form in ospfs:
                    area = form.cleaned_data.get('area')
                    network = form.cleaned_data.get('network')
                    mask = form.cleaned_data.get('mask')
                    my_play = dict(
                        name="Config OSPF",
                        hosts=data['hosts'],
                        become='yes',
                        become_method='enable',
                        gather_facts='no',
                        vars=[
                            dict(ansible_command_timeout=120)
                        ],
                        tasks=[
                            dict(action=dict(module='routeros_command', commands='/routing ospf network add network='+network+'/'+mask+' area='+area))
                        ]
                    )
                    print(my_play)
                    result = execute(my_play)
                    kond = result.stats
                    kondisi = kond['hosts'][0]['status']
                    hos = kond['hosts'][0]['host']
                    if kondisi == 'ok':
                        dataport = result.results                
                        command = dataport['success'][0]['tasks'][0]['result']['commands'][0]
                        berhasil = dataport['success'][0]['tasks'][0]['result']['changed']
                        logs = log(account=akun, targetss=hos, action='Configure OSPF '+hos, status='Success', time=datetime.now(), messages='No Error')
                        logs.save()
                        jadi = "Device   :"+hos+"    Commands:"+command+"    Changed: True"
                        output.append(jadi)      
                    else:
                        dataport = result.results
                        err = dataport['failed'][0]['tasks'][0]['result']['msg']
                        logs = log(account=akun, targetss=hos, action='Configure OSPF '+hos, status='Failed', time=datetime.now(), messages=err)
                        logs.save()
                        gagal = "Device   :"+hos+"    Output:"+err
                        output.append(gagal)
                context = {
                    'form_host': form_host,
                    'ospfs': ospfs,
                    'output': output
                }
                return render(request, 'ansibleweb/ospf.html', context)
    else:
        form_host = host_all()
        ospfs = ospfset()
    
    context = {
        'form_host': form_host,
        'ospfs': ospfs,
    }
    return render(request, 'ansibleweb/ospf.html', context)
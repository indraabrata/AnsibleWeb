from __future__ import absolute_import, unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from ..models import mac_os, PostInventoryGroup, PostInventoryHost ,PostPlayBookForm, TaskForm, log, group, addinfodevice , ios_router, preconfdevice, arp, ce_router_form, ce_router, kamusport, ios_switch, ios_switch_form, devices, iosrouter, ce_switch, ce_switch_form, routeros_router, routeros_router_form
from ..forms import ivlanset, hostnamecisco, dhcpset, ospfset, ip_staticset, vlanint, vlan_cisco, ospf_cisco, ciscobackup, ciscorestore, hostnamehuawei, ospf_huawei, intervlan_huawei, hostnamemikrotik, ipaddmikrotik, ospf_mikrotik, mikrotikbackup, huaweirestore, mikrotikrestore, autoconfig , vlanset, host_all
from django.contrib import messages
from itertools import chain
from dj_ansible.models import AnsibleNetworkHost
from dj_ansible.ansible_kit import execute
import json
from datetime import datetime
import time
import threading
from django.contrib.auth.models import User

def dhcp_all(request):
    if request.method == 'POST':
        form_host = host_all(request.POST, request.user)
        formset = dhcpset(request.POST)
        if form_host.is_valid() and formset.is_valid():
            output = []
            data = request.POST
            akun = request.user
            hoss = AnsibleNetworkHost.objects.get(host=data['hosts'])
            os = hoss.group.ansible_network_os
            if os == 'ce':
                for form in formset:
                    pool = form.cleaned_data.get('pool')
                    interface = form.cleaned_data.get('interface')
                    network = form.cleaned_data.get('network')
                    mask = form.cleaned_data.get('mask')
                    gateway = form.cleaned_data.get('gateway')
                    excluded = form.cleaned_data.get('excluded')
                    my_play = dict(
                        name="Config dhcp",
                        hosts=data['hosts'],
                        become='yes',
                        become_method='enable',
                        gather_facts='no',
                        vars=[
                            dict(ansible_command_timeout=120)
                        ],
                        tasks=[
                            dict(action=dict(module='ce_config', lines=['dhcp enable', 'ip pool '+pool, 'network '+network+' mask '+mask, 'gateway-list '+gateway, 'excluded-ip-address '+excluded])),
                            dict(action=dict(module='ce_config', lines=['int '+interface, 'ip add '+gateway+' 24', 'dhcp select interface', 'undo sh']))
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
                        logs = log(account=akun, targetss=hos, action='Configure DHCP '+hos, status='Success', time=datetime.now(), messages='No Error')
                        logs.save()
                        jadi = "Device   :"+hos+"    Commands:"+command+"    Changed: True"
                        output.append(jadi)      
                    else:
                        dataport = result.results
                        err = dataport['failed'][0]['tasks'][0]['result']['msg']
                        logs = log(account=akun, targetss=hos, action='Configure DHCP '+hos, status='Failed', time=datetime.now(), messages=err)
                        logs.save()
                        gagal = "Device   :"+hos+"    Output:"+err
                        output.append(gagal)
                context = {
                    'form_host': form_host,
                    'formset': formset,
                    'output': output
                }
                return render(request, 'ansibleweb/dhcp.html', context)
            if os == 'routeros':
                for form in formset:
                    pool = form.cleaned_data.get('pool')
                    interface = form.cleaned_data.get('interface')
                    network = form.cleaned_data.get('network')
                    mask = form.cleaned_data.get('mask')
                    gateway = form.cleaned_data.get('gateway')
                    excluded = form.cleaned_data.get('excluded')
                    my_play = dict(
                        name="Config dhcp",
                        hosts=data['hosts'],
                        become='yes',
                        become_method='enable',
                        gather_facts='no',
                        vars=[
                            dict(ansible_command_timeout=120)
                        ],
                        tasks=[
                            dict(action=dict(module='routeros_command', commands='/ip address add address='+gateway+'/'+mask+' interface='+interface)),
                            dict(action=dict(module='routeros_command', commands='/ip pool add name='+pool+' ranges='+excluded)),
                            dict(action=dict(module='routeros_command', commands='/ip dhcp-server network add address '+network+'/'+mask+' gateway='+gateway)),
                            dict(action=dict(module='routeros_command', commands='/ip dhcp-server add interface='+interface+' address-pool='+pool))
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
                        logs = log(account=akun, targetss=hos, action='Configure DHCP '+hos, status='Success', time=datetime.now(), messages='No Error')
                        logs.save()
                        jadi = "Device   :"+hos+"    Commands:"+command+"    Changed: True"
                        output.append(jadi)      
                    else:
                        dataport = result.results
                        err = dataport['failed'][0]['tasks'][0]['result']['msg']
                        logs = log(account=akun, targetss=hos, action='Configure DHCP '+hos, status='Failed', time=datetime.now(), messages=err)
                        logs.save()
                        gagal = "Device   :"+hos+"    Output:"+err
                        output.append(gagal)
                context = {
                    'form_host': form_host,
                    'formset': formset,
                    'output': output
                }
                return render(request, 'ansibleweb/dhcp.html', context) 
            if os == 'ios':
                for form in formset:
                    pool = form.cleaned_data.get('pool')
                    interface = form.cleaned_data.get('interface')
                    network = form.cleaned_data.get('network')
                    mask = form.cleaned_data.get('mask')
                    gateway = form.cleaned_data.get('gateway')
                    excluded = form.cleaned_data.get('excluded')
                    my_play = dict(
                        name="Config dhcp",
                        hosts=data['hosts'],
                        become='yes',
                        become_method='enable',
                        gather_facts='no',
                        vars=[
                            dict(ansible_command_timeout=120)
                        ],
                        tasks=[
                            dict(action=dict(module='ios_config', lines=['network +'+network+' '+mask, 'default-router '+gateway], parents='ip dhcp pool '+pool)),
                            dict(action=dict(module='ios_config', lines=['ip dhcp excluded-address '+excluded])),
                            dict(action=dict(module='ios_config', lines=['ip add '+gateway+' '+mask, 'no sh'], parents='int '+interface))
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
                        logs = log(account=akun, targetss=hos, action='Configure DHCP '+hos, status='Success', time=datetime.now(), messages='No Error')
                        logs.save()
                        jadi = "Device   :"+hos+"    Commands:"+command+"    Changed: True"
                        output.append(jadi)      
                    else:
                        dataport = result.results
                        err = dataport['failed'][0]['tasks'][0]['result']['msg']
                        logs = log(account=akun, targetss=hos, action='Configure DHCP '+hos, status='Failed', time=datetime.now(), messages=err)
                        logs.save()
                        gagal = "Device   :"+hos+"    Output:"+err
                        output.append(gagal)
                    messages.success(request, output)
                context = {
                    'form_host': form_host,
                    'formset': formset,
                    'output': output
                }
                return render(request, 'ansibleweb/dhcp.html', context)    
    else:
        form_host = host_all()
        formset = dhcpset()
    
    context = {
        'form_host': form_host,
        'formset': formset
    }
    return render(request, 'ansibleweb/dhcp.html', context)
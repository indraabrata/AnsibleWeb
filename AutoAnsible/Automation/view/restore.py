from __future__ import absolute_import, unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from ..models import mac_os, PostInventoryGroup, PostInventoryHost ,PostPlayBookForm, TaskForm, log, group, addinfodevice , ios_router, preconfdevice, arp, ce_router_form, ce_router, kamusport, ios_switch, ios_switch_form, devices, iosrouter, ce_switch, ce_switch_form, routeros_router, routeros_router_form
from ..forms import ivlanset, restoreset, hostnamecisco, dhcpset, ospfset, ip_staticset, vlanint, vlan_cisco, ospf_cisco, ciscobackup, ciscorestore, hostnamehuawei, ospf_huawei, intervlan_huawei, hostnamemikrotik, ipaddmikrotik, ospf_mikrotik, mikrotikbackup, huaweirestore, mikrotikrestore, autoconfig , vlanset, host_all
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
def restorecisco(request):
    if request.method == 'POST':
        restore = restoreset(request.POST)
        if restore.is_valid():
            print(request.POST)
            output = []
            for form in restore:
                data = request.POST
                akun = request.user
                hosts = form.cleaned_data.get('hosts')
                hos = hosts.host
                os = hosts.group.ansible_network_os
                print(os)
                print(hos)
                if os == 'ios':
                    my_play = dict(
                        name="restore",
                        hosts=hos,
                        become='yes',
                        become_method='enable',
                        gather_facts='no',
                        tasks=[
                            dict(net_put=dict(src='/home/indra/autonet/AutoAnsible/backup/{{inventory_hostname}}.config', protocol='scp', dest='flash0:/{{inventory_hostname}}.config')),
                            dict(action=dict(module='ios_command', commands=['config replace flash:{{inventory_hostname}}.config force']))
                            ]
                        )
                    result = execute(my_play)
                    kond = result.stats
                    kondisi = kond['hosts'][0]['status']
                    hos = kond['hosts'][0]['host']
                    if kondisi == 'ok':
                        dataport = result.results                
                        command = dataport['success'][0]['tasks'][0]['result']['commands'][0]
                        berhasil = dataport['success'][0]['tasks'][0]['result']['changed']
                        logs = log(account=akun, targetss=hos, action='Restore Config '+hos, status='Success', time=datetime.now(), messages='No Error')
                        logs.save()
                        jadi = "Device   :"+hos+"    Commands:"+command+"    Changed: True"
                        output.append(jadi)      
                    else:
                        dataport = result.results
                        err = dataport['failed'][0]['tasks'][0]['result']['msg']
                        logs = log(account=akun, targetss=hos, action='Restore Config '+hos, status='Failed', time=datetime.now(), messages=err)
                        logs.save()
                        gagal = "Device   :"+hos+"    Output:"+err
                        output.append(gagal)
                elif os == 'ce':
                    my_play = dict(
                        name="restore",
                        hosts=hos,
                        become='yes',
                        become_method='enable',
                        gather_facts='no',
                        vars=[
                            dict(ansible_command_timeout=120)
                        ],
                        tasks=[
                            dict(action=dict(module='cli_command', command='reset saved-configuration', prompt='Continue', answer='y'))
                        ]
                    )
                    my_play2 = dict(
                        name="restore2",
                        hosts=hos,
                        become='yes',
                        become_method='enable',
                        gather_facts='no',
                        vars=[
                            dict(ansible_command_timeout=120)
                        ],
                        tasks=[
                            dict(action=dict(module='cli_command', command='delete {{inventory_hostname}}startup.cfg', prompt='delete', answer='y'))
                        ]
                    )
                    my_play3 = dict(
                        name="restore3",
                        hosts=hos,
                        become='yes',
                        become_method='enable',
                        gather_facts='no',
                        vars=[
                            dict(ansible_command_timeout=120)
                        ],
                        tasks=[
                            dict(action=dict(module='cli_command', command='delete {{inventory_hostname}}nextup.cfg', prompt='delete', answer='y'))
                        ]
                    )
                    my_play4 = dict(
                        name="restore4",
                        hosts=hos,
                        become='yes',
                        become_method='enable',
                        gather_facts='no',
                        vars=[
                            dict(ansible_command_timeout=120)
                        ],
                        tasks=[
                            dict(net_put=dict(src='./backup/{{inventory_hostname}}.cfg', protocol='scp', dest='flash:/{{inventory_hostname}}startup.cfg'))
                        ]
                    )
                    my_play5 = dict(
                        name="restore4",
                        hosts=hos,
                        become='yes',
                        become_method='enable',
                        gather_facts='no',
                        vars=[
                            dict(ansible_command_timeout=120)
                        ],
                        tasks=[
                            dict(net_put=dict(src='./backup/{{inventory_hostname}}.cfg', protocol='scp', dest='flash:/{{inventory_hostname}}nextup.cfg'))
                        ]
                    )
                    my_play6 = dict(
                        name="restore4",
                        hosts=hos,
                        become='yes',
                        become_method='enable',
                        gather_facts='no',
                        vars=[
                            dict(ansible_command_timeout=120)
                        ],
                        tasks=[
                            dict(action=dict(module='ce_command', commands='startup saved-configuration {{inventory_hostname}}startup.cfg'))
                        ]
                    )                        
                    my_play7 = dict(
                        name="restore5",
                        hosts=hos,
                        become='yes',
                        become_method='enable',
                        gather_facts='no',
                        vars=[
                            dict(ansible_command_timeout=120)
                        ],
                        tasks=[
                            dict(action=dict(module='ce_command', commands='startup saved-configuration {{inventory_hostname}}nextup.cfg'))
                        ]
                    )
                    result = execute(my_play)
                    result2 = execute(my_play2)
                    result3 = execute(my_play3)
                    result4 = execute(my_play4)
                    result5 = execute(my_play5)
                    result6 = execute(my_play6)
                    result7 = execute(my_play7)
                    kond = result7.stats
                    kondisi = kond['hosts'][0]['status']
                    hos = kond['hosts'][0]['host']
                    print(hos)
                    print(kondisi)
                    if kondisi == 'ok':
                        dataport = result7.results
                        print(dataport)
                        logs = log(account=akun, targetss=hos, action='Restore Config '+hos, status='Success', time=datetime.now(), messages='No Error')
                        logs.save()
                        jadi = "Device   :"+hos+"    Output:Berhasil Restore    Changed: True"
                        output.append(jadi)      
                    else:
                        dataport = result7.results
                        err = dataport['failed'][0]['tasks'][0]['result']['msg']
                        logs = log(account=akun, targetss=hos, action='Restore Config '+hos, status='Failed', time=datetime.now(), messages=err)
                        logs.save()
                        gagal = "Device   :"+hos+"    Output:"+err
                        output.append(gagal)                    
                elif os == 'routeros':
                    my_play = dict(
                        name="Restore Mikrotik",
                        hosts=hos,
                        become='yes',
                        become_method='enable',
                        gather_facts='no',
                        vars=[
                            dict(ansible_command_timeout=120)
                        ],
                        tasks=[
                            dict(net_put=dict(src='./backup/{{inventory_hostname}}.backup', protocol='scp', dest='./{{inventory_hostname}}.backup')),
                            dict(action=dict(module='cli_command', command=':execute {/system backup load name=mtk2 password=mikrotik;}', prompt='Restore and reboot', answer='y'))                    
                        ]
                    )
                    result = execute(my_play)
                    kond = result.stats
                    kondisi = kond['hosts'][0]['status']
                    hos = kond['hosts'][0]['host']
                    if kondisi == 'ok':
                        dataport = result.results                
                        command = dataport['success'][0]['tasks'][0]['result']['commands'][0]
                        berhasil = dataport['success'][0]['tasks'][0]['result']['changed']
                        logs = log(account=akun, targetss=hos, action='Restore Config '+hos, status='Success', time=datetime.now(), messages='No Error')
                        logs.save()
                        jadi = "Device   :"+hos+"    Commands:"+command+"    Changed: True"
                        output.append(jadi)      
                    else:
                        dataport = result.results
                        err = dataport['failed'][0]['tasks'][0]['result']['msg']
                        logs = log(account=akun, targetss=hos, action='Restore Config '+hos, status='Failed', time=datetime.now(), messages=err)
                        logs.save()
                        gagal = "Device   :"+hos+"    Output:"+err
                        output.append(gagal)
            context = {
                'restore': restore,
                'output': output
            }
            return render(request, 'ansibleweb/restore.html', context)
    else:
        restore = restoreset()
    
    context = {
        'restore': restore
    }
    return render(request, 'ansibleweb/restore.html', context)


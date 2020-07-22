from __future__ import absolute_import, unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from ..models import mac_os, PostInventoryGroup, PostInventoryHost ,PostPlayBookForm, TaskForm, log, group, addinfodevice , ios_router, preconfdevice, arp, ce_router_form, ce_router, kamusport, ios_switch, ios_switch_form, devices, iosrouter, ce_switch, ce_switch_form, routeros_router, routeros_router_form
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

def restorecisco(request):
    if request.method == 'POST':
        restore = ciscorestore(request.POST)
        if restore.is_valid():
            print(request.POST)
            data = request.POST
            host = AnsibleNetworkHost.objects.get(host=data['hosts'])
            os = host.group.ansible_network_os
            print(os)
            print(host)
            if os == 'ios':
                my_play = dict(
                    name="restore",
                    hosts=data['hosts'],
                    become='yes',
                    become_method='enable',
                    gather_facts='no',
                    tasks=[
                        dict(net_put=dict(src='/home/indra/autonet/AutoAnsible/backup/{{inventory_hostname}}.config', protocol='scp', dest='flash0:/{{inventory_hostname}}.config')),
                        dict(action=dict(module='ios_command', commands=['config replace flash:{{inventory_hostname}}.config force']))
                        ]
                    )
                result = execute(my_play)
                #print(json.dumps(result.results, indent=4))
                output = json.dumps(result.results, indent=4)
                context = {
                    'restore': restore,
                    'output': output
                }
                return render(request, 'ansibleweb/ciscorestore.html', context)
            elif os == 'ce':
                my_play = dict(
                    name="restore",
                    hosts=data['hosts'],
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
                    hosts=data['hosts'],
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
                    hosts=data['hosts'],
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
                    hosts=data['hosts'],
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
                    hosts=data['hosts'],
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
                    hosts=data['hosts'],
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
                    hosts=data['hosts'],
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
                output = json.dumps(result7.results, indent=4)
                context = {
                    'restore': restore,
                    'output': output
                }
                return render(request, 'ansibleweb/restore.html',context)
            elif os == 'routeros':
                my_play = dict(
                    name="Restore Mikrotik",
                    hosts=data['hosts'],
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
                output = json.dumps(result.results, indent=4)
                context = {
                    'restore': restore,
                    'output': output
                }
                return render(request, 'ansibleweb/restore.html', context)
    else:
        restore = ciscorestore()
    
    context = {
        'restore': restore
    }
    return render(request, 'ansibleweb/restore.html', context)


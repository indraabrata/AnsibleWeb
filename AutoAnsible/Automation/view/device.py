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
def addhost(request):
    if request.method == 'POST':
        adddhost = PostInventoryHost(request.POST, request.user)
        if adddhost.is_valid():
            adddhost.save()
            data = request.POST
            akun = request.user
            messages.success(request, f'Berhasil membuat inventory host network')
            logs = log(account=akun, targetss='Host', action='Add Device '+data['host'], status='Success', time=datetime.now(), messages='No Error')
            logs.save()
            return redirect('host-create')
        else:
            return render(request, 'ansibleweb/post_host.html', {'form':adddhost})
    else:
        adddhost = PostInventoryHost()
        return render(request, 'ansibleweb/post_host.html', {'form':adddhost})

def addportdevice(request):
    if request.method == 'GET' and 'btnform1' in request.GET:
        infos = addinfodevice(request.GET)
        if infos.is_valid():
            data = request.GET
            print(request.GET)
            info = devices.objects.all().filter(device_id=data['hosts'])
            cek = len(info)
            if cek > 0 :
                messages.success(request, f'Infomasi Port telah terdaftar dalam database')
            else:
                messages.warning(request, f'Informasi Port belum ditambahkan dalam database')
            context = {
                'infos': infos,
                'info': info
            }
            return render(request, 'ansibleweb/addinfodevice.html', context)
    elif request.method == 'GET' and 'btnform2' in request.GET:
        infos = addinfodevice(request.GET)
        if infos.is_valid():
            data = request.GET
            print(request.GET)
            host = AnsibleNetworkHost.objects.get(id=data['hosts'])
            de_type = host.device_type
            os = host.group.ansible_network_os
            jumlah = devices.objects.all().filter(device_id=host)
            cannot = len(jumlah)
            print(host.host)
            if cannot == 0 and os == 'ce' and de_type == 'router':
                my_play = dict(
                    name="Show ip interface",
                    hosts=host.host,
                    become='yes',
                    become_method='enable',
                    gather_facts='no',
                    vars=[
                        dict(ansible_command_timeout=120)
                    ],
                    tasks=[
                        dict(action=dict(module='ce_command', commands='display ip int brief'))
                        ]
                    )
                result = execute(my_play)
                condition = result.stats
                con = condition['hosts'][0]['status']
                if con == 'ok':
                    output = result.results
                    dataport = output['success'][0]['tasks'][0]['result']['stdout_lines'][0][10:]
                    maks = len(dataport)
                    for x in range(0, maks):
                        portt = dataport[x][:23].replace(" ","")
                        ip = dataport[x][34:52].replace(" ","")
                        phys = dataport[x][55:59].replace(" ","")
                        prtcl = dataport[x][66:71].replace(" ","")
                        coba = devices(port=portt,
                                        ipadd=ip,
                                        physical=phys,
                                        protocol=prtcl,
                                        preconf='empty',
                                        device_id=host)
                        coba.save()
                    info = devices.objects.all().filter(device_id=data['hosts'])
                    context = {
                        'infos': infos,
                        'info': info
                    }
                    return render(request, 'ansibleweb/addinfodevice.html', context)
                else:
                    messages.warning(request, f'Check Connection to Remote Host!')
                    return redirect('port-device')
            elif cannot == 0 and os == 'ce' and de_type == 'switch':
                my_play = dict(
                    name="Show ip interface",
                    hosts=host.host,
                    become='yes',
                    become_method='enable',
                    gather_facts='no',
                    vars=[
                        dict(ansible_command_timeout=120)
                    ],
                    tasks=[
                        dict(action=dict(module='ce_command', commands='display interface brief'))
                        ]
                    )
                result = execute(my_play)
                condition = result.stats
                print(result.results)
                con = condition['hosts'][0]['status']
                if con == 'ok':
                    output = result.results
                    dataport = output['success'][0]['tasks'][0]['result']['stdout_lines'][0][10:]
                    maks = len(dataport)
                    for x in range(0, maks):
                        portt = dataport[x][:25].replace(" ","")
                        phys = dataport[x][28:33].replace(" ","")
                        prtcl = dataport[x][34:39].replace(" ","")
                        coba = devices(port=portt,
                                        physical=phys,
                                        protocol=prtcl,
                                        device_id=host)
                        coba.save()
                    info = devices.objects.all().filter(device_id=data['hosts'])
                    context = {
                        'infos': infos,
                        'info': info
                    }
                    return render(request, 'ansibleweb/addinfodevice.html', context)
                else:
                    messages.warning(request, f'Check Connection to Remote Host!')
                    return redirect('port-device')
            elif cannot == 0 and os == 'routeros':
                my_play = dict(
                    name="display ip",
                    hosts=host.host,
                    become='yes',
                    become_method='enable',
                    gather_facts='no',
                    vars=[
                        dict(ansible_command_timeout=120)
                    ],
                    tasks=[
                        dict(action=dict(module='routeros_command',commands='/ip address print'))
                        ]
                    )
                result = execute(my_play)
                condition= result.stats
                con = condition['hosts'][0]['status']
                if con == 'ok':
                    output = result.results
                    dataport = output['success'][0]['tasks'][0]['result']['stdout_lines'][0][2:]
                    maks = len(dataport)
                    for x in range(0, maks):
                        ip = dataport[x][5:23].replace(" ","")
                        portt = dataport[x][40:46].replace(" ","")
                        coba = devices(port=portt,
                                        ipadd=ip,
                                        physical='',
                                        protocol='',
                                        device_id=host)
                        coba.save()
                    info = devices.objects.all().filter(device_id=data['hosts'])
                    context = {
                        'infos': infos,
                        'info': info
                    }
                    return render(request, 'ansibleweb/addinfodevice.html', context)
                else:
                    messages.warning(request, f'Check Connection to Remote Host!')
                    return redirect('port-device')
            elif cannot == 0 and os =='ios' and de_type == 'switch':
                my_play = dict(
                    name="Show Ip interface brief",
                    hosts=host.host,
                    become='yes',
                    become_method='enable',
                    gather_facts='no',
                    vars=[
                        dict(ansible_command_timeout=120)
                    ],
                    tasks=[
                        dict(action=dict(module='ios_command', commands=['show ip interface brief']))
                        ]
                    )
                result = execute(my_play)
                condition = result.stats
                con = condition['hosts'][0]['status']
                if con == 'ok':
                    output = result.results
                    dataport = output['success'][0]['tasks'][0]['result']['stdout_lines'][0][1:]
                    maks = len(dataport)
                    for x in range(0, maks):
                        portt = dataport[x][:22].replace(" ","")
                        ip = dataport[x][23:38].replace(" ","")
                        phys = dataport[x][54:76]
                        prtcl = dataport[x][76:80].replace(" ","")
                        coba = devices(port=portt,
                                        ipadd=ip,
                                        physical=phys,
                                        protocol=prtcl,
                                        device_id=host)
                        coba.save()
                    info = devices.objects.all().filter(device_id=data['hosts'])
                    context = {
                        'infos': infos,
                        'info': info
                    }
                    return render(request, 'ansibleweb/addinfodevice.html', context)
                else:
                    messages.warning(request, f'Check Connection to Remote Host!')
                    return redirect('port-device')
            elif cannot == 0 and os =='ios' and de_type == 'router':
                my_play = dict(
                    name="Show Ip interface brief",
                    hosts=host.host,
                    become='yes',
                    become_method='enable',
                    gather_facts='no',
                    vars=[
                        dict(ansible_command_timeout=120)
                    ],
                    tasks=[
                        dict(action=dict(module='ios_command', commands=['show ip interface brief']))
                        ]
                    )
                result = execute(my_play)
                condition = result.stats
                con = condition['hosts'][0]['status']
                if con == 'ok':
                    output = result.results
                    dataport = output['success'][0]['tasks'][0]['result']['stdout_lines'][0][1:]
                    maks = len(dataport)
                    for x in range(0, maks):
                        portt = dataport[x][:22].replace(" ","")
                        ip = dataport[x][27:42].replace(" ","")
                        phys = dataport[x][54:76]
                        prtcl = dataport[x][76:80].replace(" ","")
                        coba = devices(port=portt,
                                        ipadd=ip,
                                        physical=phys,
                                        protocol=prtcl,
                                        device_id=host)
                        coba.save()
                    info = devices.objects.all().filter(device_id=data['hosts'])
                    context = {
                        'infos': infos,
                        'info': info
                    }
                    return render(request, 'ansibleweb/addinfodevice.html', context)
                else:
                    messages.warning(request, f'Check Connection to Remote Host!')
                    return redirect('port-device')
            else:
                if os == 'ce' and de_type == 'router':
                    my_play = dict(
                        name="Sh Ip interface",
                        hosts=host.host,
                        become='yes',
                        become_method='enable',
                        gather_facts='no',
                        vars=[
                            dict(ansible_command_timeout=120)
                        ],
                        tasks=[
                            dict(action=dict(module='ce_command', commands='display ip interface brief'))
                            ]
                        )
                    result = execute(my_play)
                    condition = result.stats
                    con = condition['hosts'][0]['status']
                    if con == 'ok':
                        output = result.results
                        dataport = output['success'][0]['tasks'][0]['result']['stdout_lines'][0][10:]
                        maks = len(dataport)
                        for x in range(0, maks):
                            portt = dataport[x][:23].replace(" ","")
                            ip = dataport[x][34:52].replace(" ","")
                            phys = dataport[x][55:59].replace(" ","")
                            prtcl = dataport[x][66:71].replace(" ","")
                            test = devices.objects.filter(device_id=data['hosts']).filter(port=portt).update(ipadd=ip, physical=phys, protocol=prtcl)
                        messages.success(request, f'Port telah tersedia!')
                        info = devices.objects.all().filter(device_id=data['hosts'])
                        context = {
                            'infos': infos,
                            'info': info
                        }
                        return render(request, 'ansibleweb/addinfodevice.html', context)
                    else:
                        messages.warning(request, f'Check Connection to Remote Host!')
                        return redirect('port-device')
                elif os == 'ce' and de_type == 'switch':
                    my_play = dict(
                        name="Sh Ip interface",
                        hosts=host.host,
                        become='yes',
                        become_method='enable',
                        gather_facts='no',
                        vars=[
                            dict(ansible_command_timeout=120)
                        ],
                        tasks=[
                            dict(action=dict(module='ce_command', commands='display interface brief'))
                            ]
                        )
                    result = execute(my_play)
                    condition = result.stats
                    con = condition['hosts'][0]['status']
                    if con == 'ok':
                        output = result.results
                        dataport = output['success'][0]['tasks'][0]['result']['stdout_lines'][0][10:]
                        maks = len(dataport)
                        for x in range(0, maks):
                            portt = dataport[x][:25].replace(" ","")
                            phys = dataport[x][28:33].replace(" ","")
                            prtcl = dataport[x][34:39].replace(" ","")
                            devices.objects.filter(device_id=data['hosts']).filter(port=portt).update(physical=phys, protocol=prtcl)
                        messages.success(request, f'Port telah tersedia!')
                        info = devices.objects.all().filter(device_id=data['hosts'])
                        context = {
                            'infos': infos,
                            'info': info
                        }
                        return render(request, 'ansibleweb/addinfodevice.html', context)
                    else:
                        messages.warning(request, f'Check Connection to Remote Host!')
                        return redirect('port-device')
                elif os == 'routeros':
                    my_play = dict(
                        name="display ip interface",
                        hosts=host.host,
                        become='yes',
                        become_method='enable',
                        gather_facts='no',
                        vars=[
                            dict(ansible_command_timeout=120)
                        ],
                        tasks=[
                            dict(action=dict(module='routeros_command', commands='/ip address print'))
                            ]
                        )
                    result = execute(my_play)
                    condition = result.stats
                    con = condition['hosts'][0]['status']
                    if con == 'ok':
                        output = result.results
                        dataport = output['success'][0]['tasks'][0]['result']['stdout_lines'][0][2:]
                        maks = len(dataport)
                        for x in range(0, maks):
                            ip = dataport[x][5:23].replace(" ","")
                            portt = dataport[x][40:46].replace(" ","")
                            devices.objects.filter(device_id=data['hosts']).filter(port=portt).update(ipadd=ip)
                        messages.info(request, f'Port telah tersedia!')
                        info = devices.objects.all().filter(device_id=data['hosts'])
                        context = {
                            'infos': infos,
                            'info': info
                        }
                        return render(request, 'ansibleweb/addinfodevice.html', context)
                    else:
                        messages.warning(request, f'Check Connection to Remote Host!')
                        return redirect('port-device')
                elif os == 'ios' and de_type == 'router':
                    my_play = dict(
                        name="Show Ip interface brief",
                        hosts=host.host,
                        become='yes',
                        become_method='enable',
                        gather_facts='no',
                        vars=[
                            dict(ansible_command_timeout=120)
                        ],
                        tasks=[
                            dict(action=dict(module='ios_command', commands=['show ip interface brief']))
                            ]
                        )
                    result = execute(my_play)
                    condition = result.stats
                    con = condition['hosts'][0]['status']
                    if con == 'ok':
                        output = result.results
                        dataport = output['success'][0]['tasks'][0]['result']['stdout_lines'][0][1:]
                        maks = len(dataport)
                        for x in range(0, maks):
                            portt = dataport[x][:22].replace(" ","")
                            ip = dataport[x][27:42].replace(" ","")
                            phys = dataport[x][54:76].replace(" ","")
                            prtcl = dataport[x][76:80].replace(" ","")
                            devices.objects.filter(device_id=data['hosts']).filter(port=portt).update(ipadd=ip, physical=phys, protocol=prtcl)
                        messages.info(request, f'Port telah tersedia!')
                        info = devices.objects.all().filter(device_id=data['hosts'])
                        context = {
                            'infos': infos,
                            'info': info
                        }
                        return render(request, 'ansibleweb/addinfodevice.html', context)
                    else:
                        messages.warning(request, f'Check connection to Remote Host!')
                        return redirect('port-device')
                elif os == 'ios' and de_type == 'switch':
                    my_play = dict(
                        name="Show Ip interface brief",
                        hosts=host.host,
                        become='yes',
                        become_method='enable',
                        gather_facts='no',
                        vars=[
                            dict(ansible_command_timeout=120)
                        ],
                        tasks=[
                            dict(action=dict(module='ios_command', commands=['show ip interface brief']))
                            ]
                        )
                    result = execute(my_play)
                    condition = result.stats
                    con = condition['hosts'][0]['status']
                    if con == 'ok':
                        output = result.results
                        dataport = output['success'][0]['tasks'][0]['result']['stdout_lines'][0][1:]
                        maks = len(dataport)
                        for x in range(0, maks):
                            portt = dataport[x][:22].replace(" ","")
                            ip = dataport[x][23:38].replace(" ","")
                            phys = dataport[x][54:76].replace(" ","")
                            prtcl = dataport[x][76:80].replace(" ","")
                            devices.objects.filter(device_id=data['hosts']).filter(port=portt).update(ipadd=ip, physical=phys, protocol=prtcl)
                        messages.info(request, f'Port telah tersedia!')
                        info = devices.objects.all().filter(device_id=data['hosts'])
                        context = {
                            'infos': infos,
                            'info': info
                        }
                        return render(request, 'ansibleweb/addinfodevice.html', context)
                    else:
                        messages.warning(request, f'Check connection to Remote Host!')
                        return redirect('port-device')  
    else:
        infos = addinfodevice()
    
    context = {
        'infos': infos
    }
    return render(request, 'ansibleweb/addinfodevice.html',context)
from __future__ import absolute_import, unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from ..models import mac_os, PostInventoryGroup, PostInventoryHost ,PostPlayBookForm, TaskForm, log, group, addinfodevice , ios_router, preconfdevice, arp, ce_router_form, ce_router, kamusport, ios_switch, ios_switch_form, devices, iosrouter, ce_switch, ce_switch_form, routeros_router, routeros_router_form
from ..forms import ivlanset, hostnamecisco, dhcpset, ospfset, ip_staticset, vlanint, vlan_cisco, ospf_cisco, ciscobackup, ciscorestore, hostnamehuawei, ospf_huawei, intervlan_huawei,hostnamemikrotik, ipaddmikrotik, ospf_mikrotik, mikrotikbackup, huaweirestore, mikrotikrestore, autoconfig , vlanset, host_all
from django.contrib import messages
from itertools import chain
from dj_ansible.models import AnsibleNetworkHost, AnsibleNetworkGroup
from dj_ansible.ansible_kit import execute
import json
from datetime import datetime
import time
import threading
from django.contrib.auth.models import User

@login_required
def arpconfig(request):
    if request.method == 'GET' and 'btnform1' in request.GET:
        form = autoconfig(request.GET)
        if form.is_valid():
            data=request.GET
            print(request.GET)
            host = AnsibleNetworkHost.objects.get(id=data['hosts'])
            os = host.group.ansible_network_os
            jumlah = arp.objects.all().filter(device_id=host)
            cannot = len(jumlah)
            if cannot == 0 and os == 'ios':
                my_play = dict(
                    name="show arp",
                    hosts=host.host,
                    become='yes',
                    become_method='enable',
                    gather_facts='no',
                    vars=[
                        dict(ansible_command_timeout=120)
                    ],
                    tasks=[
                        dict(action=dict(module='ios_command', commands='sh ip arp'))
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
                        ip = dataport[x][10:25].replace(" ","")
                        mac = dataport[x][38:52].replace(" ","")
                        portt = dataport[x][61:].replace(" ","")
                        coba = arp(ipadd=ip,
                                mac=mac,
                                port=portt,
                                device_id=host)
                        coba.save()
                    info = arp.objects.all().filter(device_id=host)
                    context = {
                        'form': form,
                        'info': info
                    }
                    return render(request, 'ansibleweb/autoconfig.html', context)
                else:
                    messages.warning(request, f'Check Connection to Remote Host!')
                    return redirect('arp')
            elif cannot == 0 and os == 'ce':
                my_play = dict(
                    name="show arp",
                    hosts=host.host,
                    become='yes',
                    become_method='enable',
                    gather_facts='no',
                    vars=[
                        dict(ansible_command_timeout=120)
                    ],
                    tasks=[
                        dict(action=dict(module='ce_command', commands='display arp'))
                        ]
                    )
                result = execute(my_play)
                condition = result.stats
                con = condition['hosts'][0]['status']
                if con == 'ok':
                    output = result.results
                    dataport = output['success'][0]['tasks'][0]['result']['stdout_lines'][0][3:]
                    maks = len(dataport)
                    for x in range(0, maks):
                        ip = dataport[x][:15].replace(" ","")
                        mac = dataport[x][16:31].replace(" ","")
                        portt = dataport[x][47:60].replace(" ","")
                        coba = arp(ipadd=ip,
                                    mac=mac,
                                    port=portt,
                                    device_id=host)
                        coba.save()
                    info = arp.objects.all().filter(device_id=host)
                    context = {
                        'form': form,
                        'info': info
                    }
                    return render(request, 'ansibleweb/autoconfig.html', context)
                else:
                    messages.warning(request, f'Check Connection to Remote Host!')
                    return redirect('arp')
            else:
                if cannot > 0 and os == 'ce':
                    print("coba")
                    arp.objects.filter(device_id=data['hosts']).delete()
                    my_play = dict(
                        name="show arp",
                        hosts=host.host,
                        become='yes',
                        become_method='enable',
                        gather_facts='no',
                        vars=[
                            dict(ansible_command_timeout=120)
                        ],
                        tasks=[
                            dict(action=dict(module='ce_command', commands='display arp'))
                            ]
                        )
                    result = execute(my_play)
                    condition = result.stats
                    con = condition['hosts'][0]['status']
                    if con == 'ok':
                        output = result.results
                        dataport = output['success'][0]['tasks'][0]['result']['stdout_lines'][0][3:]
                        maks = len(dataport)
                        for x in range(0, maks):
                            ip = dataport[x][:15].replace(" ","")
                            mac = dataport[x][16:31].replace(" ","")
                            portt = dataport[x][47:60].replace(" ","")
                            coba = arp(ipadd=ip,
                                    mac=mac,
                                    port=portt,
                                    device_id=host)
                            coba.save()
                        info = arp.objects.all().filter(device_id=host)
                        context = {
                            'form': form,
                            'info': info
                        }
                        return render(request, 'ansibleweb/autoconfig.html', context)
                    else:
                        messages.warning(request, f'Check Connection to Remote Host!')
                        return redirect('arp')
                elif cannot > 0 and os == 'ios':
                    arp.objects.filter(device_id=data['hosts']).delete()
                    my_play = dict(
                        name="show arp",
                        hosts=host.host,
                        become='yes',
                        become_method='enable',
                        gather_facts='no',
                        vars=[
                            dict(ansible_command_timeout=120)
                        ],
                        tasks=[
                            dict(action=dict(module='ios_command', commands='sh ip arp'))
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
                            ip = dataport[x][10:25].replace(" ","")
                            mac = dataport[x][38:52].replace(" ","")
                            portt = dataport[x][61:].replace(" ","")
                            coba = arp(ipadd=ip,
                                    mac=mac,
                                    port=portt,
                                    device_id=host)
                            coba.save()
                        info = arp.objects.all().filter(device_id=host)
                        context = {
                            'form': form,
                            'info': info
                        }
                        return render(request, 'ansibleweb/autoconfig.html', context)
                    else:
                        messages.warning(request, f'Check Connection to Remote Host!')
                        return redirect('arp')
    elif request.method == 'GET' and 'btnform2' in request.GET:
        form = autoconfig(request.GET, request.user)
        if form.is_valid():
            data = request.GET
            host= data['hosts']
            hos = AnsibleNetworkHost.objects.get(id=host)
            print(host)
            akun = request.user
            print(request.GET)
            device = data['hosts']
            t1 = threading.Thread(target=autoconf, args=[device, akun])
            t1.start()
            logs = log(account=akun, targetss=hos.host, action="Auto Configuration", status="PENDING", time=datetime.now(), messages="No Error")
            logs.save()
            messages.success(request, f'Starting AutoConfiguration!')
            context = {
                'form': form
            }
            return render(request, 'ansibleweb/autoconfig.html', context)
    else:
        form = autoconfig()
    
    context = {
        'form': form
    }
    return render(request, 'ansibleweb/autoconfig.html', context)



def autoconf(device, akun):
    print("Starting AutoConfiguration")
    time.sleep(10)
    host = AnsibleNetworkHost.objects.get(id=device)
    os = host.group.ansible_network_os
    tipe = host.device_type
    print(host.host)
    jumlah = arp.objects.all().filter(device_id=device)
    cannot = len(jumlah)
    ulang = True
    while ulang:
        if os == 'ios' and tipe == 'switch':
            arp.objects.filter(device_id=device).delete()
            broadcast = devices.objects.filter(device_id=device, port='Vlan1').values_list('ipadd')
            ping_ip = broadcast[0][0]
            dot = ping_ip.rfind('.')
            getchar = ping_ip[dot:]
            for x in range(2, 10):
                change = ping_ip.replace(getchar, "."+str(x))
                print(change)
                my_play = dict(
                    name="Ping broadcast",
                    hosts=host.host,
                    become='yes',
                    become_method='enable',
                    gather_facts='no',
                    vars=[
                        dict(ansible_command_timeout=120)
                    ],
                    tasks=[
                        dict(action=dict(module='ios_command', commands='ping '+change))
                    ]
                )
                result1 = execute(my_play)
            my_play2 = dict(
                name="show arp",
                hosts=host.host,
                become='yes',
                become_method='enable',
                gather_facts='no',
                vars=[
                    dict(ansible_command_timeout=120)
                ],
                tasks=[
                    dict(action=dict(module='ios_command', commands='sh ip arp'))
                    ]
                )
            result = execute(my_play2)
            condition = result.stats
            mac_booked = []
            mac_arp = []
            con = condition['hosts'][0]['status']
            if con == 'ok':
                output = result.results
                dataport = output['success'][0]['tasks'][0]['result']['stdout_lines'][0][1:]
                maks = len(dataport)
                for x in range(0, maks):
                    ip = dataport[x][10:25].replace(" ","")
                    mac = dataport[x][38:52].replace(" ","")
                    portt = dataport[x][61:].replace(" ","")
                    coba = arp(ipadd=ip,
                                mac=mac,
                                port=portt,
                                device_id=host)
                    coba.save()
                bookeds = devices.objects.filter(device_id=device, stats='Booked').values_list('new_device_mac')
                m_max = len(bookeds)
                for z in range(0, m_max):
                    del_1 = bookeds[z][0].replace("-","")
                    del_2 = del_1.replace(".","")
                    del_3 = del_2.replace(":","")
                    del_4 = del_3.lower()#dlm bentukk aabbccddeeff
                    mac_filter = del_4[:4]+"."+del_4[4:8]+"."+del_4[8:]#dlm bentuk aabb.ccdd.eeff
                    mac_booked.append(mac_filter)
                print(mac_booked)
                arps = arp.objects.filter(device_id=device).values_list('mac')
                a_max = len(arps)
                for y in range(0, a_max):
                    del1 = arps[y][0]
                    mac_arp.append(del1)
                print(mac_arp)
                inter = set.intersection(set(mac_arp), set(mac_booked))
                print(inter)
                match = list(inter)
                jumlah = len(match)
                if jumlah > 0:
                    ulang = False
                    for z in range(0, jumlah):
                        findmac = match[z]#dlm bentuk aabb.ccdd.eeff
                        print(findmac)
                        get1 = findmac.replace("-","")
                        get2 = get1.replace(".","")
                        get3 = get2.replace(":","")
                        get4 = get3.upper()#dlm bentuk AABBCCDDEEFF
                        get5 = get4[:6]#dlm bentuk AABBCC
                        get6 = get5[:2]+":"+get5[2:4]+":"+get5[4:6]#dlm bentuk AA:BB:CC
                        findos = mac_os.objects.filter(oui=get6).values_list('vendor')
                        t_os = findos[0][0]#dapat vendor
                        print(t_os)
                        mac_matching = get3.lower()
                        print(device)
                        cekking = devices.objects.filter(device_id=device, stats='Booked', new_device_mac=mac_matching)
                        matching = len(cekking)
                        de_type = devices.objects.filter(device_id=device, stats='Booked', new_device_mac=mac_matching).values_list('new_device_type')
                        dtype = de_type[0][0]
                        precon = devices.objects.filter(device_id=device, stats='Booked', new_device_mac=mac_matching).values_list('preconf')
                        cons = precon[0][0]
                        add_ip = arp.objects.filter(mac=findmac).values_list('ipadd')
                        add_ip_ok = add_ip[0][0]
                        print(add_ip)
                        print(add_ip_ok)
                        Huawei_os = "Huawei" in t_os
                        Cisco_os = "Cisco" in t_os
                        Mikrotik_os= "Mikrotik" in t_os
                        print(Huawei_os)
                        print(Cisco_os)
                        print(Mikrotik_os)
                        if Cisco_os == True and dtype == 'router' and matching > 0:
                            grup = AnsibleNetworkGroup.objects.get(name='Cisco')
                            savehost = AnsibleNetworkHost(host=cons,
                                                ansible_ssh_host=add_ip_ok,
                                                ansible_user='admin',
                                                ansible_ssh_pass='cisco',
                                                ansible_become_pass='cisco',
                                                device_type=de_type,
                                                group=grup)
                            savehost.save()
                            conf = iosrouter.objects.get(name=cons)
                            my_play = dict(
                                    name="hostname",
                                    hosts=cons,
                                    become='yes',
                                    become_method='enable',
                                    gather_facts='no',
                                    vars=[
                                        dict(ansible_command_timeout=120)
                                    ],
                                    tasks=[
                                        dict(action=dict(module='ios_config', commands=conf.hostname)),
                                        dict(action=dict(module='ios_config', commands=conf.port_cmd, parents=conf.port_ip)),
                                        dict(action=dict(module='ios_config', commands=conf.ospf_network+" area "+conf.ospf_area, parents=conf.ospf))
                                        ]
                                    )
                            result = execute(my_play)
                            kondisi = result.stats
                            kond = kondisi['hosts'][0]['status']
                            if kond == 'ok':
                                devices.objects.filter(new_device_mac=findmac).update(stats='configured')
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='SUCCESS')
                            else:
                                fail = result.results
                                err = fail['failed'][0]['tasks'][0]['result']['msg']
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='FAILED', messages=err)
                                print(f'{err}')
                        elif Cisco_os == True and dtype == 'switch' and matching > 0:
                            grup = AnsibleNetworkGroup.objects.get(name='Cisco')
                            savehost = AnsibleNetworkHost(host=cons,
                                                    ansible_ssh_host=add_ip_ok,
                                                    ansible_user='admin',
                                                    ansible_ssh_pass='cisco',
                                                    ansible_become_pass='cisco',
                                                    device_type=de_type,
                                                    group=grup)
                            savehost.save()
                            conf = ios_switch.objects.get(name=cons)
                            my_play = dict(
                                    name="hostname",
                                    hosts=cons,
                                    become='yes',
                                    become_method='enable',
                                    gather_facts='no',
                                    vars=[
                                        dict(ansible_command_timeout=120)
                                    ],
                                    tasks=[
                                        dict(action=dict(module='ios_config', commands=conf.hostname)),
                                        dict(action=dict(module='ios_vlan', vlan_id=conf.vlan_id, name=conf.vlan_name))
                                    ]
                                )
                            result = execute(my_play)
                            kondisi = result.stats
                            kond = kondisi['hosts'][0]['status']
                            if kond == 'ok':
                                devices.objects.filter(new_device_mac=findmac).update(stats='configured')
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='SUCCESS')
                            else:
                                fail = result.results
                                err = fail['failed'][0]['tasks'][0]['result']['msg']
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='FAILED', messages=err)
                                print(f'{err}')
                        elif Huawei_os == True and dtype == 'router' and matching > 0:
                            grup = AnsibleNetworkGroup.objects.get(name='Huawei')
                            savehost = AnsibleNetworkHost(host=cons,
                                                ansible_ssh_host=add_ip_ok,
                                                ansible_user='admin',
                                                ansible_ssh_pass='54541691',
                                                ansible_become_pass='54541691',
                                                device_type=de_type,
                                                group=grup)
                            savehost.save()
                            conf = ce_router.objects.get(name=cons)
                            my_play = dict(
                                    name="hostname",
                                    hosts=cons,
                                    become='yes',
                                    become_method='enable',
                                    gather_facts='no',
                                    vars=[
                                        dict(ansible_command_timeout=120)
                                    ],
                                    tasks=[
                                        dict(action=dict(module='ce_config', commands=conf.hostname)),
                                        dict(action=dict(module='ce_config', lines=[conf.ospf, conf.ospf_area, conf.ospf_network]))
                                        ]
                                    )
                            result = execute(my_play)
                            kondisi = result.stats
                            kond = kondisi['hosts'][0]['status']
                            if kond == 'ok':
                                devices.objects.filter(new_device_mac=findmac).update(stats='configured')
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='SUCCESS')
                            else:
                                fail = result.results
                                err = fail['failed'][0]['tasks'][0]['result']['msg']
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='FAILED', messages=err)
                                print(f'{err}')
                        elif Huawei_os == True and dtype == 'switch' and matching > 0:
                            grup = AnsibleNetworkGroup.objects.get(name='Huawei')
                            savehost = AnsibleNetworkHost(host=cons,
                                                ansible_ssh_host=add_ip_ok,
                                                ansible_user='admin',
                                                ansible_ssh_pass='huawei12345',
                                                ansible_become_pass='huawei12345',
                                                device_type=de_type,
                                                group=grup)
                            savehost.save()
                            print(host)
                            conf = ios_switch.objects.get(name=cons)
                            my_play = dict(
                                    name="hostname",
                                    hosts=cons,
                                    become='yes',
                                    become_method='enable',
                                    gather_facts='no',
                                    vars=[
                                        dict(ansible_command_timeout=120)
                                    ],
                                    tasks=[
                                        dict(action=dict(module='ce_config', commands='sysname '+conf.hostname)),
                                        dict(action=dict(module='ce_config', lines=['vlan '+conf.vlan_id, 'description '+conf.vlan_name]))
                                        ]
                                    )
                            result = execute(my_play)
                            print(conf.name)
                            print(result.results)
                            kondisi = result.stats
                            kond = kondisi['hosts'][0]['status']
                            if kond == 'ok':
                                devices.objects.filter(new_device_mac=findmac).update(stats='configured')
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='SUCCESS')
                            else:
                                fail = result.results
                                err = fail['failed'][0]['tasks'][0]['result']['msg']
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='FAILED', messages=err)
                                print(f'{err}')
                        elif Mikrotik_os == True and dtype == 'router' and matching > 0:
                            grup = AnsibleNetworkGroup.objects.get(name='Mikrotik')
                            savehost = AnsibleNetworkHost(host=cons,
                                                    ansible_ssh_host=add_ip_ok,
                                                    ansible_user='mikrotik',
                                                    ansible_ssh_pass='54541691',
                                                    ansible_become_pass='54541691',
                                                    device_type=de_type,
                                                    group=grup)
                            savehost.save()
                            conf = routeros_router.objects.get(name=cons)
                            my_play = dict(
                                    name="hostname",
                                    hosts=cons,
                                    become='yes',
                                    become_method='enable',
                                    gather_facts='no',
                                    vars=[
                                        dict(ansible_command_timeout=120)
                                    ],
                                    tasks=[
                                        dict(action=dict(module='routeros_command', commands=conf.hostname)),
                                        dict(action=dict(module='routeros_command', commands=conf.ospf)),
                                        dict(action=dict(module='routeros_command', commands=conf.inter_vlan)),
                                        dict(action=dict(module='routeros_coomand', commands=conf.ip_add_vlan))
                                        ]
                                )
                            result = execute(my_play)
                            kondisi = result.stats
                            kond = kondisi['hosts'][0]['status']
                            if kond == 'ok':
                                devices.objects.filter(new_device_mac=findmac).update(stats='configured')
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='SUCCESS')
                            else:
                                fail = result.results
                                err = fail['failed'][0]['tasks'][0]['result']['msg']
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='FAILED', messages=err)
                                print(f'{err}')
                        else:
                            logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='FAILED', messages='Port Tidak Sesuai')
        if os == 'ios' and tipe == 'router':
            arp.objects.filter(device_id=device).delete()
            listip = devices.objects.filter(device_id=device, stats='Booked').values_list('ipadd')
            total = len(listip)
            for x in range(0, total):
                ping_ip = listip[x][0]+str(56)
                dot = ping_ip.rfind('.')
                getchar = ping_ip[dot:]
                print(getchar)
                change = ping_ip.replace(getchar, ".255")
                print(change)
                my_play = dict(
                    name="Ping broadcast",
                    hosts=host.host,
                    become='yes',
                    become_method='enable',
                    gather_facts='no',
                    vars=[
                        dict(ansible_command_timeout=120)
                    ],
                    tasks=[
                        dict(action=dict(module='ios_command', commands='ping '+change))
                    ]
                )
                result1 = execute(my_play)
            my_play2 = dict(
                name="show arp",
                hosts=host.host,
                become='yes',
                become_method='enable',
                gather_facts='no',
                vars=[
                    dict(ansible_command_timeout=120)
                ],
                tasks=[
                    dict(action=dict(module='ios_command', commands='sh ip arp'))
                    ]
                )
            result = execute(my_play2)
            condition = result.stats
            mac_booked = []
            mac_arp = []
            con = condition['hosts'][0]['status']
            if con == 'ok':
                output = result.results
                dataport = output['success'][0]['tasks'][0]['result']['stdout_lines'][0][1:]
                maks = len(dataport)
                for x in range(0, maks):
                    ip = dataport[x][10:25].replace(" ","")
                    mac = dataport[x][38:52].replace(" ","")
                    portt = dataport[x][61:].replace(" ","")
                    coba = arp(ipadd=ip,
                                mac=mac,
                                port=portt,
                                device_id=host)
                    coba.save()
                bookeds = devices.objects.filter(device_id=device, stats='Booked').values_list('new_device_mac')
                m_max = len(bookeds)
                for z in range(0, m_max):
                    del_1 = bookeds[z][0].replace("-","")
                    del_2 = del_1.replace(".","")
                    del_3 = del_2.replace(":","")
                    del_4 = del_3.lower()#dlm bentukk aabbccddeeff
                    mac_filter = del_4[:4]+"."+del_4[4:8]+"."+del_4[8:]#dlm bentuk aabb.ccdd.eeff
                    mac_booked.append(mac_filter)
                arps = arp.objects.filter(device_id=device).values_list('mac')
                a_max = len(arps)
                for y in range(0, a_max):
                    del1 = arps[y][0]
                    mac_arp.append(del1)
                inter = set.intersection(set(mac_arp), set(mac_booked))
                match = list(inter)
                jumlah = len(match)
                if jumlah > 0:
                    ulang = False
                    for z in range(0, jumlah):
                        findmac = match[z]#dlm bentuk aabb.ccdd.eeff
                        get1 = findmac.replace("-","")
                        get2 = get1.replace(".","")
                        get3 = get2.replace(":","")
                        get4 = get3.upper()#dlm bentuk AABBCCDDEEFF
                        get5 = get4[:6]#dlm bentuk AABBCC
                        get6 = get5[:2]+":"+get5[2:4]+":"+get5[4:6]#dlm bentuk AA:BB:CC
                        findos = mac_os.objects.filter(oui=get6).values_list('vendor')
                        t_os = findos[0][0]#dapat vendor
                        ios_mac = get4.lower()#dlm bentuk aabbccddeeff
                        ios_macs = ios_mac[:4]+"."+ios_mac[4:8]+"."+ios_mac[8:]#bentuk aabb.ccdd.eeff untuk ios
                        getportarp = arp.objects.filter(device_id=device, mac=findmac).values_list('port')
                        portarpp = getportarp[0][0]#'GigabitEthernet0/0/1'
                        cekking = devices.objects.filter(device_id=device, stats='Booked', port=portarpp).values_list('new_device_mac')
                        convert_mac = cekking[0][0]
                        c_1 = convert_mac.replace("-","")
                        c_2 = c_1.replace(".","")
                        c_3 = c_2.replace(":","")
                        c_4 = c_3.lower()
                        c_5 = c_4[:4]+"."+c_4[4:8]+"."+c_4[8:]#dlm bentuk ios aabb.ccdd.eeff
                        print(c_5)
                        matching = c_5 in findmac
                        de_type = devices.objects.filter(device_id=device, stats='Booked', port=portarpp).values_list('new_device_type')
                        dtype = de_type[0][0]
                        add_ip = arp.objects.filter(mac=findmac).values_list('ipadd')
                        add_ip_ok = add_ip[0][0]
                        print(add_ip_ok)
                        precon = devices.objects.filter(device_id=device, stats='Booked', port=portarpp).values_list('preconf')
                        cons = precon[0][0]
                        Huawei_os = "Huawei" in t_os
                        Cisco_os = "Cisco" in t_os
                        Mikrotik_os= "Mikrotik" in t_os
                        print(Huawei_os)
                        print(Cisco_os)
                        print(Mikrotik_os)
                        if Cisco_os == True and dtype == 'router' and matching == True:
                            grup = AnsibleNetworkGroup.objects.get(name='Cisco')
                            savehost = AnsibleNetworkHost(host=cons,
                                                ansible_ssh_host=add_ip_ok,
                                                ansible_user='admin',
                                                ansible_ssh_pass='cisco',
                                                ansible_become_pass='cisco',
                                                device_type=de_type,
                                                group=grup)
                            savehost.save()
                            print(savehost)
                            conf = iosrouter.objects.get(name=cons)
                            my_play = dict(
                                    name="hostname",
                                    hosts=cons,
                                    become='yes',
                                    become_method='enable',
                                    gather_facts='no',
                                    vars=[
                                        dict(ansible_command_timeout=120)
                                    ],
                                    tasks=[
                                        dict(action=dict(module='ios_config', commands='hostname '+conf.hostname)),
                                        dict(action=dict(module='ios_config', commands='ip add '+conf.port_cmd, parents='int '+conf.port_ip)),
                                        dict(action=dict(module='ios_config', commands='network '+conf.ospf_network+" area "+conf.ospf_area, parents='router ospf'+conf.ospf))
                                        ]
                                    )
                            result = execute(my_play)
                            print(result.results)
                            kondisi = result.stats
                            kond = kondisi['hosts'][0]['status']
                            print(kond)
                            if kond == 'ok':
                                devices.objects.filter(new_device_mac=findmac).update(stats='configured')
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='SUCCESS')
                            else:
                                fail = result.results
                                err = fail['failed'][0]['tasks'][0]['result']['msg']
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='FAILED', messages=err)
                                print(f'{err}')
                        elif Cisco_os == True and dtype == 'switch' and matching == True:
                            grup = AnsibleNetworkGroup.objects.get(name='Cisco')
                            savehost = AnsibleNetworkHost(host=cons,
                                                    ansible_ssh_host=add_ip,
                                                    ansible_user='admin',
                                                    ansible_ssh_pass='cisco',
                                                    ansible_become_pass='cisco',
                                                    device_type=de_type,
                                                    group=grup)
                            savehost.save()
                            conf = ios_switch.objects.get(name=cons)
                            my_play = dict(
                                    name="hostname",
                                    hosts=cons,
                                    become='yes',
                                    become_method='enable',
                                    gather_facts='no',
                                    vars=[
                                        dict(ansible_command_timeout=120)
                                    ],
                                    tasks=[
                                        dict(action=dict(module='ios_config', commands=conf.hostname)),
                                        dict(action=dict(module='ios_vlan', vlan_id=conf.vlan_id, name=conf.vlan_name))
                                    ]
                                )
                            result = execute(my_play)
                            kondisi = result.stats
                            kond = kondisi['hosts'][0]['status']
                            if kond == 'ok':
                                devices.objects.filter(new_device_mac=findmac).update(stats='configured')
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='SUCCESS')
                            else:
                                fail = result.results
                                err = fail['failed'][0]['tasks'][0]['result']['msg'][0]
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='FAILED', messages=err)
                                print(f'{err}')
                        elif Huawei_os == True and dtype == 'router' and matching == True:
                            grup = AnsibleNetworkGroup.objects.get(name='Huawei')
                            savehost = AnsibleNetworkHost(host=cons,
                                                ansible_ssh_host=add_ip,
                                                ansible_user='admin',
                                                ansible_ssh_pass='huawei12345',
                                                ansible_become_pass='huawei12345',
                                                device_type=de_type,
                                                group=grup)
                            savehost.save()
                            conf = ce_router.objects.get(name=cons)
                            my_play = dict(
                                    name="hostname",
                                    hosts=cons,
                                    become='yes',
                                    become_method='enable',
                                    gather_facts='no',
                                    vars=[
                                        dict(ansible_command_timeout=120)
                                    ],
                                    tasks=[
                                        dict(action=dict(module='ce_config', commands=conf.hostname)),
                                        dict(action=dict(module='ce_config', lines=[conf.ospf, conf.ospf_area, conf.ospf_network]))
                                        ]
                                    )
                            result = execute(my_play)
                            kondisi = result.stats
                            kond = kondisi['hosts'][0]['status']
                            if kond == 'ok':
                                devices.objects.filter(new_device_mac=findmac).update(stats='configured')
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='SUCCESS')
                            else:
                                fail = result.results
                                err = fail['failed'][0]['tasks'][0]['result']['msg'][0]
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='FAILED', messages=err)
                                print(f'{err}')
                        elif Huawei_os == True and dtype == 'switch' and matching == True:
                            grup = AnsibleNetworkGroup.objects.get(name='Huawei')
                            savehost = AnsibleNetworkHost(host=cons,
                                                ansible_ssh_host=add_ip,
                                                ansible_user='admin',
                                                ansible_ssh_pass='huawei12345',
                                                ansible_become_pass='54541691',
                                                device_type=de_type,
                                                group=grup)
                            savehost.save()
                            print(host)
                            conf = ce_switch.objects.get(name=cons)
                            my_play = dict(
                                    name="hostname",
                                    hosts=cons,
                                    become='yes',
                                    become_method='enable',
                                    gather_facts='no',
                                    vars=[
                                        dict(ansible_command_timeout=120)
                                    ],
                                    tasks=[
                                        dict(action=dict(module='ce_config', commands=conf.hostname)),
                                        dict(action=dict(module='ce_config', commands=conf.vlan)),
                                        dict(action=dict(module='ce_config', lines=[conf.port_ip, conf.port_cmd1, conf.port_vlan]))
                                        ]
                                    )
                            result = execute(my_play)
                            print(conf.name)
                            print(result.results)
                            kondisi = result.stats
                            kond = kondisi['hosts'][0]['status']
                            if kond == 'ok':
                                devices.objects.filter(new_device_mac=findmac).update(stats='configured')
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='SUCCESS')
                            else:
                                fail = result.results
                                err = fail['failed'][0]['tasks'][0]['result']['msg'][0]
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='FAILED', messages=err)
                                print(f'{err}')
                        elif Mikrotik_os == True and dtype == 'router' and matching == True:
                            grup = AnsibleNetworkGroup.objects.get(name='Mikrotik')
                            savehost = AnsibleNetworkHost(host=cons,
                                                    ansible_ssh_host=add_ip,
                                                    ansible_user='mikrotik',
                                                    ansible_ssh_pass='54541691',
                                                    ansible_become_pass='54541691',
                                                    device_type=de_type,
                                                    group=grup)
                            savehost.save()
                            conf = routeros_router.objects.get(name=cons)
                            my_play = dict(
                                    name="hostname",
                                    hosts=cons,
                                    become='yes',
                                    become_method='enable',
                                    gather_facts='no',
                                    vars=[
                                        dict(ansible_command_timeout=120)
                                    ],
                                    tasks=[
                                        dict(action=dict(module='routeros_command', commands=conf.hostname)),
                                        dict(action=dict(module='routeros_command', commands=conf.ospf)),
                                        dict(action=dict(module='routeros_command', commands=conf.inter_vlan)),
                                        dict(action=dict(module='routeros_coomand', commands=conf.ip_add_vlan))
                                        ]
                                )
                            result = execute(my_play)
                            kondisi = result.stats
                            kond = kondisi['hosts'][0]['status']
                            if kond == 'ok':
                                devices.objects.filter(new_device_mac=findmac).update(stats='configured')
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='SUCCESS')
                            else:
                                fail = result.results
                                err = fail['failed'][0]['tasks'][0]['result']['msg'][0]
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='FAILED', messages=err)
                                print(f'{err}')
                        else:
                            logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='FAILED', messages='Port Tidak Sesuai')
        elif os == 'ce' and de_type == 'switch':
            arp.objects.filter(device_id=device).delete()
            broadcast = devices.objects.filter(device_id=device, port='Vlanif1').values_list('ipadd')
            ping_ip = broadcast[0][0]
            dot = ping_ip.rfind('.')
            getchar = ping_ip[dot:]
            for x in range(2, 10):
                change = ping_ip.replace(getchar, "."+str(x))
                print(change)
                my_play = dict(
                    name="Ping broadcast",
                    hosts=host.host,
                    become='yes',
                    become_method='enable',
                    gather_facts='no',
                    vars=[
                        dict(ansible_command_timeout=120)
                    ],
                    tasks=[
                        dict(action=dict(module='ce_config', commands='ping '+change))
                    ]
                )
                result1 = execute(my_play)
            my_play2 = dict(
                name="show arp",
                hosts=host.host,
                become='yes',
                become_method='enable',
                gather_facts='no',
                vars=[
                    dict(ansible_command_timeout=120)
                ],
                tasks=[
                    dict(action=dict(module='ce_command', commands='display arp'))
                    ]
                )
            result = execute(my_play2)
            print(my_play)
            condition = result.stats
            print(condition)
            mac_booked = []
            mac_arp = []
            con = condition['hosts'][0]['status']
            print(con)
            if con == 'ok':
                output = result.results
                dataport = output['success'][0]['tasks'][0]['result']['stdout_lines'][0][3:]
                maks = len(dataport)
                for x in range(0, maks):
                    ip = dataport[x][:15].replace(" ","")
                    mac = dataport[x][16:31].replace(" ","")
                    portt = dataport[x][47:60].replace(" ","")
                    coba = arp(ipadd=ip,
                                mac=mac,
                                port=portt,
                                device_id=host)
                    coba.save()
                bookeds = devices.objects.filter(device_id=device, stats='Booked').values_list('new_device_mac')
                m_max = len(bookeds)
                for z in range(0, m_max):
                    del_1 = bookeds[z][0].replace("-","")
                    del_2 = del_1.replace(".","")
                    del_3 = del_2.replace(":","")
                    del_4 = del_3.lower()
                    mac_filter = del_4[:4]+"-"+del_4[4:8]+"-"+del_4[8:]
                    mac_booked.append(mac_filter)
                arps = arp.objects.filter(device_id=device).values_list('mac')
                a_max = len(arps)
                for y in range(0, a_max):
                    del1 = arps[y][0]
                    mac_arp.append(del1)
                inter = set.intersection(set(mac_arp), set(mac_booked))
                match = list(inter)
                print(bookeds)
                print(arps)
                print(match)
                jumlah = len(match)
                if jumlah > 0:
                    ulang = False
                    for z in range(0, jumlah):
                        findmac = match[z]
                        get1 = findmac.replace("-","")
                        get2 = get1.replace(".","")
                        get3 = get2.replace(":","")
                        get4 = get3.upper()
                        get5 = get4[:6]
                        get6 = get5[:2]+":"+get5[2:4]+":"+get5[4:6]
                        findos = mac_os.objects.filter(oui=get6).values_list('vendor')
                        t_os = findos[0][0]
                        print(t_os)
                        print(findmac)
                        mac_matching = get3.lower()
                        print(device)
                        cekking = devices.objects.filter(device_id=device, stats='Booked', new_device_mac=mac_matching)
                        matching = len(cekking)
                        de_type = devices.objects.filter(device_id=device, stats='Booked', new_device_mac=mac_matching).values_list('new_device_type')
                        dtype = de_type[0][0]
                        add_ip = arp.objects.filter(mac=findmac).values_list('ipadd')
                        add_ip_ok = add_ip[0][0] 
                        print(add_ip_ok)
                        precon = devices.objects.filter(device_id=device, stats='Booked', new_device_mac=mac_matching).values_list('preconf')
                        cons = precon[0][0]
                        print(cons)
                        print(t_os)
                        print(matching)
                        print(dtype)
                        print(host.group)
                        Huawei_os = "Huawei" in t_os
                        Cisco_os = "Cisco" in t_os
                        Mikrotik_os= "Mikrotik" in t_os
                        print(Huawei_os)
                        print(Cisco_os)
                        print(Mikrotik_os)
                        if Cisco_os == True and dtype == 'router' and matching > 0:
                            grup = AnsibleNetworkGroup.objects.get(name='Cisco')
                            print('dicisco')
                            savehost = AnsibleNetworkHost(host=cons,
                                                ansible_ssh_host=add_ip_ok,
                                                ansible_user='admin',
                                                ansible_ssh_pass='cisco',
                                                ansible_become_pass='cisco',
                                                device_type=de_type,
                                                group=grup)
                            savehost.save()
                            conf = iosrouter.objects.get(name=cons)
                            my_play = dict(
                                    name="hostname",
                                    hosts=cons,
                                    become='yes',
                                    become_method='enable',
                                    gather_facts='no',
                                    vars=[
                                        dict(ansible_command_timeout=120)
                                    ],
                                    tasks=[
                                        dict(action=dict(module='ios_config', commands=conf.hostname)),
                                        dict(action=dict(module='ios_config', commands=conf.port_cmd, parents=conf.port_ip)),
                                        dict(action=dict(module='ios_config', commands=conf.ospf_network+" area "+conf.ospf_area, parents=conf.ospf))
                                        ]
                                    )
                            result = execute(my_play)
                            kondisi = result.stats
                            kond = kondisi['hosts'][0]['status']
                            if kond == 'ok':
                                devices.objects.filter(new_device_mac=mac_matching).update(stats='configured')
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='SUCCESS')
                            else:
                                fail = result.results
                                err = fail['failed'][0]['tasks'][0]['result']['msg'][0]
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='FAILED', messages=err)
                                print(f'{err}')
                        elif Huawei_os == True and dtype == 'router' and matching == True:
                            grup = AnsibleNetworkGroup.objects.get(name='Huawei')
                            print("huawei router")
                            savehost = AnsibleNetworkHost(host=cons,
                                                ansible_ssh_host=add_ip_ok,
                                                ansible_user='admin',
                                                ansible_ssh_pass='huawei12345',
                                                ansible_become_pass='huawei12345',
                                                device_type=de_type,
                                                group=grup)
                            savehost.save()
                            print(savehost)
                            conf = ce_router.objects.get(name=cons)
                            my_play = dict(
                                    name="hostname",
                                    hosts=cons,
                                    become='yes',
                                    become_method='enable',
                                    gather_facts='no',
                                    vars=[
                                        dict(ansible_command_timeout=120)
                                    ],
                                    tasks=[
                                        dict(action=dict(module='ce_config', commands=conf.hostname)),
                                        dict(action=dict(module='ce_config', lines=[conf.ospf, conf.ospf_area, conf.ospf_network]))
                                        ]
                                    )
                            result = execute(my_play)
                            print(conf.name)
                            print(result.results)
                            kondisi = result.stats
                            kond = kondisi['hosts'][0]['status']
                            if kond == 'ok':
                                devices.objects.filter(new_device_mac=mac_matching).update(stats='configured')
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='SUCCESS')
                            else:
                                fail = result.results
                                err = fail['failed'][0]['tasks'][0]['result']['msg'][0]
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='FAILED', messages=err)
                                print(f'{err}')
                        elif Huawei_os == True and dtype == 'switch' and matching == True:
                            grup = AnsibleNetworkGroup.objects.get(name='Huawei')
                            print('huawei switch')
                            savehost = AnsibleNetworkHost(host=cons,
                                                ansible_ssh_host=add_ip_ok,
                                                ansible_user='admin',
                                                ansible_ssh_pass='huawei12345',
                                                ansible_become_pass='huawei12345',
                                                device_type=de_type,
                                                group=grup)
                            savehost.save()
                            print(host)
                            conf = ce_switch.objects.get(name=cons)
                            my_play = dict(
                                    name="hostname",
                                    hosts=cons,
                                    become='yes',
                                    become_method='enable',
                                    gather_facts='no',
                                    vars=[
                                        dict(ansible_command_timeout=120)
                                    ],
                                    tasks=[
                                        dict(action=dict(module='ce_config', commands=conf.hostname)),
                                        dict(action=dict(module='ce_config', commands=conf.vlan)),
                                        dict(action=dict(module='ce_config', lines=[conf.port_ip, conf.port_cmd1, conf.port_vlan]))
                                        ]
                                    )
                            result = execute(my_play)
                            print(conf.name)
                            print(result.results)
                            kondisi = result.stats
                            kond = kondisi['hosts'][0]['status']
                            if kond == 'ok':
                                devices.objects.filter(new_device_mac=mac_matching).update(stats='configured')
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='SUCCESS')
                            else:
                                fail = result.results
                                err = fail['failed'][0]['tasks'][0]['result']['msg'][0]
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='FAILED', messages=err)
                                print(f'{err}')
                        elif Cisco_os == True and dtype == 'switch' and matching == True:
                            grup = AnsibleNetworkGroup.objects.get(name='Cisco')
                            print('cisco switch')
                            savehost = AnsibleNetworkHost(host=cons,
                                                    ansible_ssh_host=add_ip_ok,
                                                    ansible_user='admin',
                                                    ansible_ssh_pass='cisco',
                                                    ansible_become_pass='cisco',
                                                    device_type=de_type,
                                                    group=grup)
                            savehost.save()
                            conf = ios_switch.objects.get(name=cons)
                            my_play = dict(
                                    name="hostname",
                                    hosts=cons,
                                    become='yes',
                                    become_method='enable',
                                    gather_facts='no',
                                    vars=[
                                        dict(ansible_command_timeout=120)
                                    ],
                                    tasks=[
                                        dict(action=dict(module='ios_config', commands=conf.hostname)),
                                        dict(action=dict(module='ios_vlan', vlan_id=conf.vlan_id, name=conf.vlan_name))
                                    ]
                                )
                            result = execute(my_play)
                            kondisi = result.stats
                            kond = kondisi['hosts'][0]['status']
                            if kond == 'ok':
                                devices.objects.filter(new_device_mac=mac_matching).update(stats='configured')
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='SUCCESS')
                            else:
                                fail = result.results
                                err = fail['failed'][0]['tasks'][0]['result']['msg'][0]
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='FAILED', messages=err)
                                print(f'{err}')
                        elif Mikrotik_os == True and dtype == 'router' and matching == True:
                            grup = AnsibleNetworkGroup.objects.get(name='Mikrotik')
                            print('mikrotik router')
                            savehost = AnsibleNetworkHost(host=cons,
                                                    ansible_ssh_host=add_ip_ok,
                                                    ansible_user='mikrotik',
                                                    ansible_ssh_pass='54541691',
                                                    ansible_become_pass='54541691',
                                                    device_type=de_type,
                                                    group=grup)
                            savehost.save()
                            conf = routeros_router.objects.get(name=cons)
                            my_play = dict(
                                    name="hostname",
                                    hosts=cons,
                                    become='yes',
                                    become_method='enable',
                                    gather_facts='no',
                                    vars=[
                                        dict(ansible_command_timeout=120)
                                    ],
                                    tasks=[
                                        dict(action=dict(module='routeros_command', commands=conf.hostname)),
                                        dict(action=dict(module='routeros_command', commands=conf.ospf)),
                                        dict(action=dict(module='routeros_command', commands=conf.inter_vlan)),
                                        dict(action=dict(module='routeros_coomand', commands=conf.ip_add_vlan))
                                        ]
                                )
                            result = execute(my_play)
                            kondisi = result.stats
                            kond = kondisi['hosts'][0]['status']
                            if kond == 'ok':
                                devices.objects.filter(new_device_mac=mac_matching).update(stats='configured')
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='SUCCESS')
                            else:
                                fail = result.results
                                err = fail['failed'][0]['tasks'][0]['result']['msg'][0]
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='FAILED', messages=err)
                                print(f'{err}')
        elif os == 'routeros':
            arp.objects.filter(device_id=device).delete()
            my_play = dict(name="show arp",
                            host=host.host,
                            become='yes',
                            become_method='enable',
                            gather_facts='no',
                            vars=[
                                dict(ansible_command_timeout=120)
                            ],
                            tasks=[
                                dict(action=dict(module='routeros_command', commands='/ip arp print'))
                                ]
                            )
            result = execute(my_play)
            print(my_play)
            condition = result.stats
            print(condition)
            mac_booked = []
            mac_arp = []
            con = condition['hosts'][0]['status']
            print(con)
            if con == 'ok':
                output = result.results
                dataport = output['success'][0]['tasks'][0]['result']['stdout_lines'][0][3:]
                maks = len(dataport)
                for x in range(0, maks):
                    ip = dataport[x][6:22].replace(" ","")
                    mac = dataport[x][22:40].replace(" ","")
                    portt = dataport[x][40:].replace(" ","")
                    coba = arp(ipadd=ip,
                                mac=mac,
                                port=portt,
                                device_id=host)
                    coba.save()
                bookeds = devices.objects.filter(device_id=device, stats='Booked').values_list('new_device_mac')
                m_max = len(bookeds)
                for z in range(0, m_max):
                    del_1 = bookeds[z][0].replace("-","")
                    del_2 = del_1.replace(".","")
                    del_3 = del_2.replace(":","")
                    del_4 = del_3.upper()
                    mac_filter = del_4[:2]+":"+del_4[2:4]+":"+del_4[4:6]+":"+del_4[6:8]+":"+del_4[8:10]+":"+del_4[10:]
                    mac_booked.append(mac_filter)
                arps = arp.objects.filter(device_id=device).values_list('mac')
                a_max = len(arps)
                for y in range(0, a_max):
                    del1 = arps[y][0]
                    mac_arp.append(del1)
                inter = set.intersection(set(mac_arp), set(mac_booked))
                match = list(inter)
                print(bookeds)
                print(arps)
                print(match)
                jumlah = len(match)
                if jumlah > 0:
                    ulang = False
                    for z in range(0, jumlah):
                        findmac = match[z]
                        print(findmac)
                        get1 = findmac.replace("-","")
                        get2 = get1.replace(".","")
                        get3 = get2.replace(":","")
                        get4 = get3.upper()
                        get5 = get4[:6]
                        get6 = get5[:2]+":"+get5[2:4]+":"+get5[4:6]
                        findos = mac_os.objects.filter(oui=get6).values_list('vendor')
                        t_os = findos[0][0]
                        getportarp = arp.objects.filter(device_id=device, mac=findmac).values_list('port')
                        portarpp = getportarp[0][0]
                        cekking = devices.objects.filter(device_id=device, stats='Booked', port=portarpp).values_list('new_device_type')
                        convert_mac = cekking[0][0]
                        c_1 = convert_mac.replace("-","")
                        c_2 = c_1.replace(".","")
                        c_3 = c_2.replace(":","")
                        c_4 = c_3.upper()
                        c_5 = c_4[:2]+":"+c_4[2:4]+":"+c_4[4:6]+":"+c_4[6:8]+":"+c_4[8:10]+":"+c_4[10:]
                        print(c_5)
                        matching = c_5 in findmac
                        de_type = devices.objects.filter(device_id=device, stats='Booked', port=portarpp).values_list('new_device_type')
                        dtype = de_type[0][0]
                        add_ip = arp.objects.filter(mac=findmac).values_list('ipadd')
                        add_ip_ok = add_ip[0][0]
                        precon = devices.objects.filter(device_id=device, stats='Booked', port=portarpp).values_list('preconf')
                        cons = precon[0][0]
                        print(cons)
                        print(t_os)
                        Huawei_os = "Huawei" in t_os
                        Cisco_os = "Cisco" in t_os
                        Mikrotik_os= "Mikrotik" in t_os
                        print(Huawei_os)
                        print(Cisco_os)
                        print(Mikrotik_os)
                        if Cisco_os == True and dtype == 'router' and matching == True:
                            grup = AnsibleNetworkGroup.objects.get(name='Cisco')
                            savehost = AnsibleNetworkHost(host=cons,
                                                ansible_ssh_host=add_ip_ok,
                                                ansible_user='indra',
                                                ansible_ssh_pass='cisco',
                                                ansible_become_pass='cisco',
                                                device_type=de_type,
                                                group=grup)
                            savehost.save()
                            conf = iosrouter.objects.get(name=cons)
                            my_play = dict(
                                    name="hostname",
                                    hosts=cons,
                                    become='yes',
                                    become_method='enable',
                                    gather_facts='no',
                                    vars=[
                                        dict(ansible_command_timeout=120)
                                    ],
                                    tasks=[
                                        dict(action=dict(module='ios_config', commands=conf.hostname)),
                                        dict(action=dict(module='ios_config', commands=conf.port_cmd, parents=conf.port_ip)),
                                        dict(action=dict(module='ios_config', commands=conf.ospf_network+" area "+conf.ospf_area, parents=conf.ospf))
                                        ]
                                    )
                            result = execute(my_play)
                            kondisi = result.stats
                            kond = kondisi['hosts'][0]['status']
                            if kond == 'ok':
                                devices.objects.filter(new_device_mac=mac_matching).update(stats='configured')
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='SUCCESS')
                            else:
                                fail = result.results
                                err = fail['failed'][0]['tasks'][0]['result']['msg'][0]
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='FAILED', messages=err)
                                print(f'{err}')
                        elif Huawei_os == True and dtype == 'router' and matching == True:
                            grup = AnsibleNetworkGroup.objects.get(name='Huawei')
                            savehost = AnsibleNetworkHost(host=cons,
                                                ansible_ssh_host=add_ip_ok,
                                                ansible_user='admin',
                                                ansible_ssh_pass='huawei12345',
                                                ansible_become_pass='huawei12345',
                                                device_type=de_type,
                                                group=grup)
                            savehost.save()
                            print(host)
                            conf = ce_router.objects.get(name=cons)
                            my_play = dict(
                                    name="hostname",
                                    hosts=cons,
                                    become='yes',
                                    become_method='enable',
                                    gather_facts='no',
                                    vars=[
                                        dict(ansible_command_timeout=120)
                                    ],
                                    tasks=[
                                        dict(action=dict(module='ce_config', commands=conf.hostname)),
                                        dict(action=dict(module='ce_config', lines=[conf.ospf, conf.ospf_area, conf.ospf_network]))
                                        ]
                                    )
                            result = execute(my_play)
                            print(conf.name)
                            print(result.results)
                            kondisi = result.stats
                            kond = kondisi['hosts'][0]['status']
                            if kond == 'ok':
                                devices.objects.filter(new_device_mac=mac_matching).update(stats='configured')
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='SUCCESS')
                            else:
                                fail = result.results
                                err = fail['failed'][0]['tasks'][0]['result']['msg'][0]
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='FAILED', messages=err)
                                print(f'{err}')
                        elif Huawei_os == True and dtype == 'switch' and matching == True:
                            grup = AnsibleNetworkGroup.objects.get(name='Huawei')
                            savehost = AnsibleNetworkHost(host=cons,
                                                ansible_ssh_host=add_ip_ok,
                                                ansible_user='admin',
                                                ansible_ssh_pass='huawei12345',
                                                ansible_become_pass='huawei12345',
                                                device_type=de_type,
                                                group=grup)
                            savehost.save()
                            print(host)
                            conf = ce_switch.objects.get(name=cons)
                            my_play = dict(
                                    name="hostname",
                                    hosts=cons,
                                    become='yes',
                                    become_method='enable',
                                    gather_facts='no',
                                    vars=[
                                        dict(ansible_command_timeout=120)
                                    ],
                                    tasks=[
                                        dict(action=dict(module='ce_config', commands=conf.hostname)),
                                        dict(action=dict(module='ce_config', commands=conf.vlan)),
                                        dict(action=dict(module='ce_config', lines=[conf.port_ip, conf.port_cmd1, conf.port_vlan]))
                                        ]
                                    )
                            result = execute(my_play)
                            print(conf.name)
                            print(result.results)
                            kondisi = result.stats
                            kond = kondisi['hosts'][0]['status']
                            if kond == 'ok':
                                devices.objects.filter(new_device_mac=mac_matching).update(stats='configured')
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='SUCCESS')
                            else:
                                fail = result.results
                                err = fail['failed'][0]['tasks'][0]['result']['msg'][0]
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='FAILED', messages=err)
                                print(f'{err}')
                        elif Cisco_os == True and dtype == 'switch' and matching == True:
                            grup = AnsibleNetworkGroup.objects.get(name='Cisco')
                            savehost = AnsibleNetworkHost(host=cons,
                                                    ansible_ssh_host=add_ip_ok,
                                                    ansible_user='indra',
                                                    ansible_ssh_pass='cisco',
                                                    ansible_become_pass='cisco',
                                                    device_type=de_type,
                                                    group=grup)
                            savehost.save()
                            conf = ios_switch.objects.get(name=cons)
                            my_play = dict(
                                    name="hostname",
                                    hosts=cons,
                                    become='yes',
                                    become_method='enable',
                                    gather_facts='no',
                                    vars=[
                                        dict(ansible_command_timeout=120)
                                    ],
                                    tasks=[
                                        dict(action=dict(module='ios_config', commands=conf.hostname)),
                                        dict(action=dict(module='ios_vlan', vlan_id=conf.vlan_id, name=conf.vlan_name))
                                    ]
                                )
                            result = execute(my_play)
                            kondisi = result.stats
                            kond = kondisi['hosts'][0]['status']
                            if kond == 'ok':
                                devices.objects.filter(new_device_mac=mac_matching).update(stats='configured')
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='SUCCESS')
                            else:
                                fail = result.results
                                err = fail['failed'][0]['tasks'][0]['result']['msg'][0]
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='FAILED', messages=err)
                                print(f'{err}')
                        elif Mikrotik_os == True and dtype == 'router' and matching == True:
                            grup = AnsibleNetworkGroup.objects.get(name='Mikrotik')
                            savehost = AnsibleNetworkHost(host=cons,
                                                    ansible_ssh_host=add_ip_ok,
                                                    ansible_user='mikrotik',
                                                    ansible_ssh_pass='54541691',
                                                    ansible_become_pass='54541691',
                                                    device_type=de_type,
                                                    group=grup)
                            savehost.save()
                            conf = routeros_router.objects.get(name=cons)
                            my_play = dict(
                                    name="hostname",
                                    hosts=cons,
                                    become='yes',
                                    become_method='enable',
                                    gather_facts='no',
                                    vars=[
                                        dict(ansible_command_timeout=120)
                                    ],
                                    tasks=[
                                        dict(action=dict(module='routeros_command', commands=conf.hostname)),
                                        dict(action=dict(module='routeros_command', commands=conf.ospf)),
                                        dict(action=dict(module='routeros_command', commands=conf.inter_vlan)),
                                        dict(action=dict(module='routeros_coomand', commands=conf.ip_add_vlan))
                                        ]
                                )
                            result = execute(my_play)
                            kondisi = result.stats
                            kond = kondisi['hosts'][0]['status']
                            if kond == 'ok':
                                devices.objects.filter(new_device_mac=mac_matching).update(stats='configured')
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='SUCCESS')
                            else:
                                fail = result.results
                                err = fail['failed'][0]['tasks'][0]['result']['msg'][0]
                                logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='FAILED', messages=err)
                                print(f'{err}')
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
                arpcisco(host, request)
                info = arp.objects.all().filter(device_id=host)
                context = {
                    'form': form,
                    'info': info
                }
                return render(request, 'ansibleweb/autoconfig.html', context)
            elif cannot == 0 and os == 'ce':
                arphuawei(host, request)
                info = arp.objects.all().filter(device_id=host)
                context = {
                    'form': form,
                    'info': info
                }
                return render(request, 'ansibleweb/autoconfig.html', context)
            elif cannot == 0 and os == 'routeros':
                arpmikrotik(host, request)
                info = arp.objects.all().filter(device_id=host)
                context = {
                    'form': form,
                    'info': info
                }
                return render(request, 'ansibleweb/autoconfig.html', context)
            else:
                if cannot > 0 and os == 'ce':
                    print("coba")
                    arp.objects.filter(device_id=data['hosts']).delete()
                    arphuawei(host, request)
                    info = arp.objects.all().filter(device_id=host)
                    context = {
                        'form': form,
                        'info': info
                    }
                    return render(request, 'ansibleweb/autoconfig.html', context)
                elif cannot > 0 and os == 'ios':
                    arp.objects.filter(device_id=data['hosts']).delete()
                    arpcisco(host, request)
                    info = arp.objects.all().filter(device_id=host)
                    context = {
                        'form': form,
                        'info': info
                    }
                    return render(request, 'ansibleweb/autoconfig.html', context)
                elif cannot > 0 and os == 'routeros':
                    arp.objects.filter(device_id=data['hosts']).delete()
                    arpmikrotik(host, request)
                    info = arp.objects.all().filter(device_id=host)
                    context = {
                        'form': form,
                        'info': info
                    }
                    return render(request, 'ansibleweb/autoconfig.html', context)
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
    hos = AnsibleNetworkHost.objects.get(id=device)
    os = hos.group.ansible_network_os
    tipe = hos.device_type
    print(hos.host)
    jumlah = arp.objects.all().filter(device_id=device)
    cannot = len(jumlah)
    ulang = True
    while ulang:
        if os == 'ios' and tipe == 'switch':
            arp.objects.filter(device_id=device).delete()
            broadcast = devices.objects.filter(device_id=device, port='Vlan1').values_list('ipadd')
            ping_ip = broadcast[0][0]
            dot = ping_ip.rfind('.')
            ipawal = ping_ip[:dot]
            getchar = ping_ip[dot:]
            for x in range(2, 20):
                ipakhir = getchar.replace(getchar, "."+str(x))
                change = ipawal+ipakhir
                print(change)
                my_play = dict(
                    name="Ping broadcast",
                    hosts=hos.host,
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
                hosts=hos.host,
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
                                device_id=hos)
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
                        findmac = match[z]# function Mengubah value match untuk mendapatkan vendor
                        mac_vendor = get_vendor(findmac)
                        print(mac_vendor)
                        findos = mac_os.objects.filter(oui=mac_vendor).values_list('vendor')
                        t_os = findos[0][0]#dapat vendor
                        print(t_os)
                        mac_matching = lower_mac(findmac)
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
                            ciscorouter(cons, de_type, add_ip_ok, mac_matching, akun, hos)
                        elif Cisco_os == True and dtype == 'switch' and matching > 0:
                            ciscoswitch(cons, de_type, add_ip_ok, mac_matching, akun, hos)
                        elif Huawei_os == True and dtype == 'router' and matching > 0:
                            huaweirouter(cons, add_ip_ok, de_type, mac_matching, akun, hos)
                        elif Huawei_os == True and dtype == 'switch' and matching > 0:
                            huaweiswitch(cons, add_ip_ok, de_type, mac_matching, akun, hos)
                        elif Mikrotik_os == True and dtype == 'router' and matching > 0:
                            mikrotikrouter(cons, de_type, add_ip_ok, mac_matching, akun, hos)
                        else:
                            logs = log.objects.filter(account=akun, targetss=host.host, action='Auto Configuration', status='PENDING').update(status='FAILED', messages='Port Tidak Sesuai')
        if os == 'ios' and tipe == 'router':
            arp.objects.filter(device_id=device).delete() # menghapus arp table
            listip = devices.objects.filter(device_id=device, stats='Booked').values_list('ipadd') # mendapatkan list Ip address yang dipesan portnya
            total = len(listip) #total list ip port yang dibooked
            for x in range(0, total): #melakukan perulangan pada tiap ip untuk diubah menjadi ip broadcast dan menjalankan ping broadcast
                ping_ip = listip[x][0]+str(56)
                dot = ping_ip.rfind('.')
                getchar = ping_ip[dot:]
                change = ping_ip.replace(getchar, ".255")
                print(change)
                my_play = dict(
                    name="Ping broadcast",
                    hosts=hos.host,
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
                result1 = execute(my_play)#eksekusi ping broadcast
            my_play2 = dict(
                name="show arp",
                hosts=hos.host,
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
            result = execute(my_play2)#setelah ping broadcast, arp table akan terupdate dengan perangkat baru
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
                                device_id=hos)
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
                print(mac_arp)
                print(mac_booked)
                print(match)
                jumlah = len(match)
                if jumlah > 0:
                    ulang = False
                    for z in range(0, jumlah):
                        findmac = match[z]#dlm bentuk aabb.ccdd.eeff
                        mac_vendor = get_vendor(findmac)
                        print(mac_vendor)
                        findos = mac_os.objects.filter(oui=mac_vendor).values_list('vendor')
                        t_os = findos[0][0]#dapat vendor
                        getportarp = arp.objects.filter(device_id=device, mac=findmac).values_list('port')
                        portarpp = getportarp[0][0]#'GigabitEthernet0/0/1'
                        cekking = devices.objects.filter(device_id=device, stats='Booked', port=portarpp).values_list('new_device_mac')#cek perangkat baru terpasang sesuai port atau tidak
                        convert_mac = cekking[0][0]
                        c_5 = convert_mac[:4]+"."+convert_mac[4:8]+"."+convert_mac[8:]#dlm bentuk ios aabb.ccdd.eeff
                        print(c_5)
                        print(t_os)
                        mac_matching = lower_mac(findmac)
                        matching = c_5 in findmac # matching mac Arp dengan mac booking 
                        de_type = devices.objects.filter(device_id=device, stats='Booked', port=portarpp).values_list('new_device_type')
                        dtype = de_type[0][0]
                        add_ip = arp.objects.filter(mac=findmac).values_list('ipadd')
                        add_ip_ok = add_ip[0][0]
                        print(add_ip_ok)
                        precon = devices.objects.filter(device_id=device, stats='Booked', port=portarpp).values_list('preconf')
                        cons = precon[0][0]
                        Huawei_os = "Huawei" in t_os
                        Cisco_os = "Cisco" in t_os
                        Mikrotik_os= "Routerboard" in t_os
                        print(Huawei_os)
                        print(Cisco_os)
                        print(Mikrotik_os)
                        if Cisco_os == True and dtype == 'router' and matching == True:
                            ciscorouter(cons, de_type, add_ip_ok, mac_matching, akun, hos)
                        elif Cisco_os == True and dtype == 'switch' and matching == True:
                            ciscoswitch(cons, de_type, add_ip_ok, mac_matching, akun, hos)
                        elif Huawei_os == True and dtype == 'router' and matching == True:
                            huaweirouter(cons, add_ip_ok, de_type, mac_matching, akun, hos)
                        elif Huawei_os == True and dtype == 'switch' and matching == True:
                            huaweiswitch(cons, add_ip_ok, de_type, mac_matching, akun, hos)
                        elif Mikrotik_os == True and dtype == 'router' and matching == True:
                            mikrotikrouter(cons, de_type, add_ip_ok, mac_matching, akun, hos)
                        else:
                            logs = log.objects.filter(account=akun, targetss=hos.host, action='Auto Configuration', status='PENDING').update(status='FAILED', messages='Port Tidak Sesuai')
        elif os == 'ce' and tipe == 'router':
            arp.objects.filter(device_id=device).delete()
            listip = devices.objects.filter(device_id=device, stats='Booked').values_list('ipadd') # mendapatkan list Ip address yang dipesan portnya
            total = len(listip) #total list ip port yang dibooked
            for x in range(0, total): #melakukan perulangan pada tiap ip untuk diubah menjadi ip broadcast dan menjalankan ping broadcast
                ping_ip = listip[x][0]+str(56)
                dot = ping_ip.rfind('.')
                getchar = ping_ip[dot:]
                change = ping_ip.replace(getchar, ".255")
                print(change)
                my_play = dict(
                    name="Ping broadcast",
                    hosts=hos.host,
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
                result1 = execute(my_play)#eksekusi ping broadcast
            my_play2 = dict(
                name="show arp",
                hosts=hos.host,
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
            print(my_play2)
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
                                device_id=hos)
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
                        mac_vendor = get_vendor(findmac)
                        print(mac_vendor)
                        findos = mac_os.objects.filter(oui=mac_vendor).values_list('vendor')
                        t_os = findos[0][0]
                        getportarp = arp.objects.filter(device_id=device, mac=findmac).values_list('port')
                        portarpp = getportarp[0][0]
                        cekkamus = kamusport.objects.filter(portarp=portarpp).values_list('portint')
                        portout = cekkamus[0][0]
                        cekking = devices.objects.filter(device_id=device, stats='Booked', port=portout).values_list('new_device_mac')
                        convert_mac = cekking[0][0]
                        c_5 = convert_mac[:4]+"-"+convert_mac[4:8]+"-"+convert_mac[8:]
                        matching = c_5 in findmac
                        de_type = devices.objects.filter(device_id=device, stats='Booked', port=portout).values_list('new_device_type')
                        dtype = de_type[0][0]
                        add_ip = arp.objects.filter(mac=findmac).values_list('ipadd')
                        add_ip_ok = add_ip[0][0]
                        print(add_ip_ok)
                        precon = devices.objects.filter(device_id=device, stats='Booked', port=portout).values_list('preconf')
                        cons = precon[0][0]
                        Huawei_os = "Huawei" in t_os
                        Cisco_os = "Cisco" in t_os
                        Mikrotik_os= "Mikrotik" in t_os
                        print(t_os)
                        print(findmac)
                        if Cisco_os == True and dtype == 'router' and matching == True:
                            ciscorouter(cons, de_type, add_ip_ok, findmac, akun, hos)
                        elif Cisco_os == True and dtype == 'switch' and matching == True:
                            ciscoswitch(cons, de_type, add_ip_ok, findmac, akun, hos)
                        elif Huawei_os == True and dtype == 'router' and matching == True:
                            huaweirouter(cons, add_ip_ok, de_type, mac_matching, akun, hos)
                        elif Huawei_os == True and dtype == 'switch' and matching == True:
                            huaweiswitch(cons, add_ip_ok, de_type, mac_matching, akun, hos)
                        elif Mikrotik_os == True and dtype == 'router' and matching == True:
                            mikrotikrouter(cons, de_type, add_ip_ok, mac_matching, akun, hos)
                        else:
                            logs = log.objects.filter(account=akun, targetss=hos.host, action='Auto Configuration', status='PENDING').update(status='FAILED', messages='Port Tidak Sesuai')
        elif os == 'ce' and tipe == 'switch':
            broadcast = arp.objects.filter(device_id=device, port='Vlanif1').values_list('ipadd')
            ping_ip = broadcast[0][0]
            print(broadcast)
            print(ping_ip)
            dot = ping_ip.rfind('.')
            ipawal = ping_ip[:dot]
            getchar = ping_ip[dot:]
            for x in range(2, 10):
                ipakhir = getchar.replace(getchar, "."+str(x))
                change = ipawal+ipakhir
                print(change)
                my_play = dict(
                    name="Ping broadcast",
                    hosts=hos.host,
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
            arp.objects.filter(device_id=device).delete()
            my_play2 = dict(
                name="show arp",
                hosts=hos.host,
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
                                device_id=hos)
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
                        mac_vendor = get_vendor(findmac)
                        print(mac_vendor)
                        findos = mac_os.objects.filter(oui=mac_vendor).values_list('vendor')
                        t_os = findos[0][0]
                        print(t_os)
                        print(findmac)
                        mac_matching = lower_mac(findmac)
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
                        print(hos.group)
                        Huawei_os = "Huawei" in t_os
                        Cisco_os = "Cisco" in t_os
                        Mikrotik_os= "Mikrotik" in t_os
                        print(Huawei_os)
                        print(Cisco_os)
                        print(Mikrotik_os)
                        if Cisco_os == True and dtype == 'router' and matching > 0:
                            ciscorouter(cons, de_type, add_ip_ok, mac_matching, akun, hos)
                        elif Huawei_os == True and dtype == 'router' and matching > 0:
                            huaweirouter(cons, add_ip_ok, de_type, mac_matching, akun, hos)
                        elif Huawei_os == True and dtype == 'switch' and matching > 0:
                            huaweiswitch(cons, add_ip_ok, de_type, mac_matching, akun, hos)
                        elif Cisco_os == True and dtype == 'switch' and matching > 0:
                            ciscoswitch(cons, de_type, add_ip_ok, mac_matching, akun, hos)
                        elif Mikrotik_os == True and dtype == 'router' and matching > 0:
                            mikrotikrouter(cons, de_type, add_ip_ok, mac_matching, akun, hos)
                        else:
                            logs = log.objects.filter(account=akun, targetss=hos.host, action='Auto Configuration', status='PENDING').update(status='FAILED', messages='Port Tidak Sesuai')
        elif os == 'routeros' and tipe == 'router':
            arp.objects.filter(device_id=device).delete()
            listip = devices.objects.filter(device_id=device, stats='Booked').values_list('ipadd')
            total = len(listip)
            my_play = dict(
                name="Ping broadcast",
                hosts=hos.host,
                become='yes',
                become_method='enable',
                gather_facts='no',
                vars=[
                        dict(ansible_command_timeout=10)
                ],
                tasks=[
                    dict(action=dict(module='routeros_command', commands='ping 255.255.255.255'))
                ]
            )
            result1 = execute(my_play)#eksekusi ping broadcast
            my_play1 = dict(name="show arp",
                            hosts=hos.host,
                            become='yes',
                            become_method='enable',
                            gather_facts='no',
                            vars=[
                                dict(ansible_command_timeout=40)
                            ],
                            tasks=[
                                dict(action=dict(module='routeros_command', commands='/ip arp print'))
                                ]
                            )
            result = execute(my_play1)
            print(my_play1)
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
                    ip = dataport[x][5:20].replace(" ","")
                    mac = dataport[x][21:39].replace(" ","")
                    portt = dataport[x][39:46].replace(" ","")
                    coba = arp(ipadd=ip,
                                mac=mac,
                                port=portt,
                                device_id=hos)
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
                        findmac = match[z]#dlm bentuk AA:BB:CC:DD:EE
                        print(findmac)
                        mac_matching = lower_mac(findmac)
                        mac_vendor = get_vendor(findmac)
                        print(mac_vendor)
                        findos = mac_os.objects.filter(oui=mac_vendor).values_list('vendor')
                        t_os = findos[0][0]#dpt vendor
                        getportarp = arp.objects.filter(device_id=device, mac=findmac).values_list('port')
                        portarpp = getportarp[0][0]
                        cekking = devices.objects.filter(device_id=device, stats='Booked', port=portarpp).values_list('new_device_mac')
                        convert_mac = cekking[0][0]
                        c_4 = convert_mac.upper()
                        c_5 = c_4[:2]+":"+c_4[2:4]+":"+c_4[4:6]+":"+c_4[6:8]+":"+c_4[8:10]+":"+c_4[10:]
                        print(c_5)
                        matching = c_5 in findmac
                        de_type = devices.objects.filter(device_id=device, stats='Booked', port=portarpp).values_list('new_device_type')
                        dtype = de_type[0][0]
                        add_ip = arp.objects.filter(mac=findmac).values_list('ipadd')
                        add_ip_ok = add_ip[0][0]
                        print(add_ip_ok)
                        precon = devices.objects.filter(device_id=device, stats='Booked', port=portarpp).values_list('preconf')
                        cons = precon[0][0]
                        print(cons)
                        print(t_os)
                        Huawei_os = "Huawei" in t_os
                        Cisco_os = "Cisco" in t_os
                        Mikrotik_os= "Routerboard" in t_os
                        print(Huawei_os)
                        print(Cisco_os)
                        print(Mikrotik_os)
                        if Cisco_os == True and dtype == 'router' and matching == True:
                            ciscorouter(cons, de_type, add_ip_ok , mac_matching, akun, hos)
                        elif Huawei_os == True and dtype == 'router' and matching == True:
                            huaweirouter(cons, add_ip_ok, de_type, mac_matching, akun, hos)
                        elif Huawei_os == True and dtype == 'switch' and matching == True:
                            huaweiswitch(cons, add_ip_ok, de_type, mac_matching, akun, hos)
                        elif Cisco_os == True and dtype == 'switch' and matching == True:
                            ciscoswitch(cons, add_ip_ok, de_type, mac_matching, akun, hos)
                        elif Mikrotik_os == True and dtype == 'router' and matching == True:
                            mikrotikrouter(cons, de_type, add_ip_ok, mac_matching, akun, hos)

def ciscorouter(cons, de_type, add_ip_ok, mac_matching, akun, hos):
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
        name="autoconf",
        hosts=cons,
        become='yes',
        become_method='enable',
        gather_facts='no',
        vars=[
            dict(ansible_command_timeout=500)
        ],
        tasks=[
            dict(action=dict(module='ios_config', commands='hostname '+conf.hostname)),
            dict(action=dict(module='ios_config', lines=['default-router '+conf.default_router, 'network '+conf.dhcp_network+' '+conf.dhcp_mask], parents='ip dhcp pool '+conf.dhcp_pool)),
            dict(action=dict(module='ios_config', lines=['default-router '+conf.default_router2, 'network '+conf.dhcp_network2+' '+conf.dhcp_mask2], parents='ip dhcp pool '+conf.dhcp_pool2)),
            dict(action=dict(module='ios_config', lines=['default-router '+conf.default_router3, 'network '+conf.dhcp_network3+' '+conf.dhcp_mask3], parents='ip dhcp pool '+conf.dhcp_pool3)),
            dict(action=dict(module='ios_config', commands='ip dhcp excluded-address '+conf.dhcp_excluded)),
            dict(action=dict(module='ios_config', commands='ip dhcp excluded-address '+conf.dhcp_excluded2)),
            dict(action=dict(module='ios_config', commands='ip dhcp excluded-address '+conf.dhcp_excluded3)),
            dict(action=dict(module='ios_config', lines=['encapsulation dot1q '+conf.i_vlan_enc, 'ip address '+conf.i_vlan_cmd+' '+conf.i_vlan_mask], parents='int '+conf.i_vlan_int)),
            dict(action=dict(module='ios_config', lines=['encapsulation dot1q '+conf.i_vlan_enc2, 'ip address '+conf.i_vlan_cmd2+' '+conf.i_vlan_mask2], parents='int '+conf.i_vlan_int2)),
            dict(action=dict(module='ios_config', lines=['ip address '+conf.port_cmd+' '+conf.port_mask, 'no sh'], parents='int '+conf.port_ip)),
            dict(action=dict(module='ios_config', lines='network '+conf.ospf_network+' '+conf.ospf_mask+' area '+conf.ospf_area, parents='router ospf 1')),
            dict(action=dict(module='ios_config', lines='network '+conf.ospf_network2+' '+conf.ospf_mask2+' area '+conf.ospf_area2, parents='router ospf 1')),
            dict(action=dict(module='ios_config', lines='network '+conf.ospf_network3+' '+conf.ospf_mask3+' area '+conf.ospf_area3, parents='router ospf 1')),
            dict(action=dict(module='ios_config', commands='ip route 0.0.0.0 0.0.0.0 '+conf.default_gateway)),
            dict(action=dict(module='ios_config', commands='ip scp server enable')),
            dict(action=dict(module='ios_config', commands='ip address '+add_ip_ok+' 255.255.255.0', parents='int g0/0'))
        ]
    )
    result=execute(my_play)
    print(my_play)
    kondisi = result.stats
    kond = kondisi['hosts'][0]['status']
    print(result.results)
    if kond == 'ok':
        print('Success autoconfig')
        devices.objects.filter(new_device_mac=mac_matching).update(stats='configured')
        logs = log.objects.filter(account=akun, targetss=hos.host, action='Auto Configuration', status='PENDING').update(status='Success')
    else:
        print('Failed autoconfig')
        fail = result.results
        err = fail['failed'][0]['tasks'][0]['result']['msg']
        logs = log.objects.filter(account=akun, targetss=hos.host, action='Auto Configuration', status='PENDING').update(status='Failed', messages=err)
        print(f'{err}')

def ciscoswitch(cons, add_ip_ok, de_type, mac_matching, akun, hos):
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
    conf = ios_switch.objects.get(name=cons)
    print(add_ip_ok)
    my_play = dict(
        name="Autoconfig",
        hosts=cons,
        become='yes',
        become_method='enable',
        gather_facts='no',
        vars=[
            dict(ansible_command_timeout=120)
        ],
        tasks=[
            dict(action=dict(module='ios_vlan', vlan_id=conf.vlan_id, name=conf.vlan_name)),
            dict(action=dict(module='ios_vlan', vlan_id=conf.vlan_id2, name=conf.vlan_name2)),
            dict(action=dict(module='ios_vlan', vlan_id=conf.vlan_id3, name=conf.vlan_name3)),
            dict(action=dict(module='ios_config', lines=['sw mo '+conf.mode, 'sw ac vl '+conf.vlan], parents='int '+conf.interface)),
            dict(action=dict(module='ios_config', lines=['sw mo '+conf.mode2, 'sw ac vl '+conf.vlan2], parents='int '+conf.interface2)),
            dict(action=dict(module='ios_config', commands='ip scp server enable')),
            dict(action=dict(module='ios_config', commands='lldp run'))
        ]
    )
    result = execute(my_play)
    kondisi = result.stats
    kond = kondisi['hosts'][0]['status']
    if kond == 'ok':
        print('Success autoconfig')
        print(result.results)
        devices.objects.filter(new_device_mac=mac_matching).update(stats='configured')
        logs = log.objects.filter(account=akun, targetss=hos.host, action='Auto Configuration', status='PENDING').update(status='Success')
    else:
        print('Failed autoconfig')
        fail = result.results
        err = fail['failed'][0]['tasks'][0]['result']['msg']
        logs = log.objects.filter(account=akun, targetss=hos.host, action='Auto Configuration', status='PENDING').update(status='Failed', messages=err)
        print(f'{err}')	

def huaweiswitch(cons, add_ip_ok, de_type, mac_matching, akun, hos):
    grup = AnsibleNetworkGroup.objects.get(name='Huawei')
    savehost = AnsibleNetworkHost(host=cons,
            ansible_ssh_host=add_ip_ok,
            ansible_user='admin',
            ansible_ssh_pass='huawei12345',
            ansible_become_pass='huawei12345',
            device_type=de_type,
            group=grup)
    savehost.save()
    conf = ios_switch.objects.get(name=cons)
    my_play=dict(
        name="Autoconfig",
        hosts=cons,
        become='yes',
        become_method='enable',
        gather_facts='no',
        vars=[
            dict(ansible_command_timeout=120)
        ],
        tasks=[
            dict(action=dict(module='ce_config', lines=['interface '+conf.interface, 'port link-type '+conf.mode])),
            dict(action=dict(module='ce_config', lines=['interface '+conf.interface2, 'port link-type '+conf.mode2])),
            dict(action=dict(module='ce_config', lines=['vlan '+conf.vlan, 'port '+conf.interface])),
            dict(action=dict(module='ce_config', lines=['vlan '+conf.vlan2, 'port '+conf.interface2])),
            dict(action=dict(module='ce_config', lines=['vlan '+conf.vlan_id, 'description '+conf.vlan_name])),
            dict(action=dict(module='ce_config', lines=['vlan '+conf.vlan_id2, 'description '+conf.vlan_name2])),
            dict(action=dict(module='ce_config', lines=['vlan '+conf.vlan_id3, 'description '+conf.vlan_name3])),
            dict(action=dict(module='ce_config', lines=['lldp enable'])),
            dict(action=dict(module='ce_config', lines=['ip route-static 0.0.0.0 0.0.0.0 '+conf.gateway])),
            dict(action=dict(module='ce_config', lines=['scp server enable'])),
            dict(action=dict(module='ce_config', lines=['int vl 1', 'ip address '+add_ip_ok+' 255.255.255.0']))
        ]
    )
    result=execute(my_play)
    kondisi = result.stats
    kond = kondisi['hosts'][0]['status']
    if kond == 'ok':
        print('Success autoconfig')
        devices.objects.filter(new_device_mac=mac_matching).update(stats='configured')
        logs = log.objects.filter(account=akun, targetss=hos.host, action='Auto Configuration', status='PENDING').update(status='Success')
    else:
        print('Failed autoconfig')
        fail = result.results
        err = fail['failed'][0]['tasks'][0]['result']['msg']
        logs = log.objects.filter(account=akun, targetss=hos.host, action='Auto Configuration', status='PENDING').update(status='Failed', messages=err)
        print(f'{err}')

def mikrotikrouter(cons, de_type, add_ip_ok, mac_matching, akun, hos):
    grup = AnsibleNetworkGroup.objects.get(name='Mikrotik')
    savehost = AnsibleNetworkHost(host=cons,
                ansible_ssh_host=add_ip_ok,
                ansible_user='mikrotik',
                ansible_ssh_pass='54541691',
                ansible_become_pass='54541691',
                device_type=de_type,
                group=grup)
    savehost.save()
    conf = iosrouter.objects.get(name=cons)
    my_play = dict(
        name="Autoconfig",
        hosts=cons,
        become='yes',
        become_method='enable',
        gather_facts='no',
        vars=[
            dict(ansible_command_timeout=120)
        ],
        tasks=[
            dict(action=dict(module='routeros_command', commands='/system identitiy set name='+conf.hostname)),
            dict(action=dict(module='routeros_command', commands='/ip pool add name='+conf.dhcp_pool+' ranges='+conf.dhcp_excluded)),
            dict(action=dict(module='routeros_command', commands='/ip dhcp-server network add address '+conf.dhcp_network+'/'+conf.dhcp_mask+' gateway='+conf.default_router)),
            dict(action=dict(module='routeros_command', commands='/ip pool add name='+conf.dhcp_pool2+' ranges='+conf.dhcp_excluded2)),
            dict(action=dict(module='routeros_command', commands='/ip dhcp-server network add address '+conf.dhcp_network2+'/'+conf.dhcp_mask2+' gateway='+conf.default_router2)),
            dict(action=dict(module='routeros_command', commands='/ip pool add name='+conf.dhcp_pool3+' ranges='+conf.dhcp_excluded3)),
            dict(action=dict(module='routeros_command', commands='/ip dhcp-server network add address '+conf.dhcp_network3+'/'+conf.dhcp_mask3+' gateway='+conf.default_router3)),
            dict(action=dict(module='routeros_command', commands='/ip address add address='+conf.port_cmd+'/'+conf.port_mask+' interface='+conf.port_ip)),
            dict(action=dict(module='routeros_command', commands='/interface vlan add name=vlan'+conf.i_vlan_enc+' vlan-id='+conf.i_vlan_enc+' interface='+conf.i_vlan_int)),
            dict(action=dict(module='routeros_command', commands='/ip address add address='+conf.i_vlan_cmd+'/'+conf.i_vlan_mask+' interface=vlan'+conf.i_vlan_enc)),
            dict(action=dict(module='routeros_command', commands='/interface vlan add name=vlan'+conf.i_vlan_enc2+' vlan-id='+conf.i_vlan_enc2+' interface='+conf.i_vlan_int2)),
            dict(action=dict(module='routeros_command', commands='/ip address add address='+conf.i_vlan_cmd2+'/'+conf.i_vlan_mask2+' interface=vlan'+conf.i_vlan_enc2)),
            dict(action=dict(module='routeros_command', commands='/routing ospf network add network='+conf.ospf_network+'/'+conf.ospf_mask+' area='+conf.ospf_area)),
            dict(action=dict(module='routeros_command', commands='/routing ospf network add network='+conf.ospf_network2+'/'+conf.ospf_mask2+' area='+conf.ospf_area2)),
            dict(action=dict(module='routeros_command', commands='/routing ospf network add network='+conf.ospf_network3+'/'+conf.ospf_mask3+' area='+conf.ospf_area3)),
            dict(action=dict(module='routeros_command', commands='/ip route add dst-address=0.0.0.0/0 gateway='+conf.default_gateway)),
            dict(action=dict(module='routeros_command', commands='/ip address add address='+add_ip_ok+'/24 interface=ether1')),
            dict(action=dict(module='routeros_command', commands='/ip dhcp-client remove 0'))

            #tambahin ip dhcp-server add interface address-pool= trus di enable
        ]
    )
    result = execute(my_play)
    kondisi = result.stats
    kond = kondisi['hosts'][0]['status']
    if kond == 'ok':
        print('Success autoconfig')
        devices.objects.filter(new_device_mac=mac_matching).update(stats='configured')
        logs = log.objects.filter(account=akun, targetss=hos.host, action='Auto Configuration', status='PENDING').update(status='Success')
    else:
        print('Failed autoconfig')
        fail = result.results
        err = fail['failed'][0]['tasks'][0]['result']['msg']
        logs = log.objects.filter(account=akun, targetss=hos.host, action='Auto Configuration', status='PENDING').update(status='Failed', messages=err)

def huaweirouter(cons, add_ip_ok, de_type, mac_matching, akun, hos):
    grup = AnsibleNetworkGroup.objects.get(name='Huawei')
    savehost = AnsibleNetworkHost(host=cons,
            ansible_ssh_host=add_ip_ok,
            ansible_user='admin',
            ansible_ssh_pass='huawei12345',
            ansible_become_pass='huawei12345',
            device_type=de_type,
            group=grup)
    savehost.save()
    conf = iosrouter.objects.get(name=cons)
    my_play=dict(
        name="Autoconfig",
        hosts=cons,
        become='yes',
        become_method='enable',
        gather_facts='no',
        vars=[
            dict(ansible_command_timeout=120)
        ],
        tasks=[
            dict(action=dict(module='ce_config', lines=['dhcp enable', 'ip pool '+conf.dhcp_pool, 'network '+conf.dhcp_network+' mask '+conf.dhcp_mask, 'gateway-list '+conf.default_router, 'excluded-ip-address '+conf.dhcp_excluded])),
            dict(action=dict(module='ce_config', lines=['ip pool '+conf.dhcp_pool2, 'network '+conf.dhcp_network2+' mask '+conf.dhcp_mask2, 'gateway-list '+conf.default_router2, 'excluded-ip-address '+conf.dhcp_excluded2])),
            dict(action=dict(module='ce_config', lines=['ip pool '+conf.dhcp_pool3, 'network '+conf.dhcp_network3+' mask '+conf.dhcp_mask3, 'gateway-list '+conf.default_router3, 'excluded-ip-address '+conf.dhcp_excluded3])),
            dict(action=dict(module='ce_config', lines=['int '+conf.port_ip, 'ip add '+conf.port_cmd+' '+conf.port_mask, 'dhcp select interface', 'undo sh'])),
            dict(action=dict(module='ce_config', lines=['int '+conf.i_vlan_int, 'ip address '+conf.i_vlan_cmd+' '+conf.i_vlan_mask, 'dot1q termination vid '+enc.i_vlan_enc])),
            dict(action=dict(module='ce_config', lines=['int '+conf.i_vlan_int2, 'ip address '+conf.i_vlan_cmd2+' '+conf.i_vlan_mask2, 'dot1q termination vid '+enc.i_vlan_enc2])),
            dict(action=dict(module='ce_config', lines=['ospf', 'area '+conf.ospf_area, 'network '+conf.ospf_network+' '+conf.ospf_mask])),
            dict(action=dict(module='ce_config', lines=['ospf', 'area '+conf.ospf_area2, 'network '+conf.ospf_network2+' '+conf.ospf_mask2])),
            dict(action=dict(module='ce_config', lines=['ospf', 'area '+conf.ospf_area3, 'network '+conf.ospf_network3+' '+conf.ospf_mask3])),
            dict(action=dict(module='ce_config', lines=['ip route-static 0.0.0.0 0.0.0.0 '+conf.default_gateway])),
            dict(action=dict(module='ce_config', lines=['lldp enable'])),
            dict(action=dict(module='ce_config', lines=['scp server enable'])),
            dict(action=dict(module='ce_config', lines=['int g0/0', 'ip address '+add_ip_ok+' 255.255.255.0']))
        ]
    )
    result=execute(my_play)
    kondisi = result.stats
    kond = kondisi['hosts'][0]['status']
    if kond == 'ok':
        print('Success autoconfig')
        devices.objects.filter(new_device_mac=mac_matching).update(stats='configured')
        logs = log.objects.filter(account=akun, targetss=hos.host, action='Auto Configuration', status='PENDING').update(status='Success')
    else:
        print('Failed autoconfig')
        fail = result.results
        err = fail['failed'][0]['tasks'][0]['result']['msg']
        logs = log.objects.filter(account=akun, targetss=hos.host, action='Auto Configuration', status='PENDING').update(status='Failed', messages=err)
        print(f'{err}')
    
def get_vendor(findmac):
    get1 = findmac.replace("-","")
    get2 = get1.replace(".","")
    get3 = get2.replace(":","")
    get4 = get3.upper()#dlm bentuk AABBCCDDEEFF
    get5 = get4[:6]#dlm bentuk AABBCC
    get6 = get5[:2]+":"+get5[2:4]+":"+get5[4:6]#dlm bentuk AA:BB:CC
    return(get6)

def lower_mac(findmac):
    get1 = findmac.replace("-","")
    get2 = get1.replace(".","")
    get3 = get2.replace(":","")
    get4 = get3.lower()
    return(get4)

def arpcisco(host, request):
    my_play = dict(
        name = "show arp",
        hosts = host.host,
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
    else:
        messages.warning(request, f'Check Connection to Remote Host!')
        return redirect('arp')

def arpmikrotik(host, request):
    my_play = dict(
        name = "show arp",
        hosts = host.host,
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
    condition = result.stats
    con = condition['hosts'][0]['status']
    if con == 'ok':
        output = result.results
        dataport = output['success'][0]['tasks'][0]['result']['stdout_lines'][0][3:]
        maks = len(dataport)
        for x in range(0, maks):
            ip = dataport[x][5:20].replace(" ","")
            mac = dataport[x][21:39].replace(" ","")
            portt = dataport[x][39:46].replace(" ","")
            coba = arp(ipadd=ip,
                        mac=mac,
                        port=portt,
                        device_id=host)
            coba.save()
    else:
         messages.warning(request, f'Check Connection to Remote Host!')
         return redirect('arp')

def arphuawei(host, request):
    my_play = dict(
        name = "show arp",
        hosts = host.host,
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
    else:
         messages.warning(request, f'Check Connection to Remote Host!')
         return redirect('arp')

from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .models import PostInventoryGroup, PostInventoryHost ,PostPlayBookForm, TaskForm, log, group, addinfodevice , ios_router, preconfdevice, arp, ce_router_form, ce_router, kamusport, ios_switch, ios_switch_form, devices, iosrouter
from .forms import hostnamecisco, vlan_cisco, ospf_cisco, ciscobackup, ciscorestore, hostnamehuawei, ospf_huawei, intervlan_huawei, huaweibackup, hostnamemikrotik, ipaddmikrotik, ospf_mikrotik, mikrotikbackup, huaweirestore, mikrotikrestore, autoconfig
from django.contrib import messages
from django.db.models.fields.related import ManyToManyField
#from djansible.models import PlayBooks
from itertools import chain
from dj_ansible.models import AnsibleNetworkHost, AnsibleNetworkGroup
from dj_ansible.ansible_kit import execute
import json
from datetime import datetime
#from djansible.ansible_kit.executor import execute


# Create your views here.
# skaoksoaksoakas

posts = [
    {
        'author': 'Broto',
        'title': 'Ansible Post 1',
        'content': 'First post content',
        'date_posted': 'Maret 11, 2018'
    },
    {
        'author': 'Indra',
        'title': 'Ansible Post 2',
        'content': 'First post content',
        'date_posted': 'Maret 13, 2018'
    }

]
@login_required
def home(request):
    all_device = AnsibleNetworkHost.objects.all()
    context = {
        'all_device': len(all_device)
    }
    return render(request, 'ansibleweb/home.html', context)

def topologi(request):
    return render(request, 'ansibleweb/topologi.html')

def devicess(request):
    all_device = AnsibleNetworkHost.objects.all()
    all_group = AnsibleNetworkGroup.objects.all()

    context = {
        'all_device': all_device,
        'all_group': all_group
    }
    return render(request, 'ansibleweb/device.html', context)

def updategroup(request, pk):
    group = AnsibleNetworkGroup.objects.get(id=pk)
    form = PostInventoryGroup(instance=group)

    if request.method == 'POST':
        form = PostInventoryGroup(request.POST, instance=device)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context = {'form': form}
    return render(request, 'ansibleweb/post_group.html', context)


def updatedevice(request, pk):
    device = AnsibleNetworkHost.objects.get(id=pk)
    form = PostInventoryHost(instance=device)
    
    if request.method == 'POST':
        form = PostInventoryHost(request.POST, instance=device)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context = {'form': form}
    return render(request, 'ansibleweb/post_host.html',context)


def infodevice(request, pk):
    perangkat = AnsibleNetworkHost.objects.get(id=pk)
    info = devices.objects.all().filter(device_id=perangkat)

    context = {
        'perangkat': perangkat,
        'info': info
    }
    return render(request, 'ansibleweb/infodevice.html', context)

def deletegroup(request, id):
    group = AnsibleNetworkGroup.objects.get(pk=id)
    group.delete()
    return redirect('device')

def deletedevice(request, id):
    device = AnsibleNetworkHost.objects.get(pk=id)
    device.delete()
    return redirect('device')

def prenewdevice(request, pk):
    select = devices.objects.get(id=pk)
    if request.method == 'POST':
        form_device = preconfdevice(request.POST)
        if form_device.is_valid():
            print(request.POST)
            data = request.POST
            fil = select.id
            devices.objects.filter(id=fil).update(new_device_type=data['tipe'], new_device_os=data['os'])
            messages.success(request, f'Successfully create PreDevice!')
            return redirect('device')
    else:
        form_device = preconfdevice()

    context= {
        'form_device': form_device
    }
    return render(request, 'ansibleweb/prenewdevice.html', context)

def prekonfig(request, pk):
    select = devices.objects.get(id=pk)
    tipe = select.new_device_type
    cek = select.new_device_os
    state = select.preconf
    if cek == 'ios' and tipe == 'router':
        if state == 'empty':
            if request.method == 'POST':
                form_ios = ios_router(request.POST)
                if form_ios.is_valid():
                    data = request.POST
                    print(request.POST)
                    coba = iosrouter(name=data['name'],
                                    hostname='hostname '+data['name'],
                                    port_ip=data['port_ip'],
                                    port_cmd='ip add '+data['port_cmd'],
                                    i_vlan_int='int '+data['i_vlan_int'],
                                    i_vlan_enc='encapsulation dot1Q '+data['i_vlan_enc'],
                                    i_vlan_cmd='ip address '+data['i_vlan_cmd'],
                                    ospf='router ospf '+data['ospf'],
                                    ospf_network='network '+data['ospf_network'],
                                    ospf_area=data['ospf_area'],
                                    dhcp_network='network '+data['dhcp_network'],
                                    default_router ='default-router '+data['default_router'],
                                    dns_server='dns-server '+data['dns_server'],
                                    dhcp_pool='ip dhcp pool'+data['dhcp_pool'],
                                    port_id=select)
                    coba.save()
                    idd = select.id
                    devices.objects.filter(id=idd).update(preconf=data['hostname'] ,new_device_mac=data['mac'] ,stats='Booked')
                    messages.success(request, f'Successfully create PreConfiguration!')
                    return redirect('/')
            else:
                form_ios = ios_router()
                messages.warning(request, f'tidak valid')

            context = {
                'form_ios': form_ios
            }
            return render(request, 'ansibleweb/iospreconfig.html', context)
        else:
            if request.method == 'POST':
                form_ios = ios_router(request.POST)
                if form_ios.is_valid():
                    data = request.POST
                    print(request.POST)
                    iosrouter.objects.filter(port_id=select).update(name=data['name'],
                                                                    hostname='hostname '+data['name'],
                                                                    port_ip=data['port_ip'],
                                                                    port_cmd='ip add '+data['port_cmd'],
                                                                    i_vlan_int='int '+data['i_vlan_int'],
                                                                    i_vlan_enc='encapsulation dot1Q '+data['i_vlan_enc'],
                                                                    i_vlan_cmd='ip address '+data['i_vlan_cmd'],
                                                                    ospf='router ospf '+data['ospf'],
                                                                    ospf_network='network '+data['ospf_network'],
                                                                    ospf_area=data['ospf_area'],
                                                                    dhcp_network='network '+data['dhcp_network'],
                                                                    default_router ='default-router '+data['default_router'],
                                                                    dns_server='dns-server '+data['dns_server'],
                                                                    dhcp_pool='ip dhcp pool'+data['dhcp_pool'])
                    update = select.id
                    devices.objects.filter(id=update).update(preconf=data['hostname'], new_device_mac=data['mac'])
                    messages.success(request, f'Successfully update PreConfiguration!')
                    return redirect('/')
            else:
                form_ios = ios_router()
            
            context = {
                'form_ios': form_ios
            }
            return render(request, 'ansibleweb/iospreconfig.html', context)
    elif cek == 'ios' and tipe == 'switch':
        if state == 'empty':
            if request.method == 'POST':
                form_ios = ios_switch_form(request.POST)
                if form_ios.is_valid():
                    data = request.POST
                    print(request.POST)
                    coba = ios_switch(name=data['name'],
                                    hostname='sysname '+data['name'],
                                    vlan_id=data['vlan_id'],
                                    vlan_name=data['vlan_name'])
                    coba.save()
                    idd = select.id
                    devices.objects.filter(id=idd).update(preconf=data['name'] ,new_device_mac=data['mac'] ,stats='Booked')
                    messages.success(request, f'Successfully create PreConfiguration!')
                    return redirect('/')
            else:
                form_ios = ios_switch_form()

            context = {
                'form_ios': form_ios
            }
            return render(request, 'ansibleweb/ios_switch_form.html', context)

    elif cek == 'ce' and tipe == 'router':
        if state == 'empty':
            if request.method == 'POST':
                form_ce = ce_router_form(request.POST)
                if form_ce.is_valid():
                    data = request.POST
                    print(request.POST)
                    coba = ce_router(name='sysname '+data['name'],
                                    port_ip='int '+data['port_ip'],
                                    ip_add='ip add '+data['ip_add'],
                                    i_vlan_int='int '+data['i_vlan_int'],
                                    i_vlan_ip='ip address '+data['i_vlan_ip'],
                                    i_vlan_enc='dot1q termination vid '+data['i_vlan_enc'],
                                    ospf_area='area '+data['ospf_area'],
                                    ospf_network='network '+data['ospf_network'],
                                    dhcp_int='int '+data['dhcp_int'],
                                    dhcp_ipadd ='ip add '+data['dhcp_ipadd'],
                                    dhcp_server_dnslist ='dhcp server dns-list '+data['dhcp_server_dnslist'],
                                    dhcp_server_excluded='dhcp server excluded-ip-address '+data['dhcp_server_excluded'],
                                    port_id=select)
                    coba.save()
                    idd = select.id
                    devices.objects.filter(id=idd).update(preconf=data['name'] ,new_device_mac=data['mac'] ,stats='Booked')
                    messages.success(request, f'Successfully create PreConfiguration!')
                    return redirect('/')
            else:
                form_ce = ce_router_form()
                messages.warning(request, f'tidak valid')

            context = {
                'form_ce': form_ce
            }
            return render(request, 'ansibleweb/huawei/ce_router_preconfig.html', context)
        else:
            if request.method == 'POST':
                form_ce = ce_router_form(request.POST)
                if form_ce.is_valid():
                    data = request.POST
                    print(request.POST)
                    iosrouter.objects.filter(port_id=select).update(name=data['name'],
                                                                    hostname='sysname'+data['name'],
                                                                    port_ip='int '+data['port_ip'],
                                                                    ip_add='ip add '+data['ip_add'],
                                                                    i_vlan_int='int '+data['i_vlan_int'],
                                                                    i_vlan_ip='ip address '+data['i_vlan_ip'],
                                                                    i_vlan_enc='dot1q termination vid '+data['i_vlan_enc'],
                                                                    ospf_area='area '+data['ospf_area'],
                                                                    ospf_network='network '+data['ospf_network'],
                                                                    dhcp_int='int '+data['dhcp_int'],
                                                                    dhcp_ipadd ='ip add '+data['dhcp_ipadd'],
                                                                    dhcp_server_dnslist ='dhcp server dns-list '+data['dhcp_server_dnslist'],
                                                                    dhcp_server_excluded='dhcp server excluded-ip-address '+data['dhcp_server_excluded'])
                    update = select.id
                    devices.objects.filter(id=update).update(preconf=data['name'], new_device_mac=data['mac'])
                    messages.success(request, f'Successfully update PreConfiguration!')
                    return redirect('/')
            else:
                form_ce = ce_router_form()
            
            context = {
                'form_ce': form_ce
            }
            return render(request, 'ansibleweb/huawei/ce_router_preconfig.html', context)
    else:
        return redirect('/')
    

#        form = autoios(request.POST, instance=device)

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
                if os == 'ce':
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
                elif os == 'ios':
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
        form = autoconfig(request.GET)
        if form.is_valid():
            data=request.GET
            print(request.GET)
            host = AnsibleNetworkHost.objects.get(id=data['hosts'])
            os = host.group.ansible_network_os
            jumlah = arp.objects.all().filter(device_id=host)
            cannot = len(jumlah)
            if os == 'ios':
                arp.objects.filter(device_id=data['hosts']).delete()
                my_play = dict(
                    name="show arp",
                    hosts=host.host,
                    become='yes',
                    become_method='enable',
                    gather_facts='no',
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
                    bookeds = devices.objects.filter(device_id=data['hosts'], stats='Booked').values_list('new_device_mac')
                    arps = arp.objects.filter(device_id=data['hosts']).values_list('mac')
                    match = arps.intersection(bookeds)
                    jumlah = len(match)
                    for z in range(0, jumlah):
                        findmac = match[z][0]
                        os_type = devices.objects.filter(new_device_mac=findmac).values_list('new_device_os')
                        t_os = os_type[0][0]
                        de_type = devices.objects.filter(new_device_mac=findmac).values_list('new_device_type')
                        dtype = de_type[0][0]
                        add_ip = arp.objects.filter(mac=findmac).values_list('ipadd')
                        precon = devices.objects.filter(new_device_mac=findmac).values_list('preconf')
                        cons = precon[0][0]
                        if t_os == 'ios' and dtype == 'router':
                            host = AnsibleNetworkHost(host=cons,
                                                ansible_ssh_host=add_ip,
                                                ansible_user='indra',
                                                ansible_ssh_pass='cisco',
                                                ansible_become_pass='cisco',
                                                group=host.group)
                            host.save()
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
                            result = execute(my_play) ###siniiiiiii
                            kondisi = result.stats
                            kond = kondisi['hosts'][0]['status']
                            if kond == 'ok':
                                devices.objects.filter(new_device_mac=findmac).update(stats='configured')
                                messages.success(request, f'Berhasil Melakukan AutoKonfigurasi !!')
                                info = arp.objects.all().filter(device_id=host)
                                context = {
                                    'form': form,
                                    'info': info
                                }
                                return render(request, 'ansibleweb/autoconfig.html',context)
                            else:
                                messages.warning(request, f'Cek Koneksi Perangkat!!')
                                return redirect('arp')
                        elif t_os == 'ios' and dtype == 'switch':
                            host = AnsibleNetworkHost(host=cons,
                                                ansible_ssh_host=add_ip,
                                                ansible_user='indra',
                                                ansible_ssh_pass='cisco',
                                                ansible_become_pass='cisco',
                                                group=host.group)
                            host.save()
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
                                        dict(action=dict(module='ios_vlan', vlan_id=conf.vlan_id, name=conf.vlan_name))
                                    ]
                                )
                            result = execute(my_play) ###siniiiiiii
                            kondisi = result.stats
                            kond = kondisi['hosts'][0]['status']
                            if kond == 'ok':
                                devices.objects.filter(new_device_mac=findmac).update(stats='configured')
                                messages.success(request, f'Berhasil Melakukan AutoKonfigurasi !!')
                                info = arp.objects.all().filter(device_id=host)
                                context = {
                                    'form': form,
                                    'info': info
                                }
                                return render(request, 'ansibleweb/autoconfig.html',context)
                            else:
                                messages.warning(request, f'Cek Koneksi Perangkat!!')
                                return redirect('arp')
                        elif t_os == 'ce' and dtype == 'router':
                            host = AnsibleNetworkHost(host=cons,
                                                ansible_ssh_host=add_ip,
                                                ansible_user='admin',
                                                ansible_ssh_pass='54541691',
                                                ansible_become_pass='54541691',
                                                group=host.group)
                            host.save()
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
                                messages.success(request, f'Berhasil Melakukan AutoKonfigurasi !!')
                                info = arp.objects.all().filter(device_id=host)
                                context = {
                                    'form': form,
                                    'info': info
                                }
                                return render(request, 'ansibleweb/autoconfig.html',context)
                            else:
                                messages.warning(request, f'Cek Koneksi Perangkat!!')
                                return redirect('arp')
                else:
                    messages.warning(request, f'Cek Koneksi Perangkat!!')
                    return redirect('arp')
            elif os == 'ce':
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
                    bookeds = devices.objects.filter(device_id=data['hosts'], stats='Booked').values_list('new_device_mac')
                    arps = arp.objects.filter(device_id=data['hosts']).values_list('mac')
                    match = arps.intersection(bookeds)
                    print(bookeds)
                    print(arps)
                    print(match)
                    jumlah = len(match)
                    for z in range(0, jumlah):
                        findmac = match[z][0]
                        print(findmac)
                        #cekkamus = kamusport.objects.get(portarp=findmac)
                        #port_out = cekkamus.portint
                        os_type = devices.objects.filter(new_device_mac=findmac).values_list('new_device_os')
                        t_os = os_type[0][0]
                        de_type = devices.objects.filter(new_device_mac=findmac).values_list('new_device_type')
                        dtype = de_type[0][0]
                        add_ip = arp.objects.filter(mac=findmac).values_list('ipadd')
                        precon = devices.objects.filter(new_device_mac=findmac).values_list('preconf')
                        cons = precon[0][0]
                        print(cons)
                        print(t_os)
                        if t_os == 'ios' and dtype == 'router':
                            host = AnsibleNetworkHost(host=cons,
                                                ansible_ssh_host=add_ip,
                                                ansible_user='indra',
                                                ansible_ssh_pass='cisco',
                                                ansible_become_pass='cisco',
                                                group=host.group)
                            host.save()
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
                                messages.success(request, f'Berhasil Melakukan AutoKonfigurasi !!')
                                info = arp.objects.all().filter(device_id=host)
                                context = {
                                    'form': form,
                                    'info': info
                                }
                                return render(request, 'ansibleweb/autoconfig.html',context)
                            else:
                                messages.warning(request, f'Cek Koneksi Perangkat!!')
                                return redirect('arp')
                        elif t_os == 'ce' and dtype == 'router':
                            host = AnsibleNetworkHost(host=cons,
                                                ansible_ssh_host=add_ip,
                                                ansible_user='admin',
                                                ansible_ssh_pass='54541691',
                                                ansible_become_pass='54541691',
                                                group=host.group)
                            host.save()
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
                                messages.success(request, f'Berhasil Melakukan AutoKonfigurasi !!')
                                info = arp.objects.all().filter(device_id=host)
                                context = {
                                    'form': form,
                                    'info': info
                                }
                                return render(request, 'ansibleweb/autoconfig.html',context)
                            else:
                                messages.warning(request, f'Cek Koneksi Perangkat!!1')
                                return redirect('arp')
                        else:
                            messages.warning(request, f'tidak ada os')
                            return redirect('arp')                            
                else:
                    messages.warning(request, f'Cek Koneksi Perangkat!!2')
                    return redirect('arp')
    else:
        form = autoconfig()
        messages.warning(request, f'eror!4')
            
    context = {
        'form': form
    }
    return render(request, 'ansibleweb/autoconfig.html', context)





def about(request):
    return render(request, 'ansibleweb/about.html', {'title': 'About'})

def addportdevice(request):
    if request.method == 'GET' and 'btnform1' in request.GET:
        infos = addinfodevice(request.GET)
        if infos.is_valid():
            data = request.GET
            print(request.GET)
            info = devices.objects.all().filter(device_id=data['hosts'])
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
            elif cannot == 0 and os =='ios':
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
                elif os == 'ios':
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
    else:
        infos = addinfodevice()
    
    context = {
        'infos': infos
    }
    return render(request, 'ansibleweb/addinfodevice.html',context)

def addgroup(request):
    if request.method == 'POST':
        adddgroup = group(request.POST)
        if adddgroup.is_valid():
            print(request.POST)
            data = request.POST
            my_group = AnsibleNetworkGroup(name=data['name'],
                               ansible_connection='network_cli',
                               ansible_network_os=data['os'],
                               ansible_become=True)
            my_group.save()
            messages.success(request, f'Berhasil membuat group host network')
            return redirect('group-create')
    else:
        adddgroup = group()
        return render(request, 'ansibleweb/post_group.html', {'form': adddgroup })

def addhost(request):
    if request.method == 'POST':
        adddhost = PostInventoryHost(request.POST)
        if adddhost.is_valid():
            adddhost.save()
            messages.success(request, f'Berhasil membuat inventory host network')
            return redirect('Ansible-home')
        else:
            return render(request, 'ansibleweb/post_host.html', {'form':adddhost})
    else:
        adddhost = PostInventoryHost()
        return render(request, 'ansibleweb/post_host.html', {'form':adddhost})

def addPlaybook(request):
    if request.method == 'POST':
        p_form = PostPlayBookForm(request.POST)
        t_form = TaskForm(request.POST)
        if p_form.is_valid() and t_form.is_valid():
            tasks = t_form.save()
            playbook = p_form.save(commit=False)
            playbook.task = tasks
            playbook.save()
            messages.success(request, f'Your playbook has been created!')
            print(request.POST)
            data = request.POST
            my_play = dict(
                name=data['name'],
                hosts=data['hosts'],
                become=data['become'],
                become_method=data['become_method'],
                gather_facts=data['gather_facts'],
                tasks=[
                    dict(action=dict(module=data['module'], commands=data['commands']))
                    ]
                ) 
            result = execute(my_play)
            #print(json.dumps(result.results, indent=4))
            output = json.dumps(result.results, indent=4)
            context = {
                'p_form': p_form,
                't_form': t_form,
                'output': output
            }
            return render(request, 'ansibleweb/post_playbook.html', context)
            #return redirect('Ansible-home')
    else:
        p_form = PostPlayBookForm()
        t_form = TaskForm()
    
    context = {
        'p_form': p_form,
        't_form': t_form
    }
    
    return render(request, 'ansibleweb/post_playbook.html', context)

def addTask(request):
    if request.method == 'POST':
        p_form = PostPlayBookForm(request.POST)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'Task hasbeen created!')
            return redirect('Ansible-home')
    else:
        p_form = PostPlayBookForm()

    context = {
        'p_form': p_form
    }

    return render(request, 'ansibleweb/post_playbook.html',context)

def namecisco(request):
    if request.method == 'POST':
        host_form = hostnamecisco(request.POST)
        if host_form.is_valid():
            host_form.save()
            messages.success(request, f'Configure Hostname Success')
            print(request.POST)
            data = request.POST
            #host = form.cleaned_data.get['hosts']
            #name = form.cleaned_data.get['hostname']
            my_play = dict(
                name="hostname",
                hosts=data['hosts'],
                become='yes',
                become_method='enable',
                gather_facts='no',
                tasks=[
                    dict(action=dict(module='ios_config', lines=data['name']))
                    ]
                )
            result = execute(my_play)
            #print(json.dumps(result.results, indent=4))
            output = json.dumps(result.results, indent=4)
            context = {
                'host_form': host_form,
                'output': output
            }
            return render(request, 'ansibleweb/ciscohostname.html', context)
    else:
        host_form = hostnamecisco()
    
    context = {
        'host_form': host_form
    }
    return render(request, 'ansibleweb/ciscohostname.html', context)

def vlancisco(request):
    if request.method == 'POST':
        vlan = vlan_cisco(request.POST)
        if vlan.is_valid():
            #host = form.cleaned_data.get('hosts')
			#id = form.cleaned_data.get('vlan_id')
            #name = form.cleaned_data.get('vlan_name')
            print(request.POST)
            data = request.POST
            #host = form.cleaned_data['hosts']
            #name = form.cleaned_data['hostname']
            my_play = dict(
                name="hostname",
                hosts=data['hosts'],
                become='yes',
                become_method='enable',
                gather_facts='no',
                tasks=[
                    dict(action=dict(module='ios_vlan', vlan_id=data['vlan_id'], name=data['vlan_name']))
                    ]
                )
            result = execute(my_play)
            #print(json.dumps(result.results, indent=4))
            output = json.dumps(result.results, indent=4)
            context = {
                'vlan': vlan,
                'output': output
            }
            return render(request, 'ansibleweb/ciscovlan.html', context)
    else:
        vlan = vlan_cisco()
    
    context = {
        'vlan': vlan
    }
    return render(request, 'ansibleweb/ciscovlan.html', context)

def ospfcisco(request):
    if request.method == 'POST':
        ospf = ospf_cisco(request.POST)
        if ospf.is_valid():
            print(request.POST)
            data = request.POST
            my_play = dict(
                name="hostname",
                hosts=data['hosts'],
                become='yes',
                become_method='enable',
                gather_facts='no',
                tasks=[
                    dict(action=dict(module='ios_config', lines=data['lines'], parents=data['parents']))
                    ]
                )
            result = execute(my_play)
            #print(json.dumps(result.results, indent=4))
            output = json.dumps(result.results, indent=4)
            context = {
                'ospf': ospf,
                'output': output
            }
            return render(request, 'ansibleweb/ciscoospf.html', context)
    else:
        ospf = ospf_cisco()
    
    context = {
        'ospf': ospf
    }
    return render(request, 'ansibleweb/ciscoospf.html', context)

def play():
    plays = PlayBooks.objects.all().prefetch_related('task')
    
    my_play = [{
        'name':play.name,
        'hosts':play.hosts, 
        'become':play.become, 
        'become_method':play.become_method, 
        'gather_facts':play.gather_facts, 
        'tasks':[{'module':actions.module, 'commands':actions.commands} for actions in play.task.all()]} for play in plays]

def log(request):
    logs = log.objects.all()

    context = {
        'logs': logs
    }
    return render(request, 'ansibleweb/home.html', context)

# INI BENAR BACKUP

def backupcisco(request):
    if request.method == 'POST':
        backup = ciscobackup(request.POST)
        if backup.is_valid():
            print(request.POST)
            data = request.POST
            my_play = dict(
                name="nyihuy",
                hosts=data['hosts'],
                become='yes',
                become_method='enable',
                gather_facts='no',
                tasks=[
                    dict(action=dict(module='ios_config', backup='yes'), register='output'),
                    dict(action=dict(module='copy', src="{{output.backup_path}}", dest="/home/indra/autonet/AutoAnsible/backup/{{inventory_hostname}}.config")),
                    dict(action=dict(module='lineinfile', path="/home/indra/autonet/AutoAnsible/backup/{{inventory_hostname}}.config", line="Building configuration...", state='absent')),
                    dict(action=dict(module='lineinfile', path="/home/indra/autonet/AutoAnsible/backup/{{inventory_hostname}}.config", regexp="Current configuration.*", state='absent'))
                    ]
                )
            result = execute(my_play)
            #print(json.dumps(result.results, indent=4))
            output = json.dumps(result.results, indent=4)
            context = {
                'backup': backup,
                'output': output
            }
            return render(request, 'ansibleweb/ciscobackup.html', context)
    else:
        backup = ciscobackup()
    
    context = {
        'backup': backup
    }
    return render(request, 'ansibleweb/ciscobackup.html', context)

def restorecisco(request):
    if request.method == 'POST':
        restore = ciscorestore(request.POST)
        if restore.is_valid():
            print(request.POST)
            data = request.POST
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
    else:
        restore = ciscorestore()
    
    context = {
        'restore': restore
    }
    return render(request, 'ansibleweb/ciscorestore.html', context)


# Perangkat Huawei

def namehuawei(request):
    if request.method=="POST":
        hostname = hostnamehuawei(request.POST)
        if hostname.is_valid():
            print(request.POST)
            data = request.POST
            my_play = dict(
                name="conf name",
                hosts=data['hosts'],
                become='yes',
                become_method='enable',
                gather_facts='no',
                tasks=[
                    dict(action=dict(module='ce_config', lines=data['hostname']))
                ]
            )
            result = execute(my_play)
            data = result.stats
            results = result.results
            device = data['hosts'][0]['host']
            status = data['hosts'][0]['status']
            #failed = results['failed'][0]['tasks'][0]['result']['msg']
            #success = results['success'][0]['tasks'][0]['result']['stdout_lines'][0]

            output = "Host :"+device+"    Config:"+status
                
            context = {
                'hostname': hostname,
                'output': output
            }
            return render(request, 'ansibleweb/huawei/huaweihostname.html', context)
    else:
        hostname = hostnamehuawei()

    context = {
        'hostname': hostname
    }
    return render(request, 'ansibleweb/huawei/huaweihostname.html', context)

def ospfhuawei(request):
    if request.method=='POST':
        ospf = ospf_huawei(request.POST)
        if ospf.is_valid():
            print(request.POST)
            data = request.POST
            my_play = dict(
                name="Configure OSPF",
                hosts=data['hosts'],
                become='yes',
                become_method='enable',
                gather_facts='no',
                tasks=[
                    dict(action=dict(module='ce_config', lines=['ospf', data['area'], data['network']]))
                ]
            )
            result = execute(my_play)
            output = json.dumps(result.results, indent=4)
            context = {
                'ospf': ospf,
                'output': output
            }
            return render(request, 'ansibleweb/huawei/huaweiospf.html', context)
    else:
        ospf = ospf_huawei()
    
    context = {
        'ospf': ospf
    }
    return render(request, 'ansibleweb/huawei/huaweiospf.html', context)

def ivlan_huawei(request):
    if request.method=='POST':
        ivlan = intervlan_huawei(request.POST)
        if ivlan.is_valid():
            print(request.POST)
            data = request.POST
            my_play = dict(
                name="Configure Inter VLAN",
                hosts=data['hosts'],
                become='yes',
                become_method='enable',
                gather_facts='no',
                tasks=[
                    dict(action=dict(module='ce_config', lines=[data['interface'], data['ipadd'], data['cmd']]))
                ]
            )
        result = execute(my_play)
        output = json.dumps(result.results, indent=4)
        context = {
            'ivlan': ivlan,
            'output': output
        }
        return render(request, 'ansibleweb/huawei/ivlan_huawei.html', context)
    else:
        ivlan = intervlan_huawei()

    context = {
        'ivlan': ivlan
    }
    return render(request, 'ansibleweb/huawei/ivlan_huawei.html', context)

def backuphuawei(request):
    if request.method=='POST':
        backup = huaweibackup(request.POST)
        if backup.is_valid():
            print(request.POST)
            data = request.POST
            my_play = dict(
                name="Backup Configuration Huawei",
                hosts=data['hosts'],
                become='yes',
                become_method='enable',
                gather_facts='no',
                tasks=[
                    dict(action=dict(module='ce_config', lines=['sysname {{ inventory_hostname }}'], backup='yes'), register='output'),
                    dict(action=dict(module='copy', src="{{output.backup_path}}", dest="./backup/{{inventory_hostname}}.cfg"))
                ]
            )
        result = execute(my_play)
        output = json.dumps(result.results, indent=4)
        context = {
            'backup': backup,
            'output': output
        }
        return render(request, 'ansibleweb/huawei/huaweibackup.html', context)
    else:
        backup = huaweibackup()

    context = {
        'backup': backup
    }
    return render(request, 'ansibleweb/huawei/huaweibackup.html', context)

def restorehuawei(request):
    if request.method=='POST':
        restore = huaweirestore(request.POST)
        if restore.is_valid():
            print(request.POST)
            data = request.POST
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
        return render(request, 'ansibleweb/huawei/restorehuawei.html',context)
    else:
        restore = huaweirestore()
        
    context= {
        'restore': restore
    }
    return render(request, 'ansibleweb/huawei/restorehuawei.html',context)

#MIKROTIK CONFIG --------------

def namemikrotik(request):
    if request.method=='POST':
        name = hostnamemikrotik(request.POST)
        if name.is_valid():
            print(request.POST)
            data = request.POST
            my_play = dict(
                name="hostname",
                hosts=data['hosts'],
                become='yes',
                become_method='enable',
                gather_facts='no',
                vars=[
                    dict(ansible_command_timeout=120)
                ],
                tasks=[
                    dict(action=dict(module='routeros_command', commands='/system identity set name='+data['hostname']))
                ]
            )
        result = execute(my_play)
        output = json.dumps(result.results, indent=4)
        context = {
            'name': name,
            'output': output
        }
        return render(request, 'ansibleweb/mikrotik/namemikrotik.html', context)
    else:
        name = hostnamemikrotik()
        
    context = {
        'name': name
    }
    return render(request, 'ansibleweb/mikrotik/namemikrotik.html', context)
    
def ipaddmtk(request):
    if request.method=='POST':
        ipadd = ipaddmikrotik(request.POST)
        if ipadd.is_valid():
            print(request.POST)
            data = request.POST
            my_play = dict(
                name="Ip address",
                hosts=data['hosts'],
                become='yes',
                become_method='enable',
                gather_facts='no',
                vars=[
                    dict(ansible_command_timeout=120)
                ],
                tasks=[
                    dict(action=dict(module='routeros_command', commands='/ip address add address='+data['ipadd']+' interface='+data['interface']))
                ]
            )
        result = execute(my_play)
        output = json.dumps(result.results, indent=4)
        context = {
            'ipadd': ipadd,
            'output': output
        }
        return render(request, 'ansibleweb/mikrotik/ipaddmikrotik.html', context)
    else:
        ipadd = ipaddmikrotik()
        
    context = {
        'ipadd': ipadd
    }
    return render(request, 'ansibleweb/mikrotik/ipaddmikrotik.html', context)

def ospfmikrotik(request):
    if request.method=='POST':
        ospf = ospf_mikrotik(request.POST)
        if ospf.is_valid():
            print(request.POST)
            data =request.POST
            my_play = dict(
                name="OSPF",
                hosts=data['hosts'],
                become='yes',
                become_method='enable',
                gather_facts='no',
                vars=[
                    dict(ansible_command_timeout=120)
                ],
                tasks=[
                    dict(action=dict(module='routeros_command', commands='/routing ospf network add network='+data['network']+' area='+data['area']))
                ]
            )
        result = execute(my_play)
        output = json.dumps(result.results, indent=4)
        context = {
            'ospf': ospf,
            'output': output
        }
        return render(request, 'ansibleweb/mikrotik/ospfmikrotik.html', context)
    else:
        ospf = ospf_mikrotik()
        
    context = {
        'ospf': ospf
    }
    return render(request, 'ansibleweb/mikrotik/ospfmikrotik.html', context)
    
def backupmikrotik(request):
    if request.method=='POST':
        backup = mikrotikbackup(request.POST)
        if backup.is_valid():
            print(request.POST)
            data = request.POST
            my_play= dict(
                name="Backup Mikrotik",
                hosts=data['hosts'],
                become='yes',
                become_method='enable',
                gather_facts='no',
                vars=[
                    dict(ansible_command_timeout=120)
                ],
                tasks=[
                    dict(file=dict(path='./backup/{{inventory_hostname}}.backup', state='absent'))
                ]
            )            
            my_play2= dict(
                name="Backup Mikrotik",
                hosts=data['hosts'],
                become='yes',
                become_method='enable',
                gather_facts='no',
                vars=[
                    dict(ansible_command_timeout=120)
                ],
                tasks=[
                    dict(action=dict(module='routeros_command', commands='/system backup save name={{ inventory_hostname }} password={{ ansible_password }}')),
                    dict(net_get=dict(src="./{{ inventory_hostname }}.backup", protocol='scp', dest='./backup/{{ inventory_hostname}}.backup'))
                ]
            )
        result = execute(my_play)
        result2 = execute(my_play2)
        output = json.dumps(result2.results, indent=4)
        context = {
            'backup': backup,
            'output': output
        }
        return render(request, 'ansibleweb/mikrotik/backupmikrotik.html', context)
    else:
        backup = mikrotikbackup()
        
    context = {
        'backup': backup
    }
    return render(request, 'ansibleweb/mikrotik/backupmikrotik.html', context)

def restoremikrotik(request):
    if request.method=='POST':
        restore = mikrotikrestore(request.POST)
        if restore.is_valid():
            print(request.POST)
            data = request.POST
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
        return render(request, 'ansibleweb/mikrotik/restoremikrotik.html', context)
    else:
        restore = mikrotikrestore()
    
    context = {
        'restore': restore
    }
    return render(request, 'ansibleweb/mikrotik/restoremikrotik.html', context)

from __future__ import absolute_import, unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .models import mac_os, PostInventoryGroup, PostInventoryHost ,PostPlayBookForm, TaskForm, log, group, addinfodevice , ios_router, preconfdevice, arp, ce_router_form, ce_router, kamusport, ios_switch, ios_switch_form, devices, iosrouter, ce_switch, ce_switch_form, routeros_router, routeros_router_form
from .forms import ivlanset, hostnamecisco, dhcpset, ospfset, ip_staticset, vlanint, vlan_cisco, ospf_cisco, ciscobackup, ciscorestore, hostnamehuawei, ospf_huawei, intervlan_huawei, backupall, hostnamemikrotik, ipaddmikrotik, ospf_mikrotik, mikrotikbackup, huaweirestore, mikrotikrestore, autoconfig , vlanset, host_all
from django.contrib import messages
from django.db.models.fields.related import ManyToManyField
#from djansible.models import PlayBooks
from itertools import chain
from dj_ansible.models import AnsibleNetworkHost, AnsibleNetworkGroup
from dj_ansible.ansible_kit import execute
import json
from datetime import datetime
import time
from asgiref.sync import sync_to_async
import threading
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
    failure = log.objects.all().filter(status='Failed')
    successful = log.objects.all().filter(status='Success')
    logs = log.objects.all().order_by('-time')
    coba = request.GET.get('page', 1)

    paginator = Paginator(logs, 10)
    try:
        pages = paginator.page(coba)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    context = {
        'all_device': len(all_device),
        'failure': len(failure),
        'successful': len(successful),
        'pages': pages
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
    print(state)
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
                                    dhcp_pool='ip dhcp pool '+data['dhcp_pool'],
                                    port_id=select)
                    coba.save()
                    idd = select.id
                    devices.objects.filter(id=idd).update(preconf=data['name'] ,new_device_mac=data['mac'] ,stats='Booked')
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
                Print('TIDAK EMPTY')
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
                                                                    dhcp_pool='ip dhcp pool '+data['dhcp_pool'])
                    idd = select.id
                    devices.objects.filter(id=idd).update(preconf=data['name'], new_device_mac=data['mac'], stats='Booked')
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
        else:
            if request.method == 'POST':
                form_ios = ios_switch_form(request.POST)
                if form_ios.is_valid():
                    data = request.POST
                    print(request.POST)
                    ios_switch.objects.filter(port_id=select).update(name=data['name'],
                                    hostname='sysname '+data['name'],
                                    vlan_id=data['vlan_id'],
                                    vlan_name=data['vlan_name'])
                    idd = select.id
                    devices.objects.filter(id=idd).update(preconf=data['name'], new_device_mac=data['mac'] ,stats='Booked')
                    messages.success(request, f'Successfully update PreConfiguration!')
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
                    coba = ce_router(name=data['name'],
                                    hostname='sysname '+data['name'],
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
            print('TIDAK VALID')
            if request.method == 'POST':
                form_ce = ce_router_form(request.POST)
                if form_ce.is_valid():
                    data = request.POST
                    print(request.POST)
                    ce_router.objects.filter(port_id=select).update(name=data['name'],
                                                                    hostname='sysname '+data['name'],
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
                    devices.objects.filter(id=update).update(preconf=data['name'], new_device_mac=data['mac'], stats='Booked')
                    messages.success(request, f'Successfully update PreConfiguration!')
                    return redirect('/')
            else:
                form_ce = ce_router_form()
            
            context = {
                'form_ce': form_ce
            }
            return render(request, 'ansibleweb/huawei/ce_router_preconfig.html', context)
    elif cek == 'ce' and tipe == 'switch':
        if state == 'empty':
            if request.method == 'POST':
                form_ce = ce_switch_form(request.POST)
                if form_ce.is_valid():
                    data = request.POST
                    print(request.POST)
                    coba = ce_switch(name=data['name'],
                                    hostname='sysname '+data['name'],
                                    vlan = 'vlan batch '+data['vlan'],
                                    port_ip='int '+data['port_ip'],
                                    port_vlan='port default vlan '+data['port_vlan'],
                                    port_cmd1='port link-type '+data['port_cmd1'],
                                    port_id=select)
                    coba.save()
                    idd = select.id
                    devices.objects.filter(id=idd).update(preconf=data['name'] ,new_device_mac=data['mac'] ,stats='Booked')
                    messages.success(request, f'Successfully create PreConfiguration!')
                    return redirect('/')
            else:
                form_ce = ce_switch_form()
                messages.warning(request, f'tidak valid')

            context = {
                'form_ce': form_ce
            }
            return render(request, 'ansibleweb/huawei/ce_switch_preconfig.html', context)
        else:
            if request.method == 'POST':
                form_ce = ce_switch_form(request.POST)
                if form_ce.is_valid():
                    data = request.POST
                    print(request.POST)
                    ce_switch.objects.filter(port_id=select).update(name=data['name'],
                                                                    hostname='sysname '+data['name'],
                                                                    vlan = 'vlan batch '+data['vlan'],
                                                                    port_ip='int '+data['port_ip'],
                                                                    port_vlan='port default vlan '+data['port_vlan'],
                                                                    port_cmd1='port link-type '+data['port_cmd1'])
                    update = select.id
                    devices.objects.filter(id=update).update(preconf=data['name'], new_device_mac=data['mac'], stats='Booked')
                    messages.success(request, f'Successfully update PreConfiguration!')
                    return redirect('/')
            else:
                form_ce = ce_switch_form()
            
            context = {
                'form_ce': form_ce
            }
            return render(request, 'ansibleweb/huawei/ce_switch_preconfig.html', context)
    elif cek == 'routeros' and tipe == 'router':
        if state == 'empty':
            if request.method == 'POST':
                form_routeros = routeros_router_form(request.POST)
                if form_routeros.is_valid():
                    data = request.POST
                    print(request.POST)
                    coba = routeros_router(name=data['name'],
                                        hostname='/system identity set name='+data['name'],
                                        port_cmd='/ip address add address='+data['port_cmd']+' interface='+data['port_ip'],
                                        opsf='/routing ospf network add network='+data['ospf_network']+' area='+data['ospf_area'],
                                        inter_vlan='/interface vlan add name='+data['vlan_name']+' vlan-id='+data['vlan_id']+' interface='+data['vlan_int'],
                                        ip_add_vlan='/ip address add address='+data['ip_add_vlan']+' interface='+data['interface_vlan'],
                                        port_id=select)
                    coba.save()
                    idd = select.id
                    devices.objects.filter(id=idd).update(preconf=data['name'] ,new_device_mac=data['mac'] ,stats='Booked')
                    messages.success(request, f'Successfully create PreConfiguration!')
                    return redirect('/')
            else:
                form_routeros = routeros_router_form()
            context= {
                'form_routeros': form_routeros
            }
            return render(request, 'ansibleweb/mikrotik/routeros_router_form.html', context)
        else:
            if request.method == 'POST':
                form_routeros = routeros_router_form(request.POST)
                if form_routeros.is_valid():
                    data = request.POST
                    print(request.POST)
                    routeros_router.objects.filter(port_id=select).update(name=data['name'],
                                        hostname='/system identity set name='+data['name'],
                                        port_cmd='/ip address add address='+data['port_cmd']+' interface='+data['port_ip'],
                                        opsf='/routing ospf network add network='+data['ospf_network']+' area='+data['ospf_area'],
                                        inter_vlan='/interface vlan add name='+data['vlan_name']+' vlan-id='+data['vlan_id']+' interface='+data['vlan_int'],
                                        ip_add_vlan='/ip address add address='+data['ip_add_vlan']+' interface='+data['interface_vlan'])
                    update = select.id
                    devices.objects.filter(id=update).update(preconf=data['name'], new_device_mac=data['mac'] ,stats='Booked')
                    messages.success(request, f'Successfully update PreConfiguration!')
                    return redirect('/')
            else:
                form_routeros = routeros_router_form()
            context={
                'form_routeros': form_routeros
            }
            return render(request, 'ansibleweb/mikrotik/routeros_router_form.html', context)
    else:
        messages.warning(request, f'Belum menambahkan Tipe Device Baru')
        return redirect('/')
    

#        form = autoios(request.POST, instance=device)

def about(request):
    return render(request, 'ansibleweb/about.html', {'title': 'About'})


def addgroup(request):
    if request.method == 'POST':
        adddgroup = group(request.POST, instance=request.user)
        if adddgroup.is_valid():
            print(request.POST)
            data = request.POST
            akun = request.user
            my_group = AnsibleNetworkGroup(name=data['name'],
                               ansible_connection='network_cli',
                               ansible_network_os=data['os'],
                               ansible_become=True)
            my_group.save()
            logs = log(account=akun, targetss="Group Device", action="Add Group", status="Success",time=datetime.now(), messages="No Error")
            logs.save()
            messages.success(request, f'Berhasil membuat group host network')
            return redirect('group-create')
    else:
        adddgroup = group()
        return render(request, 'ansibleweb/post_group.html', {'form': adddgroup })


def log_info(request):
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

def backuphuawei(request):
    if request.method=='POST':
        backup = backupall(request.POST)
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
        backup = backupall()

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









        







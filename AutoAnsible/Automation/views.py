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

@login_required
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

@login_required
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

@login_required
def infodevice(request, pk):
    perangkat = AnsibleNetworkHost.objects.get(id=pk)
    namehost = perangkat.host
    info = devices.objects.all().filter(device_id=perangkat)

    context = {
        'perangkat': perangkat,
        'namehost': namehost,
        'info': info
    }
    return render(request, 'ansibleweb/infodevice.html', context)

@login_required
def deletegroup(request, id):
    group = AnsibleNetworkGroup.objects.get(pk=id)
    group.delete()
    return redirect('device')

@login_required
def deletedevice(request, id):
    device = AnsibleNetworkHost.objects.get(pk=id)
    deleted = device.host
    akun = request.user
    device.delete()
    logs = log(account=akun, targetss=deleted, action="Delete Device", status="Success",time=datetime.now(), messages="No Error")
    logs.save()
    return redirect('device')

@login_required
def prenewdevice(request, pk):
    select = devices.objects.get(id=pk)
    if request.method == 'POST':
        form_device = preconfdevice(request.POST)
        if form_device.is_valid():
            print(request.POST)
            data = request.POST
            fil = select.id
            devices.objects.filter(id=fil).update(new_device_type=data['tipe'])
            messages.success(request, f'Successfully create PreDevice!')
            return redirect('device')
    else:
        form_device = preconfdevice()

    context= {
        'form_device': form_device
    }
    return render(request, 'ansibleweb/prenewdevice.html', context)

@login_required
def prekonfig(request, pk):
    select = devices.objects.get(id=pk)
    tipe = select.new_device_type
    state = select.preconf
    print(state)
    if tipe == 'router':
        if state == 'empty':
            if request.method == 'POST':
                form_ios = ios_router(request.POST)
                if form_ios.is_valid():
                    data = request.POST
                    print(request.POST)
                    coba = iosrouter(name=data['name'],
                                    hostname=data['name'],

                                    port_ip=data['port_ip'],
                                    port_cmd=data['port_cmd'],
                                    port_mask=data['port_mask'],

                                    i_vlan_int=data['i_vlan_int'],
                                    i_vlan_enc=data['i_vlan_enc'],
                                    i_vlan_cmd=data['i_vlan_cmd'],
                                    i_vlan_mask=data['i_vlan_mask'],

                                    i_vlan_int2=data['i_vlan_int2'],
                                    i_vlan_enc2=data['i_vlan_enc2'],
                                    i_vlan_cmd2=data['i_vlan_cmd2'],
                                    i_vlan_mask2=data['i_vlan_mask2'],

                                    ospf_area=data['ospf_area'],
                                    ospf_network=data['ospf_network'],
                                    ospf_mask=data['ospf_mask'],

                                    ospf_area2=data['ospf_area2'],
                                    ospf_network2=data['ospf_network2'],
                                    ospf_mask2=data['ospf_mask2'],

                                    ospf_area3=data['ospf_area3'],
                                    ospf_network3=data['ospf_network3'],
                                    ospf_mask3=data['ospf_mask3'],

                                    dhcp_pool=data['dhcp_pool'],
                                    default_router =data['default_router'],
                                    dhcp_network=data['dhcp_network'],
                                    dhcp_mask=data['dhcp_mask'],
                                    dhcp_excluded=data['dhcp_excluded'],

                                    dhcp_pool2=data['dhcp_pool2'],
                                    default_router2=data['default_router2'],
                                    dhcp_network2=data['dhcp_network2'],
                                    dhcp_mask2=data['dhcp_mask2'],
                                    dhcp_excluded2=data['dhcp_excluded2'],

                                    dhcp_pool3=data['dhcp_pool3'],
                                    default_router3=data['default_router3'],
                                    dhcp_network3=data['dhcp_network3'],
                                    dhcp_mask3=data['dhcp_mask3'],
                                    dhcp_excluded3=data['dhcp_excluded3'],

                                    default_gateway=data['default_gateway'],

                                    port_id=select)
                    coba.save()
                    idd = select.id
                    devices.objects.filter(id=idd).update(preconf=data['name'] ,new_device_mac=data['mac'] ,stats='Booked')
                    messages.success(request, f'Successfully create PreConfiguration!')
                    return redirect('/')
            else:
                form_ios = ios_router()

            context = {
                'form_ios': form_ios
            }
            return render(request, 'ansibleweb/iospreconfig.html', context)
        else:
            if request.method == 'POST':
                form_ios = ios_router(request.POST)
                if form_ios.is_valid():
                    data = request.POST
                    macdata = data['mac']
                    get1 = macdata.replace("-","")
                    get2 = get1.replace(".","")
                    get3 = get2.replace(":","")
                    get4 = get3.lower()
                    print(request.POST)
                    iosrouter.objects.filter(port_id=select).update(name=data['name'],
                                                                    hostname=data['name'],
                                                                    port_ip=data['port_ip'],
                                                                    port_cmd=data['port_cmd'],
                                                                    port_mask=data['port_mask'],

                                                                    i_vlan_int=data['i_vlan_int'],
                                                                    i_vlan_enc=data['i_vlan_enc'],
                                                                    i_vlan_cmd=data['i_vlan_cmd'],
                                                                    i_vlan_mask=data['i_vlan_mask'],

                                                                    i_vlan_int2=data['i_vlan_int2'],
                                                                    i_vlan_enc2=data['i_vlan_enc2'],
                                                                    i_vlan_cmd2=data['i_vlan_cmd2'],
                                                                    i_vlan_mask2=data['i_vlan_mask2'],

                                                                    ospf_area=data['ospf_area'],
                                                                    ospf_network=data['ospf_network'],
                                                                    ospf_mask=data['ospf_mask'],

                                                                    ospf_area2=data['ospf_area2'],
                                                                    ospf_network2=data['ospf_network2'],
                                                                    ospf_mask2=data['ospf_mask2'],

                                                                    ospf_area3=data['ospf_area3'],
                                                                    ospf_network3=data['ospf_network3'],
                                                                    ospf_mask3=data['ospf_mask3'],

                                                                    dhcp_pool=data['dhcp_pool'],
                                                                    default_router =data['default_router'],
                                                                    dhcp_network=data['dhcp_network'],
                                                                    dhcp_mask=data['dhcp_mask'],
                                                                    dhcp_excluded=data['dhcp_excluded'],

                                                                    dhcp_pool2=data['dhcp_pool2'],
                                                                    default_router2=data['default_router2'],
                                                                    dhcp_network2=data['dhcp_network2'],
                                                                    dhcp_mask2=data['dhcp_mask2'],
                                                                    dhcp_excluded2=data['dhcp_excluded2'],

                                                                    dhcp_pool3=data['dhcp_pool3'],
                                                                    default_router3=data['default_router3'],
                                                                    dhcp_network3=data['dhcp_network3'],
                                                                    dhcp_mask3=data['dhcp_mask3'],
                                                                    dhcp_excluded3=data['dhcp_excluded3'],
                                                                    
                                                                    default_gateway=data['default_gateway'])

                    idd = select.id
                    devices.objects.filter(id=idd).update(preconf=data['name'], new_device_mac=get4, stats='Booked')
                    messages.success(request, f'Successfully update PreConfiguration!')
                    return redirect('/')
            else:
                form_ios = ios_router()
            
            context = {
                'form_ios': form_ios
            }
            return render(request, 'ansibleweb/iospreconfig.html', context)
    elif tipe == 'switch':
        if state == 'empty':
            if request.method == 'POST':
                form_ios = ios_switch_form(request.POST)
                if form_ios.is_valid():
                    data = request.POST
                    macdata = data['mac']
                    get1 = macdata.replace("-","")
                    get2 = get1.replace(".","")
                    get3 = get2.replace(":","")
                    get4 = get3.lower()
                    print(request.POST)
                    coba = ios_switch(name=data['name'],
                                    hostname=data['name'],

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


                                    port_id=select)
                    coba.save()
                    idd = select.id
                    devices.objects.filter(id=idd).update(preconf=data['name'] ,new_device_mac=get4 ,stats='Booked')
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
                    macdata = data['mac']
                    get1 = macdata.replace("-","")
                    get2 = get1.replace(".","")
                    get3 = get2.replace(":","")
                    get4 = get3.lower()
                    print(request.POST)
                    ios_switch.objects.filter(port_id=select).update(name=data['name'],
                                    hostname=data['name'],
                                    vlan_id=data['vlan_id'],
                                    vlan_name=data['vlan_name'],
                                    port_id=select)
                    idd = select.id
                    lihat= devices.objects.filter(id=idd).update(preconf=data['name'], new_device_mac=get4 ,stats='Booked')
                    print(lihat)
                    print(get4)
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

@login_required
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










        







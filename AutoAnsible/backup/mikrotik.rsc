# aug/15/2020 23:40:20 by RouterOS 6.28
# software id = 6UNN-EH59
#
/interface vlan
add interface=ether3 name=vlan10 vlan-id=10
/ip pool
add name=mahasiswa ranges=123.12.5.2-123.12.5.15
/ip dhcp-server
add address-pool=mahasiswa interface=ether3 name=dhcp1
add address-pool=mahasiswa interface=ether3 name=dhcp2
/tool user-manager customer
set admin access=\
    own-routers,own-users,own-profiles,own-limits,config-payment-gw
/ip address
add address=192.168.100.169/24 interface=ether1 network=192.168.100.0
add address=123.12.3.1/24 interface=ether2 network=123.12.3.0
add address=123.12.4.1/24 interface=ether2 network=123.12.4.0
add address=123.12.5.1/24 interface=ether3 network=123.12.5.0
add address=192.168.1.1/24 interface=vlan10 network=192.168.1.0
/ip dhcp-server network
add address=123.12.5.0/24 gateway=123.12.5.1
/ip route
add distance=1 gateway=192.168.100.1
add distance=1 gateway=192.168.100.1@main
add distance=1 dst-address=192.168.100.0/24 gateway=192.168.100.1
/romon port
add disabled=no
/routing ospf network
add area=backbone network=123.0.0.0/24
/system lcd
set contrast=0 enabled=no port=parallel type=24x4
/system lcd page
set time disabled=yes display-time=5s
set resources disabled=yes display-time=5s
set uptime disabled=yes display-time=5s
set packets disabled=yes display-time=5s
set bits disabled=yes display-time=5s
set version disabled=yes display-time=5s
set identity disabled=yes display-time=5s
set ether1 disabled=yes display-time=5s
set ether2 disabled=yes display-time=5s
set ether3 disabled=yes display-time=5s
set vlan10 disabled=yes display-time=5s
/tool user-manager database
set db-path=user-manager
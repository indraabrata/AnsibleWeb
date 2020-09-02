# jan/16/1970 23:30:21 by RouterOS 6.43.3
# software id = KUYK-P49N
#
# model = RB941-2nD
# serial number = A1C30962B4D9
/interface wireless
set [ find default-name=wlan1 ] disabled=no ssid=MikroTik
/interface vlan
add interface=ether2 name=vlan10 vlan-id=10
add interface=ether2 name=vlan20 vlan-id=20
/interface wireless security-profiles
set [ find default=yes ] supplicant-identity=MikroTik
/ip dhcp-server
add interface=ether2 name=dhcp4
add interface=ether2 name=dhcp5
add interface=ether2 name=dhcp6
/ip pool
add name=mahasiswa ranges=172.16.10.2-172.16.10.20
add name=dosen ranges=172.16.20.2-172.16.20.20
add name=switch ranges=172.16.50.2-172.16.50.20
add name=pegawai ranges=172.18.30.5-172.18.30.10
/ip dhcp-server
add address-pool=switch disabled=no interface=ether2 name=dhcp1
add address-pool=dosen interface=ether2 name=dhcp2
add address-pool=mahasiswa interface=ether2 name=dhcp3
add address-pool=pegawai disabled=no interface=ether3 name=dhcp7
/queue simple
add max-limit=10M/10M name="Queue Utama" target=192.168.30.1/32
/ip address
add address=172.16.50.1/24 interface=ether2 network=172.16.50.0
add address=172.16.10.1/24 interface=vlan10 network=172.16.10.0
add address=172.16.20.1/24 interface=vlan20 network=172.16.20.0
add address=123.12.2.2/24 interface=ether1 network=123.12.2.0
add address=192.168.30.1/24 interface=ether3 network=192.168.30.0
add address=172.18.10.1/24 interface=vlan10 network=172.18.10.0
/ip dhcp-server network
add address=172.16.10.0/24 gateway=172.16.10.1
add address=172.16.20.0/24 gateway=172.16.20.1
add address=172.16.50.0/24 gateway=172.16.50.1
add address=172.18.30.0/24 gateway=172.18.30.1
/ip dns
set allow-remote-requests=yes servers=8.8.8.8
/ip firewall nat
add action=masquerade chain=srcnat out-interface=ether1
/ip route
add distance=1 gateway=123.12.2.1
/routing ospf network
add area=backbone network=123.0.0.0/8
add area=backbone network=10.1.1.0/24
add area=backbone network=172.16.0.0/16
add area=backbone network=192.168.0.0/16
/system routerboard settings
set silent-boot=no
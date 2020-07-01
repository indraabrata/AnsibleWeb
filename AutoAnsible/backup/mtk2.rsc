# jun/05/2020 23:47:13 by RouterOS 6.45.9
# software id = I969-AGVF
#
#
#
/interface wireless security-profiles
set [ find default=yes ] supplicant-identity=MikroTik
/lora servers
add address=eu.mikrotik.thethings.industries down-port=1700 name=TTN-EU \
    up-port=1700
add address=us.mikrotik.thethings.industries down-port=1700 name=TTN-US \
    up-port=1700
/tool user-manager customer
set admin access=\
    own-routers,own-users,own-profiles,own-limits,config-payment-gw
/ip address
add address=192.168.100.167/24 interface=ether1 network=192.168.100.0
add address=10.1.1.5/24 interface=ether2 network=10.1.1.0
/ip cloud
set update-time=no
/ip route
add distance=1 gateway=192.168.100.1
/routing ospf network
add area=backbone network=192.168.100.0/24
/system identity
set name=mtk2
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
/system scheduler
add name=backup on-event="/system backup load=mtk2 password=mikrotik" policy=\
    ftp,reboot,read,write,policy,test,password,sniff,sensitive,romon \
    start-date=jun/05/2020 start-time=19:16:17
/tool user-manager database
set db-path=user-manager
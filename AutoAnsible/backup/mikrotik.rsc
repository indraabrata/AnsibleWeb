# aug/16/2020 14:00:39 by RouterOS 6.28
# software id = UEYT-SWL9
#
/tool user-manager customer
set admin access=\
    own-routers,own-users,own-profiles,own-limits,config-payment-gw
/ip address
add address=10.33.70.99/19 interface=ether1 network=10.33.64.0
/ip route
add distance=1 gateway=10.33.64.1
add distance=1 gateway=10.33.70.1
add distance=1 gateway=10.33.64.1
add distance=1 dst-address=10.33.64.0/19 gateway=10.33.64.1
/romon port
add disabled=no
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
/tool user-manager database
set db-path=user-manager
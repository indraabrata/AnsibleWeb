<h1 align="center">Ansible Web Automation</h1>
<h1 align="center">Network Automation Configuration Management</h2>

Fitur AnsibleAutomation:
- **Autoconfiguration**: otomatis memberikan konfigurasi pada perangkat baru yang terhubung dalam jaringan
- **Configuration**: mengirimkan konfigurasi meliputi IP Static, DHCP server, OSPF, InterVLAN, VLAN
- **Device List**: menampilkan informasi perangkat yang ada pada jaringan
- **Backup**: Backup konfigurasi perangkat
- **Restore**: Restore konfigurasi perangkat

____

# Instalasi
## Requirement
    python 3.6+
    virtualenv

## Quick start
    sudo su
    git clone https://github.com/indraabrata/AnsibleWeb.git
    virtualenv -p python3 env
    source env/bin/activate
    pip3 install -r requirements.txt
    cd AutoAnsible
    python manage.py runserver 0.0.0.0:80
    akses via browser <ip:80>

## Readme
    Pastikan server dapat terhubung ke perangkat router dan switch yang dituju (cisco, huawei, dan mikoritk)
    perangkat sudah terkonfigurasi SSH, IP , dan SCP

___

#### 1. Main Page
![Image of Home](https://github.com/indraabrata/AnsibleWeb/blob/master/AutoAnsible/media/gitpic/Home.png)

#### 2. Device List
![Image of Device List](https://github.com/indraabrata/AnsibleWeb/blob/master/AutoAnsible/media/gitpic/Device%20list.png)

#### 3. Configuration Static
![Image of Configuration](https://github.com/indraabrata/AnsibleWeb/blob/master/AutoAnsible/media/gitpic/configstatic.png)

#### 4. Backup
![Image of Backup](https://github.com/indraabrata/AnsibleWeb/blob/master/AutoAnsible/media/gitpic/backup.png)

#### 5. Restore
![Image of Restore](https://github.com/indraabrata/AnsibleWeb/blob/master/AutoAnsible/media/gitpic/Restore.png)

#### 6. Autoconfiguration
![Image of Autoconfiguration](https://github.com/indraabrata/AnsibleWeb/blob/master/AutoAnsible/media/gitpic/autoconf.png)

___

import paramiko

def grab_banner(ip_address, port):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(ip_address, port=port, username='admin', password='54541691',look_for_keys=False, allow_agent=False, banner_timeout=200)
    except:
        return client._transport.get_banner()


if __name__ == '__main__':
    print(grab_banner('192.168.0.144', 22))
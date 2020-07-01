# Generated by Django 3.0.4 on 2020-07-01 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dj_ansible', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module', models.CharField(max_length=100)),
                ('commands', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'action',
            },
        ),
        migrations.CreateModel(
            name='c_hostname',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('hosts', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='devices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('port', models.CharField(max_length=100)),
                ('ipadd', models.CharField(default='', max_length=100)),
                ('physical', models.CharField(default='', max_length=100)),
                ('protocol', models.CharField(default='', max_length=100)),
                ('preconf', models.CharField(default='empty', max_length=100)),
                ('stats', models.CharField(default='Not Booked', max_length=100)),
                ('new_device_type', models.CharField(default='', max_length=100)),
                ('new_device_mac', models.CharField(default='', max_length=100)),
                ('new_device_os', models.CharField(default='', max_length=100)),
                ('device_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dj_ansible.AnsibleNetworkHost')),
            ],
        ),
        migrations.CreateModel(
            name='kamusport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('portarp', models.CharField(max_length=255)),
                ('portint', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target', models.CharField(max_length=255)),
                ('action', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255)),
                ('time', models.CharField(max_length=255)),
                ('messages', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PlayBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('hosts', models.CharField(max_length=100)),
                ('become', models.CharField(max_length=100)),
                ('become_method', models.CharField(max_length=100)),
                ('gather_facts', models.CharField(max_length=100)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Automation.Actions')),
            ],
        ),
        migrations.CreateModel(
            name='iosrouter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('hostname', models.CharField(default='', max_length=100)),
                ('port_ip', models.CharField(default='', max_length=100)),
                ('port_cmd', models.CharField(default='', max_length=100)),
                ('i_vlan_int', models.CharField(default='', max_length=100)),
                ('i_vlan_enc', models.CharField(default='', max_length=100)),
                ('i_vlan_cmd', models.CharField(default='', max_length=100)),
                ('ospf', models.CharField(default='', max_length=100)),
                ('ospf_network', models.CharField(default='', max_length=100)),
                ('ospf_area', models.CharField(default='', max_length=100)),
                ('dhcp_network', models.CharField(default='', max_length=100)),
                ('default_router', models.CharField(default='', max_length=100)),
                ('dns_server', models.CharField(default='', max_length=100)),
                ('dhcp_pool', models.CharField(default='', max_length=100)),
                ('port_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Automation.devices')),
            ],
        ),
        migrations.CreateModel(
            name='ios_switch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('hostname', models.CharField(default='', max_length=100)),
                ('port_ip', models.CharField(default='', max_length=100)),
                ('port_cmd', models.CharField(default='', max_length=100)),
                ('vlan_id', models.CharField(default='', max_length=100)),
                ('vlan_name', models.CharField(default='', max_length=100)),
                ('port_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Automation.devices')),
            ],
        ),
        migrations.CreateModel(
            name='ce_router',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('hostname', models.CharField(default='', max_length=255)),
                ('port_ip', models.CharField(default='', max_length=255)),
                ('ip_add', models.CharField(default='', max_length=255)),
                ('i_vlan_int', models.CharField(default='', max_length=255)),
                ('i_vlan_ip', models.CharField(default='', max_length=255)),
                ('i_vlan_enc', models.CharField(default='', max_length=255)),
                ('ospf', models.CharField(default='ospf', max_length=255)),
                ('ospf_area', models.CharField(default='', max_length=255)),
                ('ospf_network', models.CharField(default='', max_length=255)),
                ('dhcp_enable', models.CharField(default='dhcp enable', max_length=255)),
                ('dhcp_int', models.CharField(default='', max_length=255)),
                ('dhcp_ipadd', models.CharField(default='', max_length=255)),
                ('dhcp_select', models.CharField(default='dhcp select interface', max_length=255)),
                ('dhcp_server_dnslist', models.CharField(default='', max_length=255)),
                ('dhcp_server_excluded', models.CharField(default='', max_length=255)),
                ('port_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Automation.devices')),
            ],
        ),
        migrations.CreateModel(
            name='arp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ipadd', models.CharField(default='', max_length=255)),
                ('mac', models.CharField(default='', max_length=255)),
                ('port', models.CharField(default='', max_length=255)),
                ('device_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dj_ansible.AnsibleNetworkHost')),
            ],
        ),
    ]

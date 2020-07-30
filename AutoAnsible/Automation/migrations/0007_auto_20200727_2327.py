# Generated by Django 3.0.4 on 2020-07-27 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Automation', '0006_remove_devices_new_device_os'),
    ]

    operations = [
        migrations.RenameField(
            model_name='iosrouter',
            old_name='dns_server',
            new_name='default_router2',
        ),
        migrations.AddField(
            model_name='iosrouter',
            name='default_router3',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='iosrouter',
            name='dhcp_excluded',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='iosrouter',
            name='dhcp_excluded2',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='iosrouter',
            name='dhcp_excluded3',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='iosrouter',
            name='dhcp_mask',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='iosrouter',
            name='dhcp_mask2',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='iosrouter',
            name='dhcp_mask3',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='iosrouter',
            name='dhcp_network2',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='iosrouter',
            name='dhcp_network3',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='iosrouter',
            name='dhcp_pool2',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='iosrouter',
            name='dhcp_pool3',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='iosrouter',
            name='i_vlan_cmd2',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='iosrouter',
            name='i_vlan_enc2',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='iosrouter',
            name='i_vlan_int2',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='iosrouter',
            name='ospf2',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='iosrouter',
            name='ospf3',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='iosrouter',
            name='ospf_area2',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='iosrouter',
            name='ospf_area3',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='iosrouter',
            name='ospf_network2',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='iosrouter',
            name='ospf_network3',
            field=models.CharField(default='', max_length=100),
        ),
    ]

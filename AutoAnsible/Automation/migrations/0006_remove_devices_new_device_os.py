# Generated by Django 3.0.4 on 2020-07-27 03:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Automation', '0005_mac_os'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devices',
            name='new_device_os',
        ),
    ]

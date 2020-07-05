from __future__ import absolute_import, unicode_literals
from celery import shared_task
import time
from dj_ansible.models import AnsibleNetworkHost, AnsibleNetworkGroup
from dj_ansible.ansible_kit import execute
from dj_ansible import *
from helloworld.celery import app
import threading


@shared_task
def sum(a,b):
    time.sleep(10)
    return a+b

@shared_task
def hello(test):
    print(f'Hahahahaa aku cinta {test}')

@app.task
def arp(a):
    time.sleep(10)
    my_play = dict(
           name="show huawei",
           hosts=a,
           become='yes',
           become_method='enable',
           gather_facts='no',
           vars=[
               dict(ansible_command_timeout=120)
           ],
           tasks=[
               dict(action=dict(module='ce_command', commands='display arp'))
           ]
       )
    print(my_play)
    result = execute(my_play)
    con = result.stats
    why = result.results
    print(why)
    print(con)

@shared_task
def coba(a):
    time.sleep(10)
    arp(a)




from django.db import models

class Actions(models.Model):
    module = models.CharField(max_length=100)
    commands = models.CharField(max_length=100)

    class Meta:
        db_table = 'action'

class PlayBook(models.Model):
    name = models.CharField(max_length=100)
    hosts = models.CharField(max_length=100)
    become = models.CharField(max_length=100)
    become_method = models.CharField(max_length=100)
    gather_facts = models.CharField(max_length=100)
    task = models.ForeignKey(Actions, on_delete=models.DO_NOTHING)
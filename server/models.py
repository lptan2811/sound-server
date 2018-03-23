from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.utils import timezone
# Create your models here.


class Users(models.Model):
    class Meta:
        db_table = 'users'
    id = models.AutoField(primary_key=True)
    name = models.TextField(default='')
    email = models.TextField(default='')
    gender = models.SmallIntegerField(default=0)

class Sound(models.Model):
    class Meta:
        db_table = 'sound'

    id = models.AutoField(primary_key=True)
    time_start = models.DateTimeField(null=True, blank=True, default=timezone.now)
    wave = ArrayField(models.FloatField(), blank=True, default=[])
    sr = models.IntegerField(default=16000)
    label = JSONField(default={}, null=True, blank=True)
    user_id = models.ForeignKey(Users, default='')

    @classmethod
    def createR(cls, label):
        new_label = cls(label=label)
        return new_label

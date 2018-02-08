from django.db import models


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
    label = models.TextField(default='')

    @classmethod
    def createR(cls, label):
        new_label = cls(label=label)
        return new_label

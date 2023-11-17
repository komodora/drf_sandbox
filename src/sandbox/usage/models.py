from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(verbose_name='氏名', max_length=20)

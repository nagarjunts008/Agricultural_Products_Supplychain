from django.db import models
from datetime import datetime

# Create your models here.
class manufacturer(models.Model):
    manufacturername = models.CharField(max_length=100)
    companyname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class products(models.Model):
    manufacturerid = models.IntegerField()
    productname = models.CharField(max_length=100)
    price = models.IntegerField()
    img = models.ImageField(upload_to ='pics/')
    description = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

class user(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    pincode = models.IntegerField()
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class logistics(models.Model):
    logisticsname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


class ordertrack(models.Model):
    userid = models.IntegerField()
    orderid = models.IntegerField()
    productid = models.IntegerField()
    manufacturerid = models.CharField(max_length=100)
    trasactionhash = models.CharField(max_length=100)
    orderstatus = models.CharField(max_length=100)
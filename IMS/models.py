from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Data(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stock_data')
    created_date = models.DateTimeField(default=timezone.now)
    install_date = models.DateField(default=timezone.now)
    serial = models.CharField(unique=True, max_length=25)
    next_serial = models.CharField(max_length=25, null=True, blank=True)
    hostname = models.CharField(max_length=25, null=True, blank=True)
    place = models.CharField(max_length=10, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.ForeignKey("Status", on_delete=models.CASCADE, related_name='stock_data')
    vendor = models.ForeignKey("Vendor", on_delete=models.CASCADE, related_name='stock_data')
    location = models.ForeignKey("location", on_delete=models.CASCADE, related_name='stock_data')
    part = models.ForeignKey("Part", on_delete=models.CASCADE, related_name='stock_data')

class Vendor(models.Model):
    vendor = models.CharField(unique=True, max_length=10)
    def __str__(self):
        return self.vendor

class Location(models.Model):
    location = models.CharField(unique=True, max_length=10)
    address = models.CharField(max_length=100)
    def __str__(self):
        return self.location

class Part(models.Model):
    part = models.CharField(max_length=40)
    part_number = models.CharField(unique=True, max_length=30)
    vendor = models.ForeignKey("Vendor", on_delete=models.CASCADE)

    class Meta:
        ordering = ['part']
    
    def __str__(self):
        return self.part

class Status(models.Model):
    status = models.CharField(max_length=10)
    def __str__(self):
        return self.status

# 배달 관리 앱
class Delivery(models.Model):
    status_list = [
        ('WAIT', '출고대기'),
        ('OUT', '출고'),
    ]
    vendor_list = [
        ('juniper', 'juniper'),
        ('extreme', 'extreme'),
        ('accedian', 'accedian'),
        ('gigamon', 'gigamon'),
        ('cisco', 'cisco')
    ]
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='delivery')
    created_date = models.DateTimeField(default=timezone.now)
    rma_num = models.CharField(max_length=20, null=True, blank=True)
    serial = models.CharField(max_length=25, null=True, blank=True)
    vendor = models.CharField(max_length=10, null=True, blank=True, choices = vendor_list)
    part = models.CharField(max_length=25, null=True, blank=True)
    status = models.CharField(max_length=5, null=True, blank=True, choices = status_list)
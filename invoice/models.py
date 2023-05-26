from django.db import models

# Create your models here.
from django.db import models

class Seller(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.TextField()

class Buyer(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.TextField()

class Item(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE, related_name='items')

class Invoice(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='invoices')
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='invoices')
    created_at = models.DateTimeField(auto_now_add=True)

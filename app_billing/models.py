from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
class Items(models.Model):
    item_name = models.CharField(max_length=120)

    def __str__(self):
        return self.item_name


class Purchase(models.Model):
    items = models.ForeignKey(Items, on_delete=models.CASCADE)
    purchase_qty = models.IntegerField(default=0)
    purchase_price = models.IntegerField()
    selling_price = models.IntegerField()
    purchase_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.items


class Order(models.Model):
    billnumber = models.CharField(max_length=12, unique=True)
    bill_date = models.DateField(auto_now=True)
    customer_name = models.CharField(max_length=60)
    phone_number = models.CharField(max_length=12)
    bill_total = models.IntegerField(default=0)

    def __str__(self):
        return str(self.billnumber)


class OrderLine(models.Model):
    bill_number = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_name = models.ForeignKey(Items, on_delete=models.CASCADE)
    product_qty = models.FloatField()
    amount= models.FloatField()
    def __str__(self):
        return str(self.bill_number)




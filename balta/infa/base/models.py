from django.db import models
from django.contrib.auth.models import User

class Shoe(models.Model):
    name = models.CharField(max_length=30)
    size = models.CharField(max_length=2)
    price = models.IntegerField()
    quantity = models.IntegerField()
class Order(models.Model):
    Customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    Shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE, null=True)
    Date = models.DateField()



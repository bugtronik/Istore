from django.db import models
from .models import Category

class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=200)
    price = models.DecimalField()
    stock = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

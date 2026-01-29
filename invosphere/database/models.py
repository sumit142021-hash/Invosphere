from django.db import models

class Billing(models.Model):
    category = models.CharField(max_length=100)
    dish = models.CharField(max_length=100)
    qty = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
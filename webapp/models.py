from django.db import models

# Create your models here.
class ItemList(models.Model):
    gameID = models.CharField(max_length=20, null=True)
    gameName = models.CharField(max_length=20, default='test')
    itemName = models.CharField(max_length=20)
    currentPrice = models.DecimalField(max_digits=10, decimal_places=0)

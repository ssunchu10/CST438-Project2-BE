from django.db import models

# Create your models here.

class User(models.Model):
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

class Item(models.Model):
    list_id = models.ForeignKey('List', on_delete=models.CASCADE, related_name='items')  # Adjust this relationship as necessary
    item_name = models.CharField(max_length=100)
    url = models.URLField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
class List(models.Model):
    name = models.CharField(max_length=100)
    is_public = models.BooleanField(default=False)
def __str__(self):
    return self.item_name

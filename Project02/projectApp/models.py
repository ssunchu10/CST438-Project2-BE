from django.db import models

# Create your models here.
#models.py
class User(models.Model):
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    def __str__(self):
        return self.email

class Item(models.Model):
    id = models.BigAutoField(primary_key=True)
    item_name = models.CharField(max_length=100, unique=True)  # Ensure item names are unique
    image_url = models.URLField(max_length=200, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.item_name
class List(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name
class Entry(models.Model):
    id = models.BigAutoField(primary_key=True)
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='entries')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='entries')

    def __str__(self):
        return f"{self.list.name} - {self.item.item_name}"

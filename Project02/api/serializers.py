from rest_framework import serializers 
from projectApp.models import User, Item

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User 
        fields= '__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'list_id', 'item_name', 'url', 'price', 'quantity', 'description'] 
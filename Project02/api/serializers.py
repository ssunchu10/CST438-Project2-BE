from rest_framework import serializers
from projectApp.models import User, Item, List, Entry

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User 
        fields= '__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'item_name', 'image_url', 'price', 'quantity', 'description'] 

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['id', 'user', 'name', 'is_public']

class EntrySerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    class Meta:
        model = Entry
        fields = ['id', 'list', 'item']

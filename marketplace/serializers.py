from rest_framework import serializers
from .models import Entrepreneur, Product, Order
from villages.serializers import VillageSerializer


class EntrepreneurSerializer(serializers.ModelSerializer):
    village = VillageSerializer(read_only=True)
    village_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = Entrepreneur
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    entrepreneur = EntrepreneurSerializer(read_only=True)
    entrepreneur_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.UUIDField(write_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['user']
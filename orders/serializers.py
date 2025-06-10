# serializers.py
from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
    
    def validate_pickup_lat(self, value):
        if not -90 <= value <= 90:
            raise serializers.ValidationError("Latitud de recogida inválida (-90 a 90)")
        return value
    
    def validate_pickup_lng(self, value):
        if not -90 <= value <= 90:
            raise serializers.ValidationError("Longitud de recogida inválida (-90 a 90)")
        return value
    
    def validate_delivery_lat(self, value):
        if not -90 <= value <= 90:
            raise serializers.ValidationError("Latitud de entrega inválida (-90 a 90)")
        return value

    def validate_delivery_lng(self, value):
        if not -90 <= value <= 90:
            raise serializers.ValidationError("Latitud de entrega inválida (-90 a 90)")
        return value
    
    
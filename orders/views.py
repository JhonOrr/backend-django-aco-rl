from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()  # Consulta todas las órdenes
    serializer_class = OrderSerializer  # Usa el serializer creado
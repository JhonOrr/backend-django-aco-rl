from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer
from django.http import JsonResponse

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_fields = ['status']

def latest_order(request):
    order = Order.objects.latest('created_at')  # Asegúrate de tener created_at en tu modelo
    return JsonResponse({
        'id': order.id,
        'customer': order.customer,
        'status': order.status
    })
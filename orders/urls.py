from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet)  # Endpoint: /api/orders/

urlpatterns = [
    path('api/', include(router.urls)),
]
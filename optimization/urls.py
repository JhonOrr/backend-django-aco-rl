from django.urls import path
from . import views

urlpatterns = [
    path('run-aco/', views.run_aco, name='run_aco'),
    path('get-routes/', views.get_routes, name='get_routes'),
]

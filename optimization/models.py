from django.db import models
import json

# Create your models here.

class OptimizedRoute(models.Model):
    """
    Modelo para almacenar las rutas optimizadas generadas por el algoritmo ACO
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    routes_data = models.JSONField()
    best_distance = models.FloatField()
    num_ants = models.IntegerField()
    iterations = models.IntegerField()
    evaporation_rate = models.FloatField()
    alpha = models.FloatField()
    beta = models.FloatField()
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Rutas optimizadas - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    
    @classmethod
    def get_latest(cls):
        """Obtiene la ruta optimizada más reciente"""
        return cls.objects.first()
    
    @classmethod
    def save_routes(cls, routes_data, best_distance, algorithm_params):
        """Guarda las rutas optimizadas con los parámetros del algoritmo"""
        return cls.objects.create(
            routes_data=routes_data,
            best_distance=best_distance,
            num_ants=algorithm_params.get('num_ants', 20),
            iterations=algorithm_params.get('iterations', 200),
            evaporation_rate=algorithm_params.get('evaporation_rate', 0.1),
            alpha=algorithm_params.get('alpha', 1),
            beta=algorithm_params.get('beta', 3)
        )

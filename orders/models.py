from django.db import models

class Order(models.Model):

  STATUS_CHOICES = [
      ('Pendiente', 'Pendiente'),
      ('En Proceso', 'En Proceso'),
      ('Completado', 'Completado'),
  ]

  customer = models.CharField(max_length=100)
  capacity = models.DecimalField(max_digits=10, decimal_places=2)
  status = models.CharField(
      max_length=20,
      choices=STATUS_CHOICES,
      default='PENDIENTE',
  )
  pickup_lat = models.DecimalField(max_digits=9, decimal_places=6)  # Latitud recogida
  pickup_lng = models.DecimalField(max_digits=9, decimal_places=6)  # Longitud recogida
  delivery_lat = models.DecimalField(max_digits=9, decimal_places=6) # Latitud entrega
  delivery_lng = models.DecimalField(max_digits=9, decimal_places=6) # Longitud entrega
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pendiente')

  created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación automática

  def __str__(self):
    return self.id
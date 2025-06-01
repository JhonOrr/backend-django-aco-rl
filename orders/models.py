from django.db import models

# Create your models here.
class Order(models.Model):

  ESTADOS = (
    ('PENDIENTE', 'Pendiente'),
    ('EN PROCESO', 'En proceso'),
    ('COMPLETADO', 'Completado'),
  )

  cliente = models.CharField(max_length=100)
  capacidad = models.DecimalField(max_digits=10, decimal_places=2)
  estado = models.CharField(
      max_length=20,
      choices=ESTADOS,
      default='PENDIENTE',
  )
  latitud_partida = models.CharField(max_length = 15, default='')
  latitud_destino = models.CharField(max_length = 15, default='')
  longitud_partida = models.CharField(max_length = 15, default='')
  longitud_destino = models.CharField(max_length = 15 ,default='')

  def __str__(self):
    return self.id
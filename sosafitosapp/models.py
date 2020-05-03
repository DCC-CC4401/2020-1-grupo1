from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Reporte(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    foto = models.ImageField(upload_to='Reportes')
    fecha = models.DateField(default=timezone.now)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)

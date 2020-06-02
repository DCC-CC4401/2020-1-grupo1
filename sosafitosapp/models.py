from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

# Create your models here.


class Reporte(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    foto = models.ImageField(upload_to="Reportes")
    fecha = models.DateField(default=timezone.now)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('home')
    
    def save(self):
        super().save()

        img = Image.open(self.foto.path)

        if img.height>1080 or img.width> 1920:
            output_size = (1920,1080)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Tag(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    reportes = models.ManyToManyField(Reporte, related_name="tags")

    def __str__(self):
        return self.nombre

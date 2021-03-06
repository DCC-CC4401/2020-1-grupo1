from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from location_field.models.plain import PlainLocationField
from PIL import Image
from taggit.managers import TaggableManager


# Create your models here.


class Reporte(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(default=None)
    foto = models.ImageField(upload_to='Reportes', default=None)
    fecha = models.DateField(default=timezone.now)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    ciudad = models.CharField(max_length=255)
    ubicacion = PlainLocationField(based_fields=['ciudad'], zoom=7)
    tags = TaggableManager()

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('home')

    def save(self):
        super().save()

        img = Image.open(self.foto.path)

        if img.height > 1080 or img.width > 1920:
            output_size = (1920, 1080)
            img.thumbnail(output_size)
            img.save(self.foto.path)


class Comentario(models.Model):
    contenido = models.TextField(max_length=400)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    reporte_padre = models.ForeignKey(Reporte, on_delete=models.CASCADE)

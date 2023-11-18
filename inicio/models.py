from django.db import models
from ckeditor.fields import RichTextField
from usuarios.models import Usuario
from django.core.validators import MaxValueValidator, MinValueValidator

class Autor(models.Model):
    nombre = models.CharField(max_length=30)
    nacionalidad = models.CharField(max_length=30)
    def __str__(self):
      return f'{self.id} - {self.nombre}'

class Editorial(models.Model):
    nombre = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    def __str__(self):
      return f'{self.id} - {self.nombre}'

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE)
    fecha_de_publicacion = models.DateField()
    hojas = models.IntegerField()
    descripcion = RichTextField()
    portada = models.ImageField(upload_to='imagenes_libros/', null=True)
    creador = models.ForeignKey(Usuario, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.titulo
    
class Resena(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    puntuacion = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comentario = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reseña de {self.usuario.username} para {self.libro.titulo}'
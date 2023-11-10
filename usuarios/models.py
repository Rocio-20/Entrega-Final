from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    nombre = models.CharField(max_length=100, blank=True)
    apellido = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    biografia = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True)
    fecha_de_cumpleanios = models.DateField(null=True, blank=True)

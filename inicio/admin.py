from django.contrib import admin
from inicio.models import Autor, Libro, Editorial


# Register your models here.
admin.site.register(Autor)
admin.site.register(Libro)
admin.site.register(Editorial)
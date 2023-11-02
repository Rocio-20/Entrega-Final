from django.urls import path
from inicio.views import inicio, autores, crear_autor, crear_editorial, crear_libro, lista_libros

urlpatterns = [
    path('',inicio, name ='inicio'),
    path('autores/',autores, name = 'autores'),
    path('autores/crear',crear_autor, name = 'crear_autores'),
    path('editoriales/',crear_editorial, name = 'crear_editorial'),
    path('libros/',crear_libro, name = 'crear_libro'),
    path('libros/l_libros',lista_libros, name='lista_libros')
]
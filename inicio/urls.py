from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from inicio.views import inicio, autores, crear_autor, crear_editorial, crear_libro, buscar_libros, libro, lista_libros, editar_libro, eliminar_libro

urlpatterns = [
    path('',inicio, name ='inicio'),
    path('autores/',autores, name = 'autores'),
    path('autores/crear',crear_autor, name = 'crear_autores'),
    path('editoriales/',crear_editorial, name = 'crear_editorial'),
    path('libros/crear/',crear_libro, name = 'crear_libro'),
    path('libros/b_libros',buscar_libros, name='buscar_libros'),
    path('libros/',libro, name='libros'),
    path('libros/l_libros', lista_libros, name = 'lista_libros'),
    path('libros/editar/<int:libro_id>/', editar_libro, name='editar_libro'),
    path('libros/eliminar/<int:libro_id>/', eliminar_libro, name='eliminar_libro'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
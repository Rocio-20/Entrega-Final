# mensajeria/urls.py
from django.urls import path
from .views import enviar_mensaje, lista_mensajes, buscar_usuarios, perfil_usuario

urlpatterns = [
    path('enviar/<int:receptor_id>', enviar_mensaje, name='enviar_mensaje'),
    path('lista_mensajes/', lista_mensajes, name='lista_mensajes'),
    path('buscar_usuarios/', buscar_usuarios, name='buscar_usuarios'),
    path('perfil_usuario/<int:usuario_id>/', perfil_usuario, name='perfil_usuario'),
]

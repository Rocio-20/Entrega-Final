from django.urls import path
from .views import registro, perfil, editar_perfil, cerrar_sesion, crear_perfil, cambiar_contraseña
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', cerrar_sesion, name='logout'),
    path('registro/', registro, name='registro'),
    path('perfil/', perfil, name='perfil'),
    path('perfil/editar/', editar_perfil, name='editar_perfil'),
    path('crear_perfil/', crear_perfil, name='crear_perfil'),
    path('cambiar-contraseña/', cambiar_contraseña.as_view(), name='cambiar_contraseña'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

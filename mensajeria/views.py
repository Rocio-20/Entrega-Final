# mensajeria/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Mensaje
from django.contrib.auth.decorators import login_required
from usuarios.models import Usuario
from django.db.models import Q
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.datastructures import MultiValueDictKeyError

@login_required
def enviar_mensaje(request, receptor_id):
    receptor = get_object_or_404(Usuario, id=receptor_id)

    if request.method == 'POST':
        try:
            contenido = request.POST['contenido']
            respuesta_a = request.POST.get('respuesta_a', None)

            if respuesta_a:
                mensaje_original = Mensaje.objects.get(id=respuesta_a)
                Mensaje.objects.create(
                    emisor=request.user,
                    receptor=mensaje_original.emisor,
                    contenido=f"RE: {mensaje_original.contenido}\n\n{contenido}"
                )
            else:
                Mensaje.objects.create(emisor=request.user, receptor=receptor, contenido=contenido)

            return redirect('lista_mensajes')  # Redirigir a la lista de mensajes después de enviar el mensaje
        except MultiValueDictKeyError:
            print("No se envió ningún mensaje.")
            pass

    return render(request, 'perfil_usuario.html', {'usuario': receptor})

@login_required
def lista_mensajes(request):
    mensajes_enviados = Mensaje.objects.filter(emisor=request.user).order_by('-fecha_envio')
    mensajes_recibidos = Mensaje.objects.filter(receptor=request.user).order_by('-fecha_envio')

    # Obtener la lista de usuarios con los que se ha intercambiado mensajes
    usuarios_intercambio = Usuario.objects.filter(
        Q(mensajes_enviados__receptor=request.user) | Q(mensajes_recibidos__emisor=request.user)
    ).distinct()

    return render(
        request,
        'lista_mensajes.html',
        {'mensajes_enviados': mensajes_enviados, 'mensajes_recibidos': mensajes_recibidos, 'usuarios_intercambio': usuarios_intercambio}
    )

@login_required
def buscar_usuarios(request):
    query = request.GET.get('q', '')
    resultados = Usuario.objects.filter(username__icontains=query).values('id', 'username')
    return render(request, 'lista_mensajes.html', {'resultados_busqueda': resultados})


def perfil_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    print(f"Valor de usuario.id: {usuario.id}")
    return render(request, 'perfil_usuario.html', {'usuario': usuario, 'receptor_id': usuario.id})

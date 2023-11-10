from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from usuarios.forms import RegistroFormulario, EditarPerfil, CrearPerfil
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from usuarios.models import Usuario

def registro(request):
    if request.method == 'POST':
        form = RegistroFormulario(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if Usuario.objects.filter(email=email).exists():
                # Agregar lógica para manejar el caso en que el correo electrónico ya existe
                pass
            else:
                user = form.save()
                login(request, user)
                return redirect('inicio')
    else:
        form = RegistroFormulario()

    return render(request, 'registro.html', {'form': form})
@login_required
def perfil(request):
    usuario = request.user
    return render(request, 'perfil.html', {'usuario': usuario})

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = EditarPerfil(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = EditarPerfil(instance=request.user)

    return render(request, 'editar_perfil.html', {'form': form})

def cerrar_sesion(request):
    response = LogoutView.as_view()(request)
    return redirect('inicio')

def crear_perfil(request):
    if request.method == 'POST':
        form = CrearPerfil(request.POST, request.FILES)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.user = request.user
            perfil.save()
            return redirect('perfil')  # Redirige a la vista de perfil después de crearlo
    else:
        form = CrearPerfil()

    return render(request, 'crear_perfil.html', {'form': form})
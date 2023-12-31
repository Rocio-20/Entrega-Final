from django.shortcuts import render, redirect, get_object_or_404
from inicio.models import Autor, Editorial, Libro
from inicio.forms import CrearAutorFormulario, BusquedaAutorFormulario, CrearEditorialFormulario, CrearLibroFormulario, BusquedaLibro, EditarLibroFormulario, ResenaFormulario
from django.shortcuts import render
from .mixins import CreatorMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from django.http import HttpResponseRedirect


def inicio(request):
  return render(request, 'inicio.html', {})

def autores(request):
    if request.method == 'GET':
        formulario = BusquedaAutorFormulario(request.GET)
        if formulario.is_valid():
            nombre_a_buscar = formulario.cleaned_data.get('nombre')
            listado_autores = Autor.objects.filter(nombre__icontains=nombre_a_buscar)

    else:
        formulario = BusquedaAutorFormulario()

    return render(request, 'autores.html', {'listado_autores': listado_autores, 'formulario': formulario})

@login_required
def crear_autor(request):
  if request.method == 'POST':
        formulario = CrearAutorFormulario(request.POST)
        if formulario.is_valid():
            info_limpia = formulario.cleaned_data
            
            nombre = info_limpia.get('nombre')
            nacionalidad = info_limpia.get('nacionalidad')
    
            autor = Autor(nombre=nombre, nacionalidad = nacionalidad)
            autor.save()
            
            return redirect(reverse('autores'))
        else:
            return render(request, 'crear_autor.html', {'formulario': formulario})
        
  formulario = CrearAutorFormulario()
  return render(request, 'crear_autor.html', {'formulario': formulario})

@login_required
def crear_editorial(request):
    if request.method == 'POST':
        form = CrearEditorialFormulario(request.POST)
        if form.is_valid():
            info_limpia = form.cleaned_data
            nombre = info_limpia.get('nombre')
            website = info_limpia.get('website')
            editorial = Editorial(nombre=nombre, website = website)
            editorial.save()
            return redirect(reverse('crear_editorial'))
    
    form = CrearEditorialFormulario()
    listado_editoriales = Editorial.objects.all()
    return render(request, 'crear_editorial.html', {'form': form, 'listado_editoriales': listado_editoriales})

def libro(request):
    return render(request, 'libros.html', {})

def buscar_libros(request):
    lista_libros = None
    if request.method == 'GET':
        formulario = BusquedaLibro(request.GET)
        if formulario.is_valid():
            titulo_a_buscar = formulario.cleaned_data.get('nombre')
            if titulo_a_buscar:
                lista_libros = Libro.objects.filter(titulo__icontains=titulo_a_buscar)
            else:
                lista_libros = Libro.objects.all()

    else:
        formulario = BusquedaLibro()

    return render(request, 'buscar_libros.html', {'lista_libros': lista_libros, 'formulario': formulario})

class CrearLibroView(CreatorMixin, SuccessMessageMixin, CreateView):
    model = Libro
    form_class = CrearLibroFormulario
    template_name = 'crear_libro.html'
    success_message = 'El libro se creó con éxito.'
    success_url = reverse_lazy('lista_libros')

    def form_valid(self, form):
        form.instance.creador = self.request.user
        portada = form.cleaned_data['portada']
        if isinstance(portada, InMemoryUploadedFile):
            img = Image.open(portada)
            
            if img.mode == 'RGBA':
                img = img.convert('RGB')

            img.thumbnail((300, 300))  

            output = BytesIO()
            img.save(output, format='JPEG')
            output.seek(0)

            form.instance.portada = InMemoryUploadedFile(
                output,
                'ImageField',  
                f"{portada.name.split('.')[0]}_resized.jpg", 
                'image/jpeg',
                output.getbuffer().nbytes,
                None
            )

        response = super().form_valid(form)
        return response
    
    def get_success_url(self):
        return reverse('lista_libros')

def es_admin(usuario):
    return usuario.is_staff

def es_creador_o_admin(user, libro):
    return user == libro.creador or user.is_staff

@login_required(login_url='libros') 
def editar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)

    if not es_creador_o_admin(request.user, libro):
        messages.error(request, 'No tienes permisos para editar este libro.')
        return redirect('lista_libros')

    if request.method == 'POST':
        formulario = EditarLibroFormulario(request.POST, request.FILES, instance=libro)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Libro editado exitosamente.')
            return redirect('lista_libros')
        else:
            messages.error(request, 'Error en el formulario. Por favor, corrige los errores.')

    else:
        formulario = EditarLibroFormulario(instance=libro)

    return render(request, 'editar_libro.html', {'formulario': formulario, 'libro': libro})

@login_required(login_url='libro')
def eliminar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    if not es_creador_o_admin(request.user, libro):
        messages.error(request, 'No tienes permisos para eliminar este libro.')
        return redirect('lista_libros')
    
    if request.method == 'POST':
        libro.delete()
        messages.success(request, 'Libro eliminado exitosamente.')
        return redirect('lista_libros')

    return render(request, 'eliminar_libro.html', {'libro': libro})

def lista_libros(request):
    libros = Libro.objects.all()
    return render(request, 'lista_libros.html', {'libros': libros})

def about_me(request):
    return render(request, 'about_me.html')

@login_required
def crear_resena(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)

    if request.method == 'POST':
        formulario = ResenaFormulario(request.POST)
        if formulario.is_valid():
            resena = formulario.save(commit=False)
            resena.usuario = request.user
            resena.libro = libro
            resena.save()
            messages.success(request, 'Reseña creada exitosamente.')
            return redirect('detalle_libro', libro_id=libro.id)
    else:
        formulario = ResenaFormulario()

    return render(request, 'crear_resena.html', {'formulario': formulario, 'libro': libro})

def detalle_libro(request, libro_id):
    libro = Libro.objects.get(pk=libro_id)
    reseñas = libro.resena_set.all()
    return render(request, 'detalle_libro.html', {'libro': libro, 'reseñas': reseñas})
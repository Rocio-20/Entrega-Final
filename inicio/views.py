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
            
            return redirect('autores')
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
                # Si el título a buscar es None, podrías querer mostrar todos los libros
                lista_libros = Libro.objects.all()

    else:
        formulario = BusquedaLibro()

    return render(request, 'buscar_libros.html', {'lista_libros': lista_libros, 'formulario': formulario})

class CrearLibroView(CreatorMixin, SuccessMessageMixin, CreateView):
    model = Libro
    form_class = CrearLibroFormulario
    template_name = 'crear_libro.html'
    success_url = reverse_lazy('lista_libros')
    success_message = 'El libro se creó con éxito.'

    def form_valid(self, form):
        form.instance.creador = self.request.user
        portada = form.cleaned_data['portada']
        if isinstance(portada, InMemoryUploadedFile):
            # Convierte el archivo en memoria a un objeto Image
            img = Image.open(portada)
            
            # Convierte la imagen a modo RGB si está en modo RGBA
            if img.mode == 'RGBA':
                img = img.convert('RGB')

            img.thumbnail((300, 300))  # Ajusta el tamaño según tus necesidades

            # Guarda la imagen redimensionada en un BytesIO
            output = BytesIO()
            img.save(output, format='JPEG')
            output.seek(0)

            # Actualiza el campo de la portada con la nueva imagen
            form.instance.portada = InMemoryUploadedFile(
                output,
                'ImageField',  # Usa 'ImageField' como tipo de archivo
                f"{portada.name.split('.')[0]}_resized.jpg",  # Nombre del archivo
                'image/jpeg',
                output.getbuffer().nbytes,
                None
            )
        return super().form_valid(form)

@login_required
def editar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)

    if request.method == 'POST':
        formulario = EditarLibroFormulario(request.POST, request.FILES, instance=libro)
        if formulario.is_valid():
            formulario.save()
            return redirect('lista_libros')
    else:
        formulario = EditarLibroFormulario(instance=libro)

    return render(request, 'editar_libro.html', {'formulario': formulario, 'libro': libro})

@login_required
def eliminar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)

    if request.method == 'POST':
        libro.delete()
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
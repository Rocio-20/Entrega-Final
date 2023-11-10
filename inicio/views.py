from django.contrib.auth import login
from .forms import RegistroFormulario
from django.shortcuts import render, redirect, get_object_or_404
from inicio.models import Autor, Editorial, Libro
from django.contrib import messages
from inicio.forms import CrearAutorFormulario, BusquedaAutorFormulario, CrearEditorialFormulario, CrearLibroFormulario, BusquedaLibro, EditarLibroFormulario
from django.shortcuts import render
from PIL import Image
from io import BytesIO

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

def crear_libro(request):
    if request.method == 'POST':
        form = CrearLibroFormulario(request.POST, request.FILES)
        if form.is_valid():
            libro = form.save()
            # Procesa la imagen antes de guardarla
            if libro.portada:
                img = Image.open(libro.portada.path)
                img.thumbnail((300, 300))  # Ajusta el tamaño según tus necesidades
                img.save(libro.portada.path)

            libro.save()
            # Mensaje de creación exitosa
            messages.success(request, 'El libro se creó con éxito.')
            # Restablecer los valores del formulario
            form = CrearLibroFormulario()
            return redirect('lista_libros')
        else:
            messages.error(request, 'Error en el formulario. Por favor, verifica los campos.')
    else:
        form = CrearLibroFormulario()
    
    print(form.errors)
    return render(request, 'crear_libro.html', {'form': form})

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

def eliminar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)

    if request.method == 'POST':
        libro.delete()
        return redirect('lista_libros')

    return render(request, 'eliminar_libro.html', {'libro': libro})

def lista_libros(request):
    libros = Libro.objects.all()
    return render(request, 'lista_libros.html', {'libros': libros})

def registro(request):
    if request.method == 'POST':
        form = RegistroFormulario(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio')
    else:
        form = RegistroFormulario()

    return render(request, 'registro.html', {'form': form})

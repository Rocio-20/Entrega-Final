from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from inicio.models import Autor, Editorial, Libro
from inicio.forms import CrearAutorFormulario, BusquedaAutorFormulario, CrearEditorialFormulario, CrearLibroFormulario

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

      
def crear_libro(request):
    if request.method == 'POST':
        form = CrearLibroFormulario(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_libros')
    else:
        form = CrearLibroFormulario()
    return render(request, 'crear_libro.html', {'form': form})

def lista_libros(request):
    libros = Libro.objects.all()
    return render(request, 'lista_libros.html', {'libros': libros})



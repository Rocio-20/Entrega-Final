from django import forms
from inicio.models import Libro, Autor, Editorial, Resena
from ckeditor.fields import RichTextField
from django.forms import ClearableFileInput
from PIL import Image

class CrearAutorFormulario(forms.Form):
    nombre = forms.CharField(max_length=30, required=False)
    nacionalidad = forms.CharField(max_length=30, required=False)

class CrearEditorialFormulario(forms.Form):
    nombre = forms.CharField(max_length=30, required=False)
    website = forms.URLField(required=False)

class CrearLibroFormulario(forms.ModelForm):
    descripcion = RichTextField(blank=True)

    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'editorial', 'fecha_de_publicacion', 'hojas', 'descripcion', 'portada']

    def __init__(self, *args, **kwargs):
        super(CrearLibroFormulario, self).__init__(*args, **kwargs)
        self.fields['autor'].widget = forms.Select(choices=Autor.objects.all().values_list('id', 'nombre'))
        self.fields['editorial'].widget = forms.Select(choices=Editorial.objects.all().values_list('id', 'nombre'))
        self.fields['portada'].widget = ClearableFileInput(attrs={'accept': 'image/*', 'onchange': 'validateImageSize(this)'})

    def clean_portada(self):
        portada = self.cleaned_data.get('portada')
        if not portada:
            raise forms.ValidationError("Por favor, carga una imagen.")
        return portada

class BusquedaAutorFormulario(forms.Form):
    nombre = forms.CharField(max_length=30, required=False)

class BusquedaLibro(forms.Form):
    nombre = forms.CharField(max_length=30, required=False)

class EditarLibroFormulario(forms.ModelForm):
    descripcion = RichTextField(blank=True)

    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'editorial', 'fecha_de_publicacion', 'hojas', 'descripcion', 'portada']

class ResenaFormulario(forms.ModelForm):
    comentario = RichTextField(blank=True)
    class Meta:
        model = Resena
        fields = ['puntuacion', 'comentario']

    def __init__(self, *args, **kwargs):
        super(ResenaFormulario, self).__init__(*args, **kwargs)


from django import forms
from .models import Libro, Autor, Editorial

class CrearAutorFormulario(forms.Form):
    nombre = forms.CharField(max_length=30, required=False)
    nacionalidad = forms.CharField(max_length=30, required=False)

class CrearEditorialFormulario(forms.Form):
    nombre = forms.CharField(max_length=30, required=False)
    website = forms.URLField(required=False)

class CrearLibroFormulario(forms.ModelForm):
    class Meta:
        model = Libro
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CrearLibroFormulario, self).__init__(*args, **kwargs)
        self.fields['autor'].widget = forms.Select(choices=Autor.objects.all().values_list('id', 'nombre'))
        self.fields['editorial'].widget = forms.Select(choices=Editorial.objects.all().values_list('id', 'nombre'))

class BusquedaAutorFormulario(forms.Form):
    nombre = forms.CharField(max_length=30, required=False)


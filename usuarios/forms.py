from django import forms
from usuarios.models import Usuario
from django.contrib.auth.forms import UserCreationForm

class RegistroFormulario(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    fecha_de_cumpleanios = forms.DateField(required=False, widget=forms.SelectDateWidget())
    nombre = forms.CharField(max_length=30, required=True)
    apellido = forms.CharField(max_length=30, required=True)
    biografia = forms.CharField(widget=forms.Textarea, required=False)
    avatar = forms.ImageField(required=False)
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'fecha_de_cumpleanios', 'nombre', 'apellido', 'biografia', 'avatar', 'password1', 'password2']

class EditarPerfil(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'email', 'avatar', 'biografia', 'fecha_de_cumpleanios']

class CrearPerfil(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'email', 'avatar', 'biografia', 'fecha_de_cumpleanios']
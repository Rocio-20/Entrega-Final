from django import forms
from usuarios.models import Usuario
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import SelectDateWidget
from datetime import datetime
from django.contrib.auth.forms import PasswordChangeForm

class RegistroFormulario(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    current_year = datetime.now().year
    fecha_de_nacimiento = forms.DateField(required=False, widget=SelectDateWidget(years=range(current_year - 100, current_year + 1)))
    nombre = forms.CharField(max_length=30, required=True)
    apellido = forms.CharField(max_length=30, required=True)
    biografia = forms.CharField(widget=forms.Textarea, required=False)
    avatar = forms.ImageField(required=False)
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'fecha_de_nacimiento', 'nombre', 'apellido', 'biografia', 'avatar']

class EditarPerfil(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'email', 'avatar', 'biografia', 'fecha_de_nacimiento']

class CrearPerfil(forms.ModelForm):
    avatar = forms.ImageField(required=False)
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'email', 'avatar', 'biografia', 'fecha_de_nacimiento']

class CambiarContraseñaFormulario(PasswordChangeForm):
    class Meta:
        model = Usuario
        fields = ('old_password', 'new_password1', 'new_password2')
        
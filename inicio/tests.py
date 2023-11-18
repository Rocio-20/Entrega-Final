from django.test import TestCase
from usuarios.models import Usuario
from inicio.models import Editorial, Autor
from django.urls import reverse

class CrearEditorialTest(TestCase):
    def setUp(self):
        self.admin_user = Usuario.objects.create_user(
            username='admin',
            password='adminpassword',
            is_staff=True,
        )

        self.client.login(username='admin', password='adminpassword')

    def test_creacion_editorial_exitosa(self):
        data = {
            'nombre': 'Editorial de Prueba',
            'website': 'http://www.editorialprueba.com',
        }
        response = self.client.post(reverse('crear_editorial'), data)

        self.assertRedirects(response, reverse('crear_editorial'))
        self.assertTrue(Editorial.objects.filter(nombre='Editorial de Prueba').exists())

class CrearAutorTest(TestCase):
    def setUp(self):
        self.admin_user = Usuario.objects.create_user(
            username='admin',
            password='adminpassword',
            is_staff=True,
        )
        self.client.login(username='admin', password='adminpassword')

    def test_creacion_autor_exitosa(self):
        data = {
            'nombre': 'Autor de Prueba',
            'nacionalidad': 'Nacionalidad de Prueba',
        }

        response = self.client.post(reverse('crear_autores'), data)
        self.assertRedirects(response, reverse('autores'))
        self.assertTrue(Autor.objects.filter(nombre='Autor de Prueba').exists())



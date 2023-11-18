from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .views import cambiar_contraseña

class CambiarContraseñaTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='usuario_de_prueba',
            password='pass_de_prueba',
        )
        self.client.login(username='usuario_de_prueba', password='pass_de_prueba')
        self.url = reverse('cambiar_contraseña')

    def test_vista_carga_correctamente(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cambiar_contraseña.html')

    def test_cambio_contraseña_exitoso(self):
        data = {
            'old_password': 'pass_de_prueba',
            'new_password1': 'pass_nueva',
            'new_password2': 'pass_nueva',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('pass_nueva'))

    def test_cambio_contraseña_fallido(self):
        data = {
            'old_password': 'pass_incorrecta',
            'new_password1': 'pass_nueva',
            'new_password2': 'pass_nueva',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200) 
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('pass_de_prueba'))



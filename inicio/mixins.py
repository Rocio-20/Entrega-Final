# En mixins.py
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Libro

class CreatorMixin(LoginRequiredMixin):
    """
    Mixin para rastrear el creador de un libro.
    """
    def form_valid(self, form):
        form.instance.creador = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['creador'] = self.request.user
        return context

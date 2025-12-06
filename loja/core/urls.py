# core/urls.py
from django.urls import path, re_path
from django.views.generic import TemplateView # Importa para servir o index.html
from . import view # Importa a view que você criou

urlpatterns = [
    # 1. Rota da API (endpoint que o React irá chamar)
    # Recomendado: Use um prefixo /api/ (o React deve chamar /api/handler/)
    path('handler/', view.api_handler, name='api_handler'),
        
    # Rota raiz: Serve o index.html gerado pelo React
    path('', TemplateView.as_view(template_name='Home.jsx'), name='frontend_index'),

    re_path(r'^(?!api/|admin/)(?:.*)/?$', TemplateView.as_view(template_name='index.html')),
]
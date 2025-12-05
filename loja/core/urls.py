from django.urls import path
from . import view

urlpatterns = [
    path('execute/', view.api_execute, name='api_execute'),
    path('handler/', view.api_handler, name='api_handler'),
]

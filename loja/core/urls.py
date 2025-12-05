from django.urls import path
from . import view
from .view import api_execute

urlpatterns = [
    path('', view.index, name='index'),
    path('handler/', view.api_handler, name='handler'),
    path('api/execute/', api_execute, name='api_execute'),
]

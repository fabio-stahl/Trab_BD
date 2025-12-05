from django.urls import path
from . import view

urlpatterns = [
    path('', view.index, name='index'),
    path('handler/', view.api_handler, name='handler'),
]

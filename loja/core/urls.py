from django.urls import path
from . import view

urlpatterns = [
    path("handler/", view.api_handler, name="api_handler"),
]

from django.urls import path
from . import view

urlpatterns = [
    path('', view.index_view, name='index'),
    path('login/', view.login_view, name='login'),
    path('register/', view.register_view, name='register'),
    path('home/', view.dashboard, name='dashboard'),

]

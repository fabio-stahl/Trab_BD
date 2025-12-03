'''

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required
def index_view(request):
    return render(request, 'index.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')  # redireciona para a home
        else:
            return render(request, 'login.html', {"erro": "Usuário ou senha incorretos"})
    
    return render(request, "login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            return render(request, "register.html", {"erro": "Senhas não conferem"})

        User.objects.create_user(username=username, email=email, password=password1)
        return redirect("login")

    return render(request, "register.html")
'''
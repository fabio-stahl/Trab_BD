from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
import json

@login_required(login_url='/login/')
def dashboard(request):
    return render(request, 'dashboard.html')



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

@csrf_exempt
def create_table(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

        except Exception as e:
            print("ERRO no create_table")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

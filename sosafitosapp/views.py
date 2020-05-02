from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from .forms import UserRegisterForm


# Create your views here.
def home(request):
    return render(request, "sosafitosapp/home.html")


def login_user(request):
    if request.method == 'GET':
        return render(request, "sosafitosapp/login.html")

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Bienvenido ' + username)
            return redirect("home")
        else:
            messages.warning(request, 'Usuario o contraseña incorrectos')
            return HttpResponseRedirect('/register/')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def registerReport(request):
    pass


def editProfile(request):
    if request.method == 'GET':
        return render(request, "sosafitosapp/edit_profile.html")

    if request.method == 'POST':
        if request.user.password == request.POST['old password']:
            request.user.username = request.POST['username']
            request.user.password = request.POST['new password']
            request.user.email = request.POST['mail']
            messages.success(request, 'Perfil actualizado!')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, 'Contraseña incorrecta')


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"¡Cuenta creada para {username}!")
            return redirect("home")
    else:
        form = UserRegisterForm()
    return render(request, "sosafitosapp/user_register.html", {"form":form})
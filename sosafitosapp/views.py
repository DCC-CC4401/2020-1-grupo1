from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, "sosafitosapp/home.html")


def register_user(request):
    if request.method == 'GET':
        return render(request, "sosafitosapp/register.html")

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        mail = request.POST['mail']
        user = User.objects.create_user(username=username, password=password, email=mail)
        return HttpResponseRedirect('/')


def login_user(request):
    if request.method == 'GET':
        return render(request, "sosafitosapp/login.html")

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def registerReport(request):
    pass


def editProfile(request):
    if request.method == 'GET':
        return render(request, "sosafitosapp/edit_profile.html")

    if request.method == 'POST':
        pass


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
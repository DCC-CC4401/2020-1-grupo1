from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

def home(request):
    return render(request, "sosafitosapp/login.html")

def login(request):
    pass

def registerReport(request):
    pass

def editProfile(request):
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
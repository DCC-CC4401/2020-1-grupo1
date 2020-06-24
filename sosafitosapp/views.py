from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, EditProfileForm
from sosafitosapp.models import Reporte


def user_is_not_logged_in(user):
    return not user.is_authenticated


@login_required
def home(request):

    reportes = Reporte.objects.all()
    args = {'reportes' : reportes}
    return render(request, "sosafitosapp/home.html", args)


@user_passes_test(user_is_not_logged_in, login_url='/')
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
            return HttpResponseRedirect('/login')


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/login')


class ReporteCreateView(LoginRequiredMixin, CreateView):
    model = Reporte
<<<<<<< HEAD
    fields = ['titulo', 'descripcion', 'foto', 'ciudad', 'ubicacion', 'tags']
=======
    fields = ['titulo', 'descripcion', 'foto', 'ciudad', 'ubicacion']

>>>>>>> agregados formato
    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)


@login_required
def editProfile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            if form.has_changed():
                messages.success(request, "Perfil editado exitosamente")
            return redirect("home")
    else:
        form = EditProfileForm(instance=request.user)
        return render(request, "sosafitosapp/edit_profile.html", {"form": form})


@user_passes_test(user_is_not_logged_in, login_url='/')
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
    return render(request, "sosafitosapp/user_register.html", {"form": form})


@login_required
def editPassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Contraseña editada exitosamente")
            return HttpResponseRedirect("/editProfile")
        else:
            messages.warning(request, "Error en la contraseña")
            return HttpResponseRedirect("/editPassword")
    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, "sosafitosapp/edit_password.html", {"form": form})


@login_required
def view_reporte(request, pk):
    reporte = Reporte.objects.get(id=pk)
    args = {'reporte' : reporte}
    if request.method == 'GET':
        return render(request, "sosafitosapp/reporte.html", args)


@login_required
def my_report(request):

    reportes = Reporte.objects.all()
    args = {'reportes' : reportes, 'titulo': "Mis reportes"}
    return render(request, "sosafitosapp/myreports.html", args)
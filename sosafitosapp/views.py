from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from taggit.models import Tag
from .forms import UserRegisterForm, EditProfileForm, CommentCreationForm, FilterForm
from sosafitosapp.models import Reporte, Comentario


def user_is_not_logged_in(user):
    return not user.is_authenticated


def home(request):
    if request.method == 'GET':
        return render(request, "sosafitosapp/home.html")


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
            return HttpResponseRedirect('/home')
        else:
            messages.warning(request, 'Usuario o contraseña incorrectos')
            return HttpResponseRedirect('/login')


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/home')


def reporteHomeView(request, state=0):
    reportes = Reporte.objects.all().order_by("-fecha")
    page_number = request.GET.get('page')
    if state == 0:
        request.session['type'] = 0

    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            page_number = 1
            request.session['type'] = form.cleaned_data["filter_type"]
            request.session['filter_data'] = form.cleaned_data["filter_content"]

    if request.session['type'] == "1":
        reportes = Reporte.objects.all().order_by("-fecha").filter(ciudad=request.session['filter_data'])
    elif request.session['type'] == "2":
        reportes = Reporte.objects.all().order_by("-fecha").filter(tags__name=request.session['filter_data'])

    paginator = Paginator(reportes, 5)
    page_obj = paginator.get_page(page_number)
    context = {
        "reportes": reportes,
        "form": FilterForm,
        'page_obj': page_obj
    }
    return render(request, "sosafitosapp/home.html", context)


class ReporteCreateView(LoginRequiredMixin, CreateView):
    model = Reporte
    fields = ['titulo', 'descripcion', 'foto', 'ciudad', 'ubicacion', 'tags']

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)


class ReporteUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Reporte
    fields = ['titulo', 'descripcion', 'foto', 'ciudad', 'ubicacion', 'tags']
    success_url = '/my_report'

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def test_func(self):
        report = self.get_object()
        return self.request.user == report.autor


@login_required
def editProfile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            if form.has_changed():
                messages.success(request, "Perfil editado exitosamente")
            return HttpResponseRedirect('/home')
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
            return HttpResponseRedirect('/home')
        
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


def view_reporte(request, pk):
    reporte = Reporte.objects.get(id=pk)
    if request.method == 'POST':
        form = CommentCreationForm(request.POST)
        if form.is_valid():
            form.instance.autor = request.user
            form.instance.reporte_padre = reporte
            form.save()
    form = CommentCreationForm()
    comentarios = Comentario.objects.filter(reporte_padre=reporte)
    args = {'reporte': reporte, 'form': form, 'comentarios': comentarios}
    return render(request, "sosafitosapp/reporte.html", args)


class MyReporteListView(LoginRequiredMixin, ListView):
    model = Reporte
    template_name = 'sosafitosapp/myreports.html'
    context_object_name = 'reportes'
    paginate_by = 3

    def get_queryset(self):
        return Reporte.objects.filter(autor=self.request.user).order_by('-fecha')

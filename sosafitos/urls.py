"""sosafitos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from sosafitosapp import views
from sosafitosapp.views import ReporteCreateView, ReporteUpdateView, ReporteListView, MyReporteListView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.reporteHomeView, name='home'),
    path('reporte/new/', ReporteCreateView.as_view(), name='reportCreate'),
    path('home/', ReporteListView.as_view(), name = 'home-'),
    path('login/', views.login_user, name='login'),
    path('editProfile/', views.editProfile, name='edit'),
    path('logout/', views.logout_user, name='logout'),
    path('registerUser/', views.register, name='registerUser'),
    path('editPassword/', views.editPassword, name='editPassword'),
    re_path(r'view_reporte/(?P<pk>\d+)/$', views.view_reporte, name='view_reporte'),
    path('my_report/', MyReporteListView.as_view(), name='myreport'),
    path('reporte/<int:pk>/update/', ReporteUpdateView.as_view(), name='reportEdit')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
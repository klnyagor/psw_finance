from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from perfil.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('perfil/', include('perfil.urls')),
    path('extrato/', include('extrato.urls')),
    path('planejamento/', include('planejamento.urls')),
    path('contas/', include('contas.urls')),
    path('', home, name="home")

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('coordenador_curso.urls')),
    path('usuarios/', include('usuario.urls')),
    path('professores/', include('professores.urls')),
    path('admin/', admin.site.urls),
]

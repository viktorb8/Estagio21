from django.contrib import admin

from .models import Professores

class Listando_Professores(admin.ModelAdmin):
    list_display = ('nome_completo', 'email')
    list_display_links = ('nome_completo',)
    search_fields = ('nome_completo',)
    list_per_page = 10

admin.site.register(Professores, Listando_Professores)
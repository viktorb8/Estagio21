from django.contrib import admin

from .models import Projeto, Colaboradores, Bolsas, Bolsistas


class Listando_Projetos(admin.ModelAdmin):
    list_display = ('id', 'nome_projeto', 'portaria_projeto','coordenador_projeto')
    list_display_links = ('id', 'nome_projeto')
    search_fields = ('nome_projeto','coordenador_projeto',)
    list_filter = ('coordenador_projeto','portaria_projeto',)
    list_per_page = 10


class BolsistaInline(admin.StackedInline):
    model = Bolsistas


class BolsaAdm(admin.ModelAdmin):
    inlines = [
        BolsistaInline,
    ]


admin.site.site_header = 'Adminstrador Projetos UNEMAT'
admin.site.register(Projeto, Listando_Projetos)
admin.site.register(Colaboradores)
admin.site.register(Bolsas, BolsaAdm)
admin.site.register(Bolsistas)



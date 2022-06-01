from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lista_projetos', views.lista_projetos, name='lista_projetos'),
    path('usuario_bolsista/<int:bolsa_id>/<int:projeto_id>', views.usuario_bolsista, name='usuario_bolsista'),
    path('projeto/<int:projeto_id>', views.projeto, name='projeto'),
    path('projeto/<int:projeto_id>/relarorios', views.relatorios, name='relatorios'),
    path('projeto/relatorio_bolsas', views.relatorio_bolsas, name='relatorio_bolsas'),
    path('projeto/<int:projeto_id>/bolsas', views.bolsas, name='bolsas'),
    path('projeto/<int:projeto_id>/cadastrar_bolsa', views.cadastrar_bolsa, name='cadastrar_bolsa'),
    path('projeto/<int:bolsa>/<int:id>/cadastrar_bolsista', views.cadastrar_bolsista, name='cadastrar_bolsista'),
    path('projeto/<int:bolsa>/<int:id>/deletar_bolsa', views.deletar_bolsa, name='deletar_bolsa'),
    path('projeto/<str:relatorio>/<int:id>/deletar_relatorio', views.deletar_relatorio, name='deletar_relatorio'),
    path('projeto/<str:bolsa_criada>/<int:bolsista_id>/<int:id>/deletar_bolsista', views.deletar_bolsista, name='deletar_bolsista'),
    path('buscar', views.buscar, name='buscar'),
    path('pdf_view/projeto_<int:pdf_id>.pdf', views.ViewPDF, name="pdf_view"),
    path('cadastrar_projeto', views.cadastrar_projeto, name='cadastrar_projeto'),
    path('editar_projeto/<int:projeto_id>', views.editar_projeto, name='editar_projeto'),
    path('deletar_projeto/<int:projeto_id>', views.deletar_projeto, name='deletar_projeto'),
    path('deletar_colaborador/<str:colaborador>/<int:id>', views.deletar_colaborador, name='deletar_colaborador')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

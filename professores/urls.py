from django.urls import path

from . import views

urlpatterns = [
    path('cadastrar_professor', views.cadastrar_professor, name='cadastrar_professor'),
    path('montar_lista', views.montar_lista, name='montar_lista'),
    path('lista_professores', views.lista_professores, name='lista_professores'),
    path('deletar_professor/<int:professor_id>', views.deletar_professor, name='deletar_professor'),
    path('deletar/<int:professor_id>', views.deletar, name='deletar'),
    path('excluir/<int:projeto_id>', views.excluir, name='excluir'),
]
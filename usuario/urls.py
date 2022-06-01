from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('cadastro', views.cadastro, name='cadastro'),
    path('login', views.login, name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('logout', views.logout, name='logout'),
    path('lista', views.lista, name='lista'),
    path('editar/<str:username>', views.editar, name='editar'),
    path('deletar_usuario/<int:user_id>', views.deletar_usuario, name='deletar_usuario'),
    path('administrativo/editar_usuario', views.editar_usuario, name='editar_usuario'),
    path('administrativo/alterar_senha', views.alterar_senha, name='alterar_senha'),
    path('administrativo', views.administrativo, name='administrativo'),
    #alterar senha
    path('recuperar_senha', auth_views.PasswordResetView.as_view(template_name="usuarios/recuperar_senha.html"), name="reset_password"),
    path('nova_senha_enviada', auth_views.PasswordResetDoneView.as_view(template_name="usuarios/email_enviado.html"), name="password_reset_done"),
    path('senha/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="usuarios/nova_senha.html"), name="password_reset_confirm"),
    path('senha_recuperada', auth_views.PasswordResetCompleteView.as_view(template_name="usuarios/senha_alterada.html"), name="password_reset_complete"),
]

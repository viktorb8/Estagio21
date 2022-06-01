from django.contrib.auth.models import User


def email_existe(email, lista_erros):
    if not User.objects.filter(email=email).exists():
        lista_erros['email'] = 'Usuário inválido!'


def verifica_email(email, lista_erros):
    existe = User.objects.filter(email=email).exists()
    if existe:
        lista_erros['email'] = 'Email já cadastrado!'


def verifica_senha(senha1, senha2, lista_erros):
    if senha1 != senha2:
        lista_erros['password1'] = 'Senhas são diferentes!'

from professores.models import Professores


def verifica_email(email, lista_erros):
    existe = Professores.objects.filter(email=email).exists()

    if existe:
        lista_erros['email'] = 'Email já cadastrado!'

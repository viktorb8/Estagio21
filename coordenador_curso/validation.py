from django.contrib.auth.models import User

from coordenador_curso.models import Projeto, Bolsistas, Bolsas


def datas_iguais(data_de_inicio, data_de_fim, lista_erros):
    if data_de_inicio == data_de_fim:
        lista_erros['data_de_fim'] = 'A data de término não pode ser igual a data de início!'


def data_menor(data_de_inicio, data_de_fim, lista_erros):
    if data_de_inicio > data_de_fim:
        lista_erros['data_de_fim'] = 'A data de término não pode ser menor que a data de início!'


def prazo_maior(data_de_fim, fim_projeto, lista_erros):
    if data_de_fim > fim_projeto:
        lista_erros['data_de_fim'] = 'A bolsa não pode se encerrar após o fim do projeto!'


def prazo_menor(data_de_inicio, inicio_projeto, lista_erros):
    if inicio_projeto > data_de_inicio:
        lista_erros['data_de_inicio'] = 'A bolsa não pode iniciar antes do inicio do projeto!'


def portaria_existe(portaria_projeto, lista_erros):
    existe = Projeto.objects.filter(portaria_projeto=portaria_projeto).exists()

    if existe:
        lista_erros['portaria_projeto'] = 'Portaria já registrada!'


def email_cadastrado(email, id_bolsa, id, lista_erros):
    existe = User.objects.filter(email=email).exists()
    if existe:
        consta = Bolsistas.objects.filter(email=email).exists()
        if consta:
            bolsista = Bolsistas.objects.filter(email=email).first()
            if bolsista.bolsa_id == id_bolsa:
                if id is None:
                    lista_erros['email'] = 'Email já cadastrado no sistema!'
                return 0
            elif id is None:
                lista_erros['email'] = 'Email já cadastrado no sistema!'


def bolsa_existe(orgao_remunerador, id_projeto, id, lista_erros):
    existe = Bolsas.objects.filter(orgao_remunerador=orgao_remunerador).filter(projeto_id=id_projeto).exists()
    if existe:
        if id_projeto == id:
            if id is None:
                lista_erros['orgao_remunerador'] = 'Bolsa já cadastrada!'
            return 0
        elif id is None:
            lista_erros['orgao_remunerador'] = 'Bolsa já cadastrada!'
    else:
        return 0
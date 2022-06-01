from django.db import models

from professores.models import Professores


class Projeto(models.Model):

    acoes = (
        ('', "---------"),
        ('Projeto', "Projeto"),
        ('Evento', "Evento"),
        ('Curso', "Curso"),
    )

    areas = (
        ('', "---------"),
        ('Comunicação', 'Comunicação'),
        ('Cultura', 'Cultura'),
        ('Direitos Humanos e Justiça','Direitos Humanos e Justiça'),
        ('Educação', 'Educação'),
        ('Meio Ambiente', 'Meio Ambiente'),
        ('Saúde', 'Saúde'),
        ('Tecnologia e Produção', 'Tecnologia e Produção'),
        ('Trabalho', 'Trabalho'),
    )


    nome_projeto = models.CharField('Nome do Projeto', max_length=200)
    portaria_projeto = models.PositiveIntegerField('Nº da Portaria')
    data_de_inicio = models.DateField('Data de Inicio')
    data_de_fim = models.DateField('Data de Termino')
    objetivo_projeto = models.TextField('Objetivo do Projeto', max_length=800)
    area_projeto = models.CharField('Área do Projeto', max_length=30, choices=areas, blank=False)
    coordenador_projeto = models.ForeignKey(Professores, on_delete=models.CASCADE)
    url_projeto = models.URLField('URL do Projeto')
    tipos_de_acoes = models.CharField('Tipos de Ações', max_length=10, choices=acoes, blank=False)
    financiador = models.CharField('Financiador', max_length=30, null=True)
    valor_financiado = models.CharField('Valor Financiado', max_length=30)
    edital_financiado = models.CharField('Edital do Financiamento', max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nome_projeto


class Relatorios(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='relatorio')
    relatorio = models.FileField('Relatório', blank=True)


class Colaboradores(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='colaboradores')
    colaborador_projeto = models.CharField(max_length=200, blank=True)
    lattes = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.colaborador_projeto


class Bolsas(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='bolsas')
    orgao_remunerador = models.CharField(max_length=50, blank=True)
    tipo_bolsa = models.CharField('Tipo de bolsa', max_length=50, blank=True, null=True)
    portaria_bolsa = models.PositiveIntegerField('Nº da Portaria', blank=True, null=True)
    data_de_inicio = models.DateField('Data de Início', blank=True, null=True)
    data_de_fim = models.DateField('Data de Término', blank=True, null=True)

    def __str__(self):
        return self.orgao_remunerador


class Bolsistas(models.Model):
    bolsa = models.ForeignKey(Bolsas, on_delete=models.CASCADE, related_name='bolsistas')
    bolsista = models.CharField('Nome', max_length=200, blank=True)
    email = models.EmailField(max_length=200, blank=True)

    def __str__(self):
        return self.bolsista


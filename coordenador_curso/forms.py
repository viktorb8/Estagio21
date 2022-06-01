from django import forms
from .models import Projeto, Professores, Colaboradores, Bolsas, Bolsistas, Relatorios
from .validation import datas_iguais, data_menor, portaria_existe, prazo_maior, prazo_menor, email_cadastrado, \
    bolsa_existe


class PostForm(forms.ModelForm):
    format_key = 'DATE_INPUT_FORMATS'

    class Meta:
        model = Projeto
        fields = '__all__'

    nome_projeto = forms.CharField(label='Nome do Projeto:', required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control col-8',
            'maxlength': '200',
        }
    ))

    portaria_projeto = forms.IntegerField(label='Nº da Portaria:', required=True, widget=forms.NumberInput(
        attrs={
            'type': 'number',
            'class': 'form-control col-4'
        }
    ))

    data_de_inicio = forms.DateField(label='Data de Inicio:', required=True, widget=forms.DateInput(
        attrs={
            'type': 'date',
            'date-input': 'date',
            'class': 'form-control col-4',
            'format': '%d-%m-%Y',
            'value': '{{data_de_inicio|date:"d-m-Y"}}'
        }
    ))

    data_de_fim = forms.DateField(label='Data de Término:', required=True, widget=forms.DateInput(
        attrs={
            'type': 'date',
            'class': 'form-control col-4',
            'format': '%d-%m-%Y'
        }
    ))

    objetivo_projeto = forms.CharField(label='Objetivos do Projeto:', required=True, widget=forms.Textarea(
        attrs={
            'type': 'text',
            'class': 'form-control col-8',
            'maxlength': '800'
        }
    ))

    area_projeto = forms.ChoiceField(label='Área do Projeto:', choices=Projeto.areas, required=True,
                                     widget=forms.Select(
                                         attrs={
                                             'class': 'form-control col-8',
                                             'name': 'area'
                                         }
                                     ))

    coordenador_projeto = forms.ModelChoiceField(label='Coordenador do Projeto:', required=True,
                                                 queryset=Professores.objects.all().order_by('id'), widget=forms.Select(
            attrs={
                'class': 'form-control col-8',
                'name': 'mytext[]'
            }
        ))

    url_projeto = forms.CharField(label='URL do Projeto', required=True, widget=forms.URLInput(
        attrs={
            'type': 'url',
            'class': 'form-control col-8',
            'maxlenght': '200'
        }
    ))

    tipos_de_acoes = forms.ChoiceField(label='Área do Projeto:', choices=Projeto.acoes, required=True,
                                       widget=forms.Select(
                                           attrs={
                                               'class': 'form-control col-8',
                                               'name': 'acoes',
                                           }
                                       ))

    relatorio_inicial = forms.FileField(label='Relatório Inicial', required=False)

    financiador = forms.CharField(label='Financiador:', required=False, widget=forms.TextInput(
        attrs={
            'class': 'form-control col-8',
            'maxlength': '30',
        }
    ))

    edital_financiado = forms.CharField(label='Edital Financiado:', required=False, widget=forms.TextInput(
        attrs={
            'class': 'form-control col-8',
            'maxlength': '20',
        }
    ))

    valor_financiado = forms.CharField(label='Valor:', required=False, widget=forms.TextInput(
        attrs={
            'class': 'form-control col-4',
            'maxlength': '20',
            'type': 'text',
            'pattern': "^\$\d{1,3}(.\d{3})*(\,\d+)?$",
            'data-type': "currency",
            'placeholder': "R$ 1.000.000,00",
        }
    ))

    def clean(self):
        data_de_inicio = self.cleaned_data.get('data_de_inicio')
        data_de_fim = self.cleaned_data.get('data_de_fim')
        portaria_projeto = self.cleaned_data.get('portaria_projeto')

        lista_erros = {}

        datas_iguais(data_de_inicio, data_de_fim, lista_erros)
        data_menor(data_de_inicio, data_de_fim, lista_erros)
        portaria_existe(portaria_projeto, lista_erros)

        if lista_erros is not None:
            for erro in lista_erros:
                mensagem_erro = lista_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data


class EditForm(forms.ModelForm):
    format_key = 'DATE_INPUT_FORMATS'

    class Meta:
        model = Projeto
        fields = '__all__'

    nome_projeto = forms.CharField(label='Nome do Projeto:', required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control col-8',
            'maxlength': '200',
        }
    ))

    portaria_projeto = forms.IntegerField(label='Nº da Portaria:', required=True, widget=forms.NumberInput(
        attrs={
            'type': 'number',
            'class': 'form-control col-4'
        }
    ))

    data_de_inicio = forms.DateField(label='Data de Inicio:', required=True, widget=forms.DateInput(
        attrs={
            'type': 'date',
            'date-input': 'date',
            'class': 'form-control col-4',
            'format': '%d-%m-%Y',
            'value': '{{data_de_inicio|date:"d-m-Y"}}'
        }
    ))

    data_de_fim = forms.DateField(label='Data de Término:', required=True, widget=forms.DateInput(
        attrs={
            'type': 'date',
            'class': 'form-control col-4',
            'format': '%d-%m-%Y'
        }
    ))

    objetivo_projeto = forms.CharField(label='Objetivos do Projeto:', required=True, widget=forms.Textarea(
        attrs={
            'type': 'text',
            'class': 'form-control col-8',
            'maxlength': '800'
        }
    ))

    area_projeto = forms.ChoiceField(label='Área do Projeto:', choices=Projeto.areas, required=True,
                                     widget=forms.Select(
                                         attrs={
                                             'class': 'form-control col-8',
                                             'name': 'area'
                                         }
                                     ))



    coordenador_projeto = forms.ModelChoiceField(label='Coordenador do Projeto:', required=True,
                                                 queryset=Professores.objects.all().order_by('id'), widget=forms.Select(
            attrs={
                'class': 'form-control col-8',
            }
        ))

    url_projeto = forms.CharField(label='URL do Projeto', required=True, widget=forms.URLInput(
        attrs={
            'type': 'url',
            'class': 'form-control col-8',
            'maxlenght': '200'
        }
    ))

    tipos_de_acoes = forms.ChoiceField(label='Área do Projeto:', choices=Projeto.acoes, required=True,
                                       widget=forms.Select(
                                           attrs={
                                               'class': 'form-control col-8',
                                               'name': 'acoes',
                                           }
                                       ))

    financiador = forms.CharField(label='Financiador:', required=False, widget=forms.TextInput(
        attrs={
            'class': 'form-control col-8',
            'maxlength': '30',
        }
    ))

    edital_financiado = forms.CharField(label='Edital Financiado:', required=False, widget=forms.TextInput(
        attrs={
            'class': 'form-control col-8',
            'maxlength': '20',
        }
    ))

    valor_financiado = forms.CharField(label='Valor:', required=False, widget=forms.TextInput(
        attrs={
            'class': 'form-control col-4',
            'maxlength': '20',
            'type': 'text',
            'pattern': "^\$\d{1,3}(.\d{3})*(\,\d+)?$",
            'data-type': "currency",
            'placeholder': "R$ 1.000.000,00",
        }
    ))

    def clean(self):
        data_de_inicio = self.cleaned_data.get('data_de_inicio')
        data_de_fim = self.cleaned_data.get('data_de_fim')

        lista_erros = {}

        datas_iguais(data_de_inicio, data_de_fim, lista_erros)
        data_menor(data_de_inicio, data_de_fim, lista_erros)

        if lista_erros is not None:
            for erro in lista_erros:
                mensagem_erro = lista_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data


class RelatorioForm(forms.ModelForm):
    class Meta:
        model = Relatorios
        fields = '__all__'

    relatorio = forms.FileField(label='Relatório', required=False, widget=forms.FileInput(
        attrs={
            'class': 'form-control'
        }
    ))


class ColabForm(forms.ModelForm):
    class Meta:
        model = Colaboradores
        fields = '__all__'

    colaborador_projeto = forms.CharField(label="Colaborador do Projeto", widget=forms.TextInput(
        attrs={
            'class': 'form-control col-8',
            'maxlength': '200',
        }
    ))

    lattes = forms.CharField(label='Lattes', required=True, widget=forms.URLInput(
        attrs={
            'type': 'url',
            'class': 'form-control col-7',
            'maxlenght': '200'
        }
    ))


class BolsistaForm(forms.ModelForm):
    class Meta:
        model = Bolsistas
        fields = '__all__'

    bolsista = forms.CharField(label="Bolsista do Projeto", widget=forms.TextInput(
        attrs={
            'class': 'form-control col-7',
            'maxlength': '200',
        }
    ))

    email = forms.EmailField(label='E-mail', required=True, widget=forms.EmailInput(
        attrs={
            'class': 'form-control col-7',
            'maxlength': '200',
            'placeholder': "Ex.: jose@unemat.br",
            'name': 'email'
        }
    ))

    def clean(self):
        id = self.cleaned_data.get('id')
        bolsa = self.cleaned_data.get('bolsa')
        email = self.cleaned_data.get('email')

        id_bolsa = bolsa.id

        lista_erros = {}

        email_cadastrado(email, id_bolsa, id, lista_erros)

        if lista_erros is not None:
            for erro in lista_erros:
                mensagem_erro = lista_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data


class BolsaForm(forms.ModelForm):
    class Meta:
        model = Bolsas
        fields = '__all__'

    orgao_remunerador = forms.CharField(label="Qual o orgão remunerador?", required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control col-8',
            'maxlength': '200',
        }
    ))

    tipo_bolsa = forms.CharField(label="Qual o tipo da bolsa?", required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control col-8',
            'maxlength': '200',
        }
    ))

    portaria_bolsa = forms.IntegerField(label='Nº da Portaria:', required=True, widget=forms.NumberInput(
        attrs={
            'type': 'number',
            'class': 'form-control col-4'
        }
    ))

    data_de_inicio = forms.DateField(label='Data de Inicio:', required=True, widget=forms.DateInput(
        attrs={
            'type': 'date',
            'date-input': 'date',
            'class': 'form-control col-4',
            'format': '%d-%m-%Y',
            'value': '{{data_de_inicio|date:"d-m-Y"}}'
        }
    ))

    data_de_fim = forms.DateField(label='Data de Término:', required=True, widget=forms.DateInput(
        attrs={
            'type': 'date',
            'class': 'form-control col-4',
            'format': '%d-%m-%Y'
        }
    ))

    def clean(self):
        projeto = self.cleaned_data.get('projeto')
        id = self.cleaned_data.get('id')
        data_de_inicio = self.cleaned_data.get('data_de_inicio')
        data_de_fim = self.cleaned_data.get('data_de_fim')
        orgao_remunerador = self.cleaned_data.get('orgao_remunerador')

        inicio_projeto = projeto.data_de_inicio
        fim_projeto = projeto.data_de_fim
        id_projeto = projeto.id

        lista_erros = {}

        datas_iguais(data_de_inicio, data_de_fim, lista_erros)
        data_menor(data_de_inicio, data_de_fim, lista_erros)
        prazo_maior(data_de_fim, fim_projeto, lista_erros)
        prazo_menor(data_de_inicio, inicio_projeto, lista_erros)
        bolsa_existe(orgao_remunerador, id_projeto, id, lista_erros)

        if lista_erros is not None:
            for erro in lista_erros:
                mensagem_erro = lista_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data

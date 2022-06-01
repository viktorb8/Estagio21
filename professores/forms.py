from django import forms
from .models import Professores
from .validation import verifica_email


class ProfForm(forms.ModelForm):
    class Meta:
        model = Professores
        fields = '__all__'

    nome_professor = forms.CharField(label='Nome', required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'maxlength': '200',
            'placeholder': "Ex.: José",
            'name': 'nome'
        }
    ))

    sobrenome_professor = forms.CharField(label='Sobrenome', required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'maxlength': '200',
            'placeholder': "Ex.: da Silva",
            'name': 'sobrenome'
        }
    ))

    email = forms.EmailField(label='E-mail', required=True, widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'maxlength': '200',
            'placeholder': "Ex.: jose@unemat.br",
            'name': 'email'
        }
    ))

    senha = forms.CharField(label='Senha', required=True, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': "Digite sua senha",
            'name': 'senha'
        }
    ))



    def clean(self):
        email = self.cleaned_data.get('email')

        lista_erros = {}

        verifica_email(email, lista_erros)

        if lista_erros is not None:
            for erro in lista_erros:
                mensagem_erro = lista_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data


class EditaProf(forms.ModelForm):
    class Meta:
        model = Professores
        fields = '__all__'

    nome_professor = forms.CharField(label='Nome', required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'maxlength': '200',
            'placeholder': "Ex.: José",
            'name': 'nome'
        }
    ))

    sobrenome_professor = forms.CharField(label='Sobrenome', required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'maxlength': '200',
            'placeholder': "Ex.: da Silva",
            'name': 'sobrenome'
        }
    ))

    email = forms.EmailField(label='E-mail', required=True, widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'maxlength': '200',
            'placeholder': "Ex.: jose@unemat.br",
            'name': 'email'
        }
    ))
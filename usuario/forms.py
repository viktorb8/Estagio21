from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserChangeForm

from usuario.validation import verifica_email, verifica_senha, email_existe


class Login(forms.Form):
    email = forms.EmailField(label='Email: ', max_length=200, widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'maxlength': '200',
            'placeholder': "Entre com o email cadastrado",
            'name': 'email'
        }
    ))

    senha = forms.CharField(label='Senha: ', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': "Digite aqui sua senha",
            'name': 'senha1'
        }
    ))

    def clean(self):
        email = self.cleaned_data.get('email')

        lista_erros = {}

        email_existe(email, lista_erros)

        if lista_erros is not None:
            for erro in lista_erros:
                mensagem_erro = lista_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data


class UserCreationForm(forms.Form):
    first_name = forms.CharField(label='Nome', max_length=20, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'maxlength': '200',
            'placeholder': "Ex.: José",
            'name': 'nome'
        }
    ))

    last_name = forms.CharField(label='Sobrenome', max_length=150, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'maxlength': '200',
            'placeholder': "Ex.: da Silva",
            'name': 'sobrenome'
        }
    ))

    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)

    email = forms.EmailField(label='Email', max_length=200, widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'maxlength': '200',
            'placeholder': "Ex.: jose@unemat.br",
            'name': 'email'
        }
    ))

    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': "Digite sua senha",
            'name': 'senha1'
        }
    ))

    password2 = forms.CharField(label='Confirmação', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': "Confirme sua senha",
            'name': 'senha2'
        }
    ))

    def clean(self):
        email = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        lista_erros = {}

        verifica_email(email, lista_erros)
        verifica_senha(password1, password2, lista_erros)

        if lista_erros is not None:
            for erro in lista_erros:
                mensagem_erro = lista_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data

    def save(self, commit=True):
        user = User.objects.create_user(
            is_staff=True,
            username=self.cleaned_data['username'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1']
        )
        return user


class EditarUsuarioForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',

        )

    first_name = forms.CharField(label='Nome: ', max_length=20, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'maxlength': '200',
            'placeholder': "Ex.: José",
            'name': 'nome'
        }
    ))

    last_name = forms.CharField(label='Sobrenome: ', max_length=150, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'maxlength': '200',
            'placeholder': "Ex.: da Silva",
            'name': 'sobrenome'
        }
    ))

    email = forms.EmailField(label='E-mail: ', max_length=200, widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'maxlength': '200',
            'placeholder': "Ex.: jose@unemat.br",
            'name': 'email'
        }
    ))


class FormErro(forms.Form):

    email = forms.EmailField()

    def clean(self):
        lista_erros = {}

        if lista_erros is not None:
            for erro in lista_erros:
                mensagem_erro = lista_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data

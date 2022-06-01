from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
import datetime
from coordenador_curso.models import Projeto, Bolsistas
from professores.forms import EditaProf
from professores.models import Professores
from usuario.forms import UserCreationForm, EditarUsuarioForm, FormErro, Login
from django.contrib.auth.forms import PasswordChangeForm


def cadastro(request):
    if request.method == 'GET':

        user = UserCreationForm()
        context = {
            'new_user': user
        }
        return render(request, 'usuarios/cadastro.html', context)

    elif request.method == 'POST':

        user = UserCreationForm(request.POST)
        str_nome = request.POST.get('first_name')
        str_sobrenome = request.POST.get('last_name')

        nome = ''.join(str_nome.split())
        sobrenome = ''.join(str_sobrenome.split())

        str_user = nome + sobrenome

        user_size = len(str_user)

        if user_size > 10:
            user_name = ''
            for i in range(0, 9):
                user_name += str_user[i].lower()
        else:
            user_name = str_user

        if User.objects.filter(username=user_name).exists():
            user_name = user_name[:-1]
            new = 1
            user_name += str(new)
            while User.objects.filter(username=user_name).exists():
                if User.objects.filter(username=user_name).exists():
                    user_name = user_name[:-1]
                    new += 1
                    user_name += str(new)
                else:
                    user_name += str(new)
                    break

        request.POST._mutable = True
        request.POST['username'] = user_name
        request.POST._mutable = False

        if user.is_valid():
            user.is_staff = True
            user.save()
            return redirect('lista')
        else:
            context = {
                'new_user': user
            }
            return render(request, 'usuarios/cadastro.html', context)


def editar(request, username):
    if request.method == 'GET':
        usuario = User.objects.get(username=username)
        form = EditarUsuarioForm(instance=usuario)
        context = {
            'form': form,
            'user': usuario,
        }
        return render(request, 'usuarios/editar.html', context)

    if request.method == 'POST':
        usuario = User.objects.get(username=username)
        form = EditarUsuarioForm(request.POST, instance=usuario)

        email_user = usuario.email
        email = request.POST.get('email')

        if email_user != email:
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'Email já cadastrado!')

        if form.is_valid():
            form.save()
            return redirect('lista')
        else:
            context = {
                'form': form,
            }
            return render(request, 'usuarios/editar.html', context)


def login(request):
    if request.method == 'GET':
        form = Login()
        context = {
            'form': form
        }
        return render(request, 'usuarios/login.html', context)
    if request.method == 'POST':
        form = Login(request.POST)
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if User.objects.filter(email=email):
            user = User.objects.filter(email=email).get()
            valido = user.check_password(senha)
            if not valido:
                form.add_error('senha', 'Senha incorreta!')

        if form.is_valid():
            if User.objects.filter(email=email).exists():
                nome = User.objects.filter(email=email).values_list('username', flat=True).get()
                user = auth.authenticate(request, username=nome, password=senha)
                if user is not None:
                    auth.login(request, user)
                    return redirect('dashboard')
        context = {
            'form': form
        }
        return render(request, 'usuarios/login.html', context)


def logout(request):
    auth.logout(request)
    return redirect('login')


def dashboard(request):
    if request.user.is_authenticated:

        projetos = Projeto.objects.order_by('id')

        hoje = datetime.datetime.now().date()
        delta = datetime.timedelta(days=90)
        prox_mes = hoje+delta

        projetos = projetos.filter(data_de_fim__gte=hoje, data_de_fim__lte=prox_mes).order_by('data_de_fim')

        context = {
            'projetos': projetos
        }

        return render(request, 'usuarios/dashboard.html', context)
    else:
        return redirect('index')


def deletar_usuario(request, user_id):
    usuario = User.objects.get(id=user_id)
    usuario.delete()
    return redirect('lista')


def lista(request):
    usuarios = User.objects.order_by('id').filter(is_superuser=False)
    for usuario in usuarios:
        existe = Bolsistas.objects.filter(email=usuario.email).exists()
        if existe:
            usuarios = usuarios.exclude(email=usuario.email)
    page = request.GET.get('page', 1)
    paginator = Paginator(usuarios, 10)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    context = {'usuarios': users}

    return render(request, 'usuarios/lista.html', context)


def alterar_senha(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('logout')
        else:
            context = {
                'form': form
            }
            return render(request, 'usuarios/password_change_form.html', context)

    else:
        form = PasswordChangeForm(user=request.user)
        context = {
            'form': form
        }
        return render(request, 'usuarios/password_change_form.html', context)


def editar_usuario(request):
    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, instance=request.user)

        email_user = request.user.email
        email = request.POST.get('email')

        if email_user != email:
            if User.objects.filter(email=email).exists():
                erro = FormErro(request.POST)
                request.POST._mutable = True
                request.POST['email'] = email
                request.POST._mutable = False
                erro.add_error('email', 'Email já cadastrado!')
                form.add_error('email', 'Já cadastrado')

        if request.user.is_superuser:
            professor = Professores.objects.get(email=request.user.email)
            form_prof = EditaProf(request.POST, instance=professor)

            str_nome = request.POST.get('first_name')
            str_sobrenome = request.POST.get('last_name')
            email = request.POST.get('email')
            nome_completo = str_nome + ' ' + str_sobrenome

            request.POST._mutable = True
            request.POST['nome_professor'] = str_nome
            request.POST['sobrenome_professor'] = str_sobrenome
            request.POST['email'] = email
            request.POST['nome_completo'] = nome_completo
            request.POST._mutable = False

            if email_user != email:
                if User.objects.filter(email=email).exists():
                    erro = FormErro(request.POST)
                    request.POST._mutable = True
                    request.POST['email'] = email
                    request.POST._mutable = False
                    erro.add_error('email', 'Email já cadastrado!')
                    form.add_error('email', 'Já cadastrado')
            else:
                form_prof.save()

        if form.is_valid():
            form.save()
            context = {
                'form': form,
            }
            return render(request, 'usuarios/administrativo/editado.html', context)

        else:
            form = EditarUsuarioForm(instance=request.user)
            context = {
                'form': form,
                'erro': erro,
            }
            return render(request, 'usuarios/administrativo/editar_usuario.html', context)

    else:
        form = EditarUsuarioForm(instance=request.user)
        context = {'form': form}
        return render(request, 'usuarios/administrativo/editar_usuario.html', context)


def administrativo(request):
    return render(request, 'usuarios/administrativo.html')




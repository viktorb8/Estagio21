from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from coordenador_curso.models import Projeto
from professores.forms import ProfForm
from professores.models import Professores


def cadastrar_professor(request):
    if request.method == 'POST':
        form = ProfForm(request.POST)

        str_nome = request.POST.get('nome_professor')
        str_sobrenome = request.POST.get('sobrenome_professor')
        email = request.POST.get('email')
        senha1 = request.POST.get('senha')
        senha2 = request.POST['senha2']

        nome = ''.join(str_nome.split())
        sobrenome = ''.join(str_sobrenome.split())

        nome_completo = str_nome + ' ' + str_sobrenome
        request.POST._mutable = True
        request.POST['nome_completo'] = nome_completo
        request.POST._mutable = False

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

        if senha1 != senha2:
            form.add_error('senha', 'Senhas são diferentes!')

        if form.is_valid():
            user = User.objects.create_user(username=user_name, first_name=nome, last_name=sobrenome, email=email, password=senha1)
            user.is_staff = True
            user.is_superuser = True
            form.save()
            user.save()
            return redirect('lista_professores')
        else:
            context = {
                'prof_form': form,
            }
            return render(request, 'professores/cadastrar_professor.html', context)

    form = ProfForm()

    context = {
        'prof_form': form,
    }
    return render(request, 'professores/cadastrar_professor.html', context)


def montar_lista(request):
    professores = Professores.objects.order_by('id')
    page = request.GET.get('page', 1)
    paginator = Paginator(professores, 10)

    try:
        profs = paginator.page(page)
    except PageNotAnInteger:
        profs = paginator.page(1)
    except EmptyPage:
        profs = paginator.page(paginator.num_pages)

    return profs


def lista_professores(request):
    lista = montar_lista(request)

    context = {
        'professores': lista,
    }

    return render(request, 'professores/lista_professores.html', context)


def deletar(request, professor_id):
    professor = Professores.objects.get(pk=professor_id)
    projetos = Projeto.objects.order_by('id')
    coordenador = professor.nome_professor
    projetos = projetos.filter(coordenador_projeto__nome_completo__icontains=coordenador)

    context = {
        'projetos': projetos,
        'prof': professor,
    }

    return render(request, 'professores/deletar.html', context)


def excluir(request, projeto_id):
    projeto = Projeto.objects.get(pk=projeto_id)
    prof_id = projeto.coordenador_projeto.id
    projeto.delete()
    return redirect('deletar', prof_id)


def deletar_professor(request, professor_id):
    professor = Professores.objects.get(pk=professor_id)
    email = professor.email
    usuario = User.objects.get(email=email)
    user = request.user.id

    if user == usuario.id:
        lista = montar_lista(request)

        context = {
            'professores': lista,
            'alert_flag': True,
        }

        return render(request, 'professores/lista_professores.html', context)
    else:
        projetos = Projeto.objects.order_by('id')
        coordenador = professor.nome_professor
        projetos = projetos.filter(coordenador_projeto__nome_completo__icontains=coordenador)
        if projetos:
            return redirect('deletar', professor_id)
        else:
            professor.delete()
            usuario.delete()
            return redirect('lista_professores')
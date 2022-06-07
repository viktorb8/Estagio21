from io import BytesIO

from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import get_template
from django.urls import reverse
from xhtml2pdf import pisa
from .models import Projeto, Colaboradores, Bolsas, Bolsistas, Relatorios
from .forms import PostForm, ColabForm, EditForm, BolsaForm, BolsistaForm, RelatorioForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    return render(request, 'index.html')


def cadastrar_projeto(request):
    if request.method == 'GET':
        form = PostForm()
        form_colab_factory = inlineformset_factory(Projeto, Colaboradores, form=ColabForm, extra=1)
        form_colab = form_colab_factory()

        context = {
            'form': form,
            'form_colab': form_colab,
        }
        return render(request, 'cadastrar_projeto.html', context)

    elif request.method == 'POST':

        form = PostForm(request.POST, request.FILES)
        form_colab_factory = inlineformset_factory(Projeto, Colaboradores, form=ColabForm, max_num=5)
        form_colab = form_colab_factory(request.POST)

        if form.is_valid() and form_colab.is_valid():
            projeto_salvo = form.save()
            form_colab.instance = projeto_salvo
            form_colab.save()
            form_id = projeto_salvo.id
            return redirect('projeto', form_id)
        else:
            context = {
                'form': form,
                'form_colab': form_colab,
            }
            return render(request, 'cadastrar_projeto.html', context)


def lista_projetos(request):
    if request.user.is_authenticated:
        email = request.user.email
        existe = Bolsistas.objects.filter(email=email).exists()
        if existe:
            id = set()
            bolsista = Bolsistas.objects.filter(email=email).first()
            bolsa_id = bolsista.bolsa_id
            bolsa = Bolsas.objects.filter(id=bolsa_id).first()
            id.add(bolsa.projeto_id)
            projetos = Projeto.objects.filter(id__in=id)
            logado = True
        else:
            projetos = Projeto.objects.order_by('id')
            logado = False
    else:
        projetos = Projeto.objects.order_by('id')
        logado = False

    projetos_unemat = projetos
    print(projetos_unemat)
    page = request.GET.get('page', 1)
    paginator = Paginator(projetos_unemat, 10)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    lista_acoes = Projeto.acoes
    lista_areas = Projeto.areas

    context = {
        'projetos': users,
        'acoes': lista_acoes,
        'areas': lista_areas,
        'logado': logado,
    }

    return render(request, 'lista_projetos.html', context)


def buscar(request):
    projetos = Projeto.objects.order_by('id')

    projeto = request.GET.get('projeto')
    coordenador = request.GET.get('coordenador')
    portaria = request.GET.get('portaria')
    acao = request.GET.get('acao')
    areas = request.GET.get('area')
    inicio = request.GET.get('inicio')
    termino = request.GET.get('termino')

    if projeto != '' and projeto is not None:
        projetos = projetos.filter(nome_projeto__icontains=projeto)

    elif coordenador != '' and coordenador is not None:
        projetos = projetos.filter(coordenador_projeto__nome_completo__icontains=coordenador)

    elif portaria != '' and portaria is not None:
        projetos = projetos.filter(portaria_projeto__iexact=portaria)

    elif acao != '' and acao is not None:
        projetos = projetos.filter(tipos_de_acoes__iexact=acao)

    elif areas != '' and areas is not None:
        projetos = projetos.filter(area_projeto__iexact=areas)

    if inicio != '' and inicio is not None:
        projetos = projetos.filter(data_de_inicio__gte=inicio).order_by('data_de_inicio')

    if termino != '' and termino is not None:
        projetos = projetos.filter(data_de_fim__lte=termino).order_by('data_de_inicio')

    page = request.GET.get('page', 1)
    paginator = Paginator(projetos, 10)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    lista_acoes = Projeto.acoes
    lista_areas = Projeto.areas

    dados = {
        'projetos': users,
        'acoes': lista_acoes,
        'areas': lista_areas,
    }

    return render(request, 'buscar.html', dados)


def editar_projeto(request, projeto_id):
    if request.method == 'GET':
        projeto_editar = Projeto.objects.filter(id=projeto_id).first()
        if projeto_editar is None:
            return redirect(reverse('projeto'))
        form = EditForm(instance=projeto_editar)
        form_colab_factory = inlineformset_factory(Projeto, Colaboradores, form=ColabForm, extra=1)
        form_colab = form_colab_factory(instance=projeto_editar)

        context = {
            'form': form,
            'form_colab': form_colab,
            'projeto': projeto_editar,
            'id': projeto_id,
        }
        return render(request, 'editar_projeto.html', context)
    elif request.method == 'POST':
        projeto_editar = Projeto.objects.filter(id=projeto_id).first()
        if projeto_editar is None:
            return redirect(reverse('projeto'))
        form = EditForm(request.POST, request.FILES, instance=projeto_editar)
        form_colab_factory = inlineformset_factory(Projeto, Colaboradores, form=ColabForm, extra=1)
        form_colab = form_colab_factory(request.POST, instance=projeto_editar)

        portaria = projeto_editar.portaria_projeto
        value = request.POST.get('portaria_projeto')

        editado = int(value)

        if portaria != editado:
            if Projeto.objects.filter(portaria_projeto=editado).exists():
                form.add_error('portaria_projeto', 'Portaria já registrada!')

        valor = request.POST.get('valor_financiado')
        request.POST._mutable = True
        request.POST['valor_financiado'] = valor
        request.POST._mutable = False

        financiado = request.POST.get('financiado')
        if financiado == "no":
            request.POST._mutable = True
            request.POST['financiador'] = ""
            request.POST['valor_financiado'] = ""
            request.POST['edital_financiado'] = ""
            request.POST._mutable = False

        if form.is_valid() and form_colab.is_valid():
            projeto_editado = form.save()
            form_colab.instance = projeto_editado
            form_colab.save()
            return redirect('projeto', projeto_editar.id)
        else:
            context = {
                'form': form,
                'form_colab': form_colab,
                'projeto': projeto_editar,
            }
            return render(request, 'editar_projeto.html', context)


def relatorios(request, projeto_id):
    if request.method == 'GET':
        projeto_editar = Projeto.objects.filter(id=projeto_id).first()
        if projeto_editar is None:
            return redirect(reverse('projeto'))
        form = EditForm(instance=projeto_editar)
        form_relatorio_factory = inlineformset_factory(Projeto, Relatorios, form=RelatorioForm, extra=1)
        form_relatorio = form_relatorio_factory(instance=projeto_editar)

        context = {
            'form': form,
            'form_relatorio': form_relatorio,
            'id': projeto_id,
        }

        return render(request, 'relatorios.html', context)
    elif request.method == 'POST':
        projeto_editar = Projeto.objects.filter(id=projeto_id).first()
        if projeto_editar is None:
            return redirect(reverse('projeto'))
        form = EditForm(request.POST, instance=projeto_editar)
        form_relatorio_factory = inlineformset_factory(Projeto, Relatorios, form=RelatorioForm, extra=1)
        form_relatorio = form_relatorio_factory(request.POST, request.FILES, instance=projeto_editar)

        if form.is_valid() and form_relatorio.is_valid():
            projeto_editado = form.save()
            form_relatorio.instance = projeto_editado
            form_relatorio.save()
            return redirect('projeto', projeto_id)
        else:
            context = {
                'form': form,
                'form_relatorio': form_relatorio,
                'id': projeto_id,
            }
            return render(request, 'editar_projeto.html', context)


def bolsas(request, projeto_id):
    projeto = get_object_or_404(Projeto, pk=projeto_id)

    projeto_a_exibir = {
        'projeto': projeto,
        'id': projeto_id,
    }

    bolsas = Bolsas.objects.filter(projeto_id=projeto_id).all()

    for bolsa in bolsas:
        id = bolsa.id
        bolsistas = Bolsistas.objects.filter(bolsa_id=id).all()
        if not bolsistas:
            bolsa = bolsa.id
            return redirect('cadastrar_bolsista', bolsa, projeto_id)

    return render(request, 'bolsas.html', projeto_a_exibir)


def cadastrar_bolsa(request, projeto_id):
    if request.method == 'GET':
        projeto_editar = Projeto.objects.filter(id=projeto_id).first()
        if projeto_editar is None:
            return redirect(reverse('projeto'))
        form = EditForm(instance=projeto_editar)
        form_bolsa_factory = inlineformset_factory(Projeto, Bolsas, form=BolsaForm, extra=1)
        form_bolsa = form_bolsa_factory(instance=projeto_editar)

        context = {
            'form': form,
            'form_bolsa': form_bolsa,
            'id': projeto_id,
        }
        return render(request, 'cadastrar_bolsa.html', context)
    elif request.method == 'POST':
        projeto_editar = Projeto.objects.filter(id=projeto_id).first()
        if projeto_editar is None:
            return redirect(reverse('projeto'))
        form = EditForm(request.POST, instance=projeto_editar)

        form_bolsa_factory = inlineformset_factory(Projeto, Bolsas, form=BolsaForm, extra=1)
        form_bolsa = form_bolsa_factory(request.POST, instance=projeto_editar)

        if form.is_valid() and form_bolsa.is_valid():
            projeto_editado = form.save()
            form_bolsa.instance = projeto_editado
            form_bolsa.save()
            print("Projeto aberto: ", projeto_id)
            return redirect('bolsas', projeto_id)
        else:
            context = {
                'form': form,
                'form_bolsa': form_bolsa,
                'id': projeto_id,
            }
            return render(request, 'cadastrar_bolsa.html', context)


def cadastrar_bolsista(request, bolsa, id):
    if request.method == 'GET':
        bolsa_criada = Bolsas.objects.filter(id=bolsa).first()
        if bolsa_criada is not None:
            projeto_editar = Projeto.objects.filter(id=id).first()
            if projeto_editar is None:
                return redirect(reverse('projeto'))
            form = EditForm(instance=projeto_editar)

            form_bolsa_factory = inlineformset_factory(Projeto, Bolsas, form=BolsaForm, extra=1)
            form_bolsa = form_bolsa_factory(instance=projeto_editar)

            form_bolsista_factory = inlineformset_factory(Bolsas, Bolsistas, form=BolsistaForm, extra=1)
            form_bolsista = form_bolsista_factory(instance=bolsa_criada)

            bolsa_id = bolsa_criada.id
            bolsista = Bolsistas.objects.filter(bolsa_id=bolsa_id).all()
            if bolsista:
                flag = False
            else:
                flag = True

            context = {
                'form': form,
                'bolsa_criada': bolsa_criada,
                'form_bolsa': form_bolsa,
                'form_bolsista': form_bolsista,
                'id': id,
                'alert_flag': flag,
            }
            return render(request, 'cadastrar_bolsista.html', context)
        return redirect('bolsas', id)

    elif request.method == 'POST':
        bolsa_criada = Bolsas.objects.filter(id=bolsa).first()
        if bolsa_criada is not None:
            projeto_editar = Projeto.objects.filter(id=id).first()
            if projeto_editar is None:
                return redirect(reverse('projeto'))
            form = EditForm(request.POST, instance=projeto_editar)

            form_bolsa_factory = inlineformset_factory(Projeto, Bolsas, form=BolsaForm, extra=1)
            form_bolsa = form_bolsa_factory(request.POST, instance=projeto_editar)

            form_bolsista_factory = inlineformset_factory(Bolsas, Bolsistas, form=BolsistaForm, extra=1)
            form_bolsista = form_bolsista_factory(request.POST, instance=bolsa_criada)

            if form_bolsista.is_valid() and form_bolsa.is_valid():
                form_bolsa.save()
                form_bolsista.save()
                return redirect('usuario_bolsista', bolsa_criada.id, id)
            else:
                context = {
                    'form': form,
                    'form_bolsa': form_bolsa,
                    'bolsa_criada': bolsa_criada,
                    'form_bolsista': form_bolsista,
                    'id': id,
                    'alert_flag': False,
                }
        return render(request, 'cadastrar_bolsista.html', context)


def usuario_bolsista(request, bolsa_id, projeto_id):
    bolsa = get_object_or_404(Bolsas, pk=bolsa_id)
    bolsistas = Bolsistas.objects.filter(bolsa_id=bolsa.id).all()

    x = 0
    senha = "123456"

    for bolsista in bolsistas:
        x += 1
        str_nome = bolsista.bolsista
        nome = ''.join(str_nome.split())

        str_user = nome

        user_size = len(str_user)

        if user_size > 10:
            user_name = ''
            for i in range(0, 9):
                user_name += str_user[i].lower()
        else:
            user_name = str_user.lower()

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

        existe = User.objects.filter(email=bolsista.email).exists()

        if not existe:
            user = User.objects.create_user(username=user_name, email=bolsista.email, password=senha)
            user.is_staff = True
            user.save()
    return redirect('bolsas', projeto_id)


def deletar_colaborador(request, colaborador, id):
    colaborador = Colaboradores.objects.filter(colaborador_projeto=colaborador)
    if colaborador is not None:
        colaborador.delete()
        return redirect('editar_projeto', id)
    else:
        return redirect(reverse('projeto'))


def deletar_bolsa(request, bolsa, id):
    bolsa = Bolsas.objects.filter(id=bolsa).first()
    if bolsa is not None:
        bolsistas = Bolsistas.objects.filter(bolsa_id=bolsa.id).all()
        for bolsista in bolsistas:
            usuario = User.objects.get(email=bolsista.email)
            usuario.delete()
        bolsa.delete()
    return redirect('bolsas', id)


def deletar_relatorio(request, relatorio, id):
    relatorio = Relatorios.objects.filter(relatorio=relatorio)
    if relatorio is not None:
        relatorio.delete()
    return redirect('relatorios', id)


def deletar_bolsista(request, bolsa_criada, bolsista_id, id):
    if bolsista_id == 0:
        return redirect('cadastrar_bolsista', bolsa_criada, id)
    else:
        bolsista = Bolsistas.objects.filter(id=bolsista_id).first()
        if bolsista is not None:
            return redirect('cadastrar_bolsista', bolsa_criada, id)
        else:
            return redirect(reverse('cadastrar_bolsista'))


def deletar_projeto(request, projeto_id):
    projeto = Projeto.objects.get(pk=projeto_id)
    projeto.delete()
    return redirect('lista_projetos')


def projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, pk=projeto_id)

    if request.user.is_authenticated:
        email = request.user.email
        bolsista = Bolsistas.objects.filter(email=email).exists()
        if bolsista:
            logado = True
        else:
            logado = False
    else:
        logado = False

    projeto_a_exibir = {
        'projeto': projeto,
        'logado': logado,
    }

    return render(request, 'projeto.html', projeto_a_exibir)


def relatorio_bolsas(request):
    bolsas = Bolsas.objects.order_by('id')
    bolsistas = Bolsistas.objects.order_by('id')

    financiador = request.GET.get('financiador')
    portaria = request.GET.get('portaria')
    inicio = request.GET.get('inicio')
    termino = request.GET.get('termino')
    pdf = request.GET.get('pdf')

    if financiador != '' and financiador is not None:
        bolsas = bolsas.filter(orgao_remunerador__icontains=financiador)

    elif portaria != '' and portaria is not None:
        bolsas = bolsas.filter(portaria_bolsa__iexact=portaria)

    if inicio != '' and inicio is not None:
        bolsas = bolsas.filter(data_de_inicio__gte=inicio).order_by('data_de_inicio')

    if termino != '' and termino is not None:
        bolsas = bolsas.filter(data_de_fim__lte=termino).order_by('data_de_inicio')

    page = request.GET.get('page', 1)
    paginator = Paginator(bolsas, 10)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    if financiador != '' and financiador is not None:
        v_financiador = financiador
    else:
        v_financiador = ''
    if portaria != '' and portaria is not None:
        v_portaria = portaria
    else:
        v_portaria = ''
    if inicio != '' and inicio is not None:
        v_inicio = inicio
    else:
        v_inicio = ''
    if termino != '' and termino is not None:
        v_termino = termino
    else:
        v_termino = ''

    dados = {
        'bolsas': users,
        'bolsistas': bolsistas,
        'v_financiador': v_financiador,
        'v_portaria': v_portaria,
        'v_inicio': v_inicio,
        'v_termino': v_termino,
    }

    if pdf == "pdf":

        data = {
            'bolsas': bolsas,
            'bolsistas': bolsistas,
        }
        template = get_template("bolsas_pdf.html")
        data_p = template.render(data)
        response = BytesIO()

        pdfPage = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")), response)
        if not pdfPage.err:
            return HttpResponse(response.getvalue(), content_type="application/pdf")
        else:
            return None

    return render(request, 'relatorio_bolsas.html', dados)


def ViewPDF(request, pdf_id):
    projeto_view = get_object_or_404(Projeto, pk=pdf_id)

    projeto_a_exibir = {
        'projeto': projeto_view
    }

    template = get_template("pdf_page.html")
    data_p = template.render(projeto_a_exibir)
    response = BytesIO()

    pdfPage = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")), response)
    if not pdfPage.err:
        return HttpResponse(response.getvalue(), content_type="application/pdf")
    else:
        return None

from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Contato
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages


# Create your views here.
def index(request):
    # Ordenando a tabela por ID em ordem decrescente e filtrando somente os contatos que estão com mostrar=True
    contatos = Contato.objects.order_by('-id').filter(mostrar=True)

    paginator = Paginator(contatos, 5)
    page = request.GET.get('p')
    contatos = paginator.get_page(page)

    return render(request, 'contatos/index.html', {
        'contatos': contatos
    })


def see_contact(request, contato_id):
    # contato = Contato.objects.get(id=contato_id)
    contato = get_object_or_404(Contato, id=contato_id)  # Forma mais simples de retornar erro 404

    # Não exibindo os detalhes se o campo mostrar estiver = False
    if not contato.mostrar:
        raise Http404()

    return render(request, 'contatos/see_contact.html', {
        'contato': contato
    })


# Forma mais trabalhosa de retornar erro 404 com try ... except
# try:
#     contato = Contato.objects.get(id=contato_id)
#     return render(request, 'contatos/see_contact.html', {
#         'contato': contato
#     })
# except Contato.DoesNotExist as e:
#     raise Http404()


def busca(request):
    termo = request.GET.get('termo')  # Pegando o que foi digitado no campo de busca
    if termo is None or not termo:
        messages.add_message(request,
                             messages.ERROR,
                             'Campo termo não pode ficar vazio!'
                             )
        return redirect('index')


    # Concatenando nome e sobrenome
    campos = Concat('nome', Value(' '), 'sobrenome')

    contatos = Contato.objects.annotate(
        nome_completo=campos
    ).filter(
        Q(nome_completo__icontains=termo) | Q(telefone__icontains=termo)
    )
    # Para ver o select que o sistema está executando
    # print(contatos.query)

    paginator = Paginator(contatos, 5)
    page = request.GET.get('p')
    contatos = paginator.get_page(page)

    return render(request, 'contatos/index.html', {
        'contatos': contatos
    })

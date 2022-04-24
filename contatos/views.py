from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Contato
from django.core.paginator import Paginator


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

from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Contato


# Create your views here.
def index(request):
    contatos = Contato.objects.all()
    return render(request, 'contatos/index.html', {
        'contatos': contatos
    })


def see_contact(request, contato_id):
    # contato = Contato.objects.get(id=contato_id)
    contato = get_object_or_404(Contato, id=contato_id)  # Forma mais simples de retornar erro 404
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

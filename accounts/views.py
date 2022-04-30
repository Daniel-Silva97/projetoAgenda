from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import validate_email
from django.contrib.auth.models import User


# Create your views here.
def login(request):
    return render(request, 'accounts/login.html')


def logout(request):
    return render(request, 'accounts/logout.html')


def register(request):
    if request.method != 'POST':
        return render(request, 'accounts/register.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    if not nome:
        messages.error(request, 'Campo Nome obrigatório')
        return render(request, 'accounts/register.html')
    elif not sobrenome:
        messages.error(request, 'Campo Sobrenome obrigatório')
        return render(request, 'accounts/register.html')
    elif not email:
        messages.error(request, 'Campo E-mail obrigatório')
        return render(request, 'accounts/register.html')
    elif not usuario:
        messages.error(request, 'Campo Usuário obrigatório')
        return render(request, 'accounts/register.html')
    elif not senha:
        messages.error(request, 'Campo Senha obrigatório')
        return render(request, 'accounts/register.html')
    elif not senha2:
        messages.error(request, 'Campo Repita sua senha obrigatório')
        return render(request, 'accounts/register.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'E-mail inválido')
        return render(request, 'accounts/register.html')

    if len(usuario) < 6:
        messages.error(request, 'Usuário muito curto, digite pelo menos 6 caracteres')
        return render(request, 'accounts/register.html')

    if len(senha) < 6:
        messages.error(request, 'Senha muito curta, digite pelo menos 6 caracteres')
        return render(request, 'accounts/register.html')

    if senha != senha2:
        messages.error(request, 'Senhas não conferem, digite novamente')
        return render(request, 'accounts/register.html')

    if User.objects.filter(username=usuario).exists():
        messages.info(request, 'Usuário já possui cadastro')
        return render(request, 'accounts/register.html')

    if User.objects.filter(email=email).exists():
        messages.info(request, 'E-mail já possui cadastro')
        return render(request, 'accounts/register.html')

    messages.success(request, 'Usuário cadastrado com sucesso! Realize o login.')
    user = User.objects.create_user(username=usuario, email=email, password=senha, first_name=nome, last_name=sobrenome)
    user.save()
    return redirect('login')


    return render(request, 'accounts/register.html')


def dashboard(request):
    return render(request, 'accounts/dashboard.html')

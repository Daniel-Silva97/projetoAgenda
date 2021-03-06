from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormContato


# Create your views here.
def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.error(request, 'Usuário ou Senha inválidos!')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, 'Login realizado com sucesso!')
        return redirect('dashboard')


def logout(request):
    auth.logout(request)
    return redirect('login')


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


@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContato()
        return render(request, 'accounts/dashboard.html', {'form': form})

    form = FormContato(request.POST, request.FILES)

    if not form.is_valid():
        messages.error(request, 'Erro ao cadastrar contato')
        form = FormContato()
        return render(request, 'accounts/dashboard.html', {'form': form})

    descricao = request.POST.get('descricao')

    if len(descricao) < 5:
        messages.error(request, 'Descrição deve conter mais que 5 caracteres')
        form = FormContato()
        return render(request, 'accounts/dashboard.html', {'form': form})

    form.save()
    messages.success(request, 'Contato cadastrado com sucesso!')
    return redirect('dashboard')

from django.db import models
from django.utils import timezone

"""
CONTATOS
id: INT (automático)
nome: STR * (obrigatório)
sobrenome: STR (opcional)
telefone: STR * (obrigatório)
email: STR (opcional)
data_criacao: DATETIME (automático)
descricao: texto
categoria: CATEGORIA (outro model)

 CATEGORIA
 id: INT
 nome: STR * (obrigatório)
"""


# Create your models here.
class Categoria(models.Model):
    nome = models.CharField(max_length=255)

    # Para mudar a exibição do nome no DjangoAdmin
    def __str__(self):
        return self.nome


class Contato(models.Model):
    nome = models.CharField(max_length=255)
    sobrenome = models.CharField(max_length=255, blank=True)  # blank=True diz que o cmapo não é obrigatório
    telefone = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True)
    data_criacao = models.DateTimeField(default=timezone.now)
    descricao = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)  # Criando chave estrangeira referenciando
    mostrar = models.BooleanField(default=True)
    # classe Categoria

    def __str__(self):
        return self.nome

# Para criar no SQLite, precisa fazer as migrações, são 2 comandos:
# python .\manage.py makemigrations
# python manage.py migrate

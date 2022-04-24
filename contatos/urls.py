from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:contato_id>', views.see_contact, name='see_contact'),
    path('busca/', views.busca, name='busca'),
]

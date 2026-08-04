from django.urls import path
from .views import (
    livro_detail_view,
    buscar_livros_view
)

app_name = 'catalogo'

urlpatterns = [
    path('buscar/', buscar_livros_view, name='buscar_livros'),
    path('<str:slug>/', livro_detail_view, name='livro_detail'),
]
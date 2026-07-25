from django.urls import path
from .views import (
    carrinho_view, 
    adicionar_item_view, 
    limpar_carrinho_view,
    remover_item_view,
    diminuir_quantidade_view
)

app_name = 'carrinho'

urlpatterns = [
    path('carrinho/', carrinho_view, name='carrinho'),
    path('adicionar/<int:livro_id>/', adicionar_item_view, name='adicionar_item'),
    path('limpar-carrinho/', limpar_carrinho_view, name='limpar_carrinho'),
    path('remover/<int:livro_id>/', remover_item_view, name='remover_item'),
    path('diminuir-quantidade/<int:livro_id>', diminuir_quantidade_view, name='diminuir_quantidade')
]

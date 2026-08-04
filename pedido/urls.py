from django.urls import path
from .views import (
  confirmar_pedido_view,
  detalhe_pedido_view,
  fechar_pedido_view,
)

app_name = 'pedido'

urlpatterns = [
    path("confirmar/", confirmar_pedido_view, name="confirmar_pedido"),
    path("fechar/<int:endereco_id>/", fechar_pedido_view, name="fechar_pedido"),
    path("<int:pedido_id>/", detalhe_pedido_view, name="detalhe_pedido"),
]

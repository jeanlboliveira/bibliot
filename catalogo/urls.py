from django.urls import path
from .views import (
    livro_detail_view
)

app_name = 'catalogo'

urlpatterns = [
    path('<str:slug>/', livro_detail_view, name='livro_detail')
]
from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('<str:slug>/', views.livro_detail_view, name='livro_detail')
]
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from . import models
from lista_desejos.models import ListaDeDesejos
from carrinho.models import Carrinho

def livro_detail_view(request, slug):
    livro = get_object_or_404(models.Livro, slug=slug)
    esta_na_lista = False
    esta_no_carrinho = False

    if request.user.is_authenticated:
        esta_na_lista = ListaDeDesejos.objects.esta_na_lista(request.user, livro)
        esta_no_carrinho = Carrinho.objects.esta_no_carrinho(request.user, livro)

    context = {
        'livro': livro,
        'esta_na_lista': esta_na_lista,
        'esta_no_carrinho': esta_no_carrinho,
    }

    return render(
        request=request,
        template_name='catalogo/livro_detail.html',
        context=context
    )


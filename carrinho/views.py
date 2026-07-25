from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Carrinho
from catalogo.models import Livro
# Create your views here.

def carrinho_view(request):
    items = Carrinho.objects.get_itens(usuario=request.user)

    context = {
        'items': items,
    }

    return render(
        request=request,
        template_name='carrinho/carrinho.html',
        context=context
    )


def adicionar_item_view(request, livro_id):
    if request.method == 'POST':
        livro = get_object_or_404(Livro, id=livro_id)

        Carrinho.objects.adicionar_livro(
            livro=livro, 
            usuario=request.user
        )

        return redirect(request.META.get('HTTP_REFERER', 'core:home'))

    return HttpResponse(status=405)


def remover_item_view(request, livro_id):
    if request.method == 'POST':
        livro = get_object_or_404(Livro, id=livro_id)
        Carrinho.objects.remover_livro(
            usuario=request.user,
            livro=livro,
        )
        return redirect('carrinho:carrinho')

    return HttpResponse(status=405)


def limpar_carrinho_view(request):
    if request.method == 'POST':
        Carrinho.objects.limpar_carrinho(usuario=request.user)

        return redirect(
            'carrinho:carrinho'
        )
        
    return render(
        request=request,
        template_name='core/home.html'
    )
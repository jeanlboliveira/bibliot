from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import Carrinho
from catalogo.models import Livro
# Create your views here.


@login_required
def carrinho_view(request):
    items = Carrinho.objects.get_itens(usuario=request.user)
    subtotal_carrinho = Carrinho.objects.subtotal_carrinho(usuario=request.user)

    print('SUBTOTAL DO CARRINHO:', subtotal_carrinho)

    context = {
        'items': items,
        'subtotal_carrinho': subtotal_carrinho,
    }

    return render(
        request=request,
        template_name='carrinho/carrinho.html',
        context=context
    )

@login_required
def adicionar_item_view(request, livro_id):
    if request.method == 'POST':
        livro = get_object_or_404(Livro, id=livro_id)

        Carrinho.objects.adicionar_livro(
            livro=livro, 
            usuario=request.user
        )

        subtotal_carrinho = Carrinho.objects.subtotal_carrinho(usuario=request.user)


        item = get_object_or_404(Carrinho, usuario=request.user, livro=livro)

        return JsonResponse({
            'quantidade': item.quantidade,
            'subtotal': f'{item.subtotal:.2f}',
            'quantidade_total_carrinho': Carrinho.objects.filter(usuario=request.user).count(),
            'subtotal_carrinho': f'{subtotal_carrinho:.2f}'
        })

    return HttpResponse(status=405)

@login_required
def remover_item_view(request, livro_id):
    if request.method == 'POST':
        livro = get_object_or_404(Livro, id=livro_id)
        Carrinho.objects.remover_livro(
            usuario=request.user,
            livro=livro,
        )
        return redirect('carrinho:carrinho')

    return HttpResponse(status=405)

@login_required
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

@login_required
def diminuir_quantidade_view(request, livro_id):
    if request.method == "POST":
        livro = get_object_or_404(Livro, id=livro_id)

        Carrinho.objects.diminuir_quantidade(usuario=request.user, livro=livro)
        subtotal_carrinho = Carrinho.objects.subtotal_carrinho(usuario=request.user)


        item = get_object_or_404(Carrinho, usuario=request.user, livro=livro)

        return JsonResponse({
            'quantidade': item.quantidade,
            'subtotal': item.subtotal,
            'subtotal_carrinho': subtotal_carrinho

        })

    return render(
        request=request,
        template_name='core/home.html'
    )
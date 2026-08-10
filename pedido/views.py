from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from carrinho.models import Carrinho
from accounts.models import Endereco
from .models import (
    Pedido,
    ItemPedido, 
)


@login_required
def detalhe_pedido_view(request, pedido_id):
    pedido = get_object_or_404(
        Pedido.objects.select_related('usuario', 'endereco').prefetch_related('itens__livro'),
        id=pedido_id,
        usuario=request.user,
    )

    pedido_total = sum(item.subtotal for item in pedido.itens.all())

    return render(
        request=request,
        template_name='pedido/detalhes_pedido.html',
        context={
            'pedido': pedido,
            'pedido_total': pedido_total,
        }
    )

# Create your views here.
@login_required
def confirmar_pedido_view(request):
    usuario = request.user
    itens_carrinho = Carrinho.objects.filter(usuario=usuario)

    if not itens_carrinho.exists():
        return redirect("carrinho:carrinho")

    if request.method == 'POST':
        endereco_id = request.POST.get('endereco')
        if endereco_id:
            return redirect('pedido:fechar_pedido', endereco_id=endereco_id)

    enderecos = Endereco.objects.filter(usuario=usuario).order_by('-principal', 'id')
    subtotal_carrinho = sum(item.subtotal for item in itens_carrinho)

    return render(
        request=request,
        template_name='pedido/confirmar_pedido.html',
        context={
            'enderecos': enderecos,
            'itens': itens_carrinho,
            'subtotal_carrinho': subtotal_carrinho,
        }
    )


@login_required
@transaction.atomic
def fechar_pedido_view(request, endereco_id):
    usuario = request.user

    itens_carrinho = Carrinho.objects.filter(usuario=usuario)

    if not itens_carrinho.exists():
        return redirect("carrinho:carrinho")

    endereco = get_object_or_404(
        Endereco,
        id=endereco_id,
        usuario=usuario,
    )

    endereco_pedido = endereco

    pedido = Pedido.objects.create(
        usuario=usuario,
        endereco=endereco_pedido,
    )

    for item in itens_carrinho:
        ItemPedido.objects.create(
            pedido=pedido,
            livro=item.livro,
            quantidade=item.quantidade,
            preco_unitario=item.livro.preco,
        )

    itens_carrinho.delete()

    return redirect("pedido:detalhe_pedido", pedido_id=pedido.id)

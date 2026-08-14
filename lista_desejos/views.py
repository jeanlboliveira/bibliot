from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render

from catalogo.models import Livro

from .models import ListaDeDesejos


# Create your views here.
@login_required
def wishlist_view(request):
    items = ListaDeDesejos.objects.get_itens(usuario=request.user)

    context = {
        'items': items,
    }
    
    return render(
        request=request, 
        template_name='lista_desejos/wishlist.html', 
        context=context,
    )

@login_required
def toggle_view(request, livro_id):
    if request.method == 'POST':
        usuario = request.user
        livro = get_object_or_404(Livro, id=livro_id)

        ListaDeDesejos.objects.adicionar_ou_remover_item(usuario=usuario, livro=livro)

        return JsonResponse({
            'quantidade_total_wishlist': ListaDeDesejos.objects.filter(usuario=usuario).count()
        })

    return HttpResponse(status=405)


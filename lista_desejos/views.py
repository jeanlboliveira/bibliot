from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import ListaDeDesejos
from catalogo.models import Livro

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

        ListaDeDesejos.objects.adicionar_item(usuario=usuario, livro=livro)

        return JsonResponse({
            'quantidade_total_wishlist': ListaDeDesejos.objects.filter(usuario=usuario).count()
        })

    return HttpResponse(status=405)


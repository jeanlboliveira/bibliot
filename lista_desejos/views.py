from django.shortcuts import render
from .models import ListaDeDesejos

# Create your views here.
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
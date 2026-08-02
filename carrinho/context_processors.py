from .models import Carrinho

def quantidade_carrinho(request):
    if request.user.is_authenticated:
        total = Carrinho.objects.filter(usuario=request.user).count()
    else:
        total = 0

    return {
        'quantidade_carrinho': total
    }
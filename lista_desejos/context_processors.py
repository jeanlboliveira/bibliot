from .models import ListaDeDesejos

def quantidade_wishlist(request):

  if request.user.is_authenticated:
    total_wishlist = ListaDeDesejos.objects.filter(usuario=request.user).count()

  else:
    total_wishlist = 0


  context = {
    'total_wishlist': total_wishlist
  }
  return context

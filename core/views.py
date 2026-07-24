from django.shortcuts import render
from catalogo import models

# Create your views here.
def home_view(request):
    categorias = models.Categoria.objects.prefetch_related("livros").filter(ativa=True) # relação many 2 many, precisa do related_name

    context = {
        'categorias': categorias
    }

    return render(
        request=request,
        template_name='core/home.html',
        context=context
    )
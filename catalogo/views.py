from django.shortcuts import render
from django.shortcuts import get_object_or_404
from . import models

def livro_detail_view(request, slug):
    livro = get_object_or_404(models.Livro, slug=slug)
    # print('Livro:', livro)
    context = {
        'livro': livro
    }

    return render(
        request=request,
        template_name='catalogo/livro_detail.html',
        context=context
    )


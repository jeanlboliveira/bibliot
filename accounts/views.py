from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CadastroForm, EnderecoForm

# Create your views here.

def register_view(request):
    if request.method == "POST":
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')

    else:
        form = CadastroForm()

    return render(
        request=request,
        template_name='accounts/register.html',
        context={'form': form}
    )


@login_required
def profile_view(request):
    return render(
        request=request,
        template_name='accounts/profile.html',
        context={
            'enderecos': request.user.enderecos.all(),
            'pedidos': request.user.pedidos.select_related('endereco').prefetch_related('itens__livro').order_by('-criado_em')
        }
    )


@login_required
def adicionar_endereco_view(request):
    next_url = request.GET.get('next', 'home')
    if request.method == 'POST':
        form = EnderecoForm(request.POST)
        if form.is_valid():
            endereco = form.save(commit=False)
            endereco.usuario = request.user
            endereco.save()
            return redirect(next_url)
    else:
        form = EnderecoForm()

    return render(
        request=request,
        template_name='accounts/adicionar_endereco.html',
        context={'form': form}
    )


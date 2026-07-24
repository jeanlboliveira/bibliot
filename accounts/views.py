from django.shortcuts import render, redirect
from .forms import CadastroForm

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


def profile_view(request):
    return render(
        request=request,
        template_name='accounts/profile.html'
    )


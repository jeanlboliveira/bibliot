from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Endereco, Usuario


class LoginForm(AuthenticationForm):
    # o username é obrigatório modo a estrutura da classe-mãe
    username = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(
            attrs={
                "class": "auth-input",
                "id": "email",
            }
        ),
    )

    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(
            attrs={
                "class": "auth-input",
                "id": "pass",
            }
        ),
    )


class CadastroForm(UserCreationForm):
    nome = forms.CharField(
        label="Nome",
        widget=forms.TextInput(attrs={"class": "auth-input", "id": "nome"}),
    )

    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(
            attrs={
                "class": "auth-input",
                "id": "email",
            }
        ),
    )

    telefone = forms.CharField(
        label="Telefone",
        widget=forms.EmailInput(
            attrs={
                "class": "auth-input",
                "id": "telefone",
            }
        ),
    )

    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(
            attrs={
                "class": "auth-input",
                "id": "password1",
            }
        ),
    )

    password2 = forms.CharField(
        label="Confirmar Senha",
        widget=forms.PasswordInput(
            attrs={
                "class": "auth-input",
                "id": "password2",
            }
        ),
    )

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ("email", "nome")


class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = [
            "nome_completo",
            "cep",
            "estado",
            "cidade",
            "bairro",
            "rua",
            "numero",
            "complemento",
            "referencia",
            "principal",
        ]

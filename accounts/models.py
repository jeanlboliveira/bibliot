from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator

# Create your models here.
class UsuarioManager(BaseUserManager):
    def create_user(self, email, password = None, **extra_fields):
        if not email:
            raise ValueError(_('O E-mail é obrigatório'))

        email = self.normalize_email(email)
        usuario = self.model(email=email, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)

        return usuario

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _("E-mail"), 
        max_length=254, 
        unique=True,
        db_index=True,
    )     

    nome = models.CharField(
        _("Nome"),
        max_length=255,
    )

    telefone = models.CharField(
        _("Telefone"), 
        max_length=20, 
        blank=True,
        validators=[
            RegexValidator(
                r'/^(?:\(\d{2}\)\s?|(\d{2}))9\d{4}-?\d{4}$/',
                _('O Telefone deve o formato (11)91234-5678 ou 11912345678')
            )
        ],
    )

    data_nascimento = models.DateField(
        _("Dafa de nascimento"), 
        null=True, 
        blank=True,
    )

    is_active = models.BooleanField(
        _("Ativo"), 
        default=True,
        help_text=_("Usuários inativos não podem fazer login"),
    )

    is_staff = models.BooleanField(
        _("Membro da equipe"), 
        default=False
    )

    data_joined = models.DateTimeField(
        _("Data de Cadastro"),
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        _("Atualizado em"), 
        auto_now=True,
    )

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('Usuário')
        verbose_name_plural = _('Usuários')
        ordering = ['-data_joined']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['-data_joined']),
        ]

    def __str__(self):
        return self.email


class Endereco(models.Model):
    class Estado(models.TextChoices):
        AC = "AC", _("Acre")
        AL = "AL", _("Alagoas")
        AP = "AP", _("Amapá")
        AM = "AM", _("Amazonas")
        BA = "BA", _("Bahia")
        CE = "CE", _("Ceará")
        DF = "DF", _("Distrito Federal")
        ES = "ES", _("Espírito Santo")
        GO = "GO", _("Goiás")
        MA = "MA", _("Maranhão")
        MT = "MT", _("Mato Grosso")
        MS = "MS", _("Mato Grosso do Sul")
        MG = "MG", _("Minas Gerais")
        PA = "PA", _("Pará")
        PB = "PB", _("Paraíba")
        PR = "PR", _("Paraná")
        PE = "PE", _("Pernambuco")
        PI = "PI", _("Piauí")
        RJ = "RJ", _("Rio de Janeiro")
        RN = "RN", _("Rio Grande do Norte")
        RS = "RS", _("Rio Grande do Sul")
        RO = "RO", _("Rondônia")
        RR = "RR", _("Roraima")
        SC = "SC", _("Santa Catarina")
        SP = "SP", _("São Paulo")
        SE = "SE", _("Sergipe")
        TO = "TO", _("Tocantins")

    usuario = models.ForeignKey(
        "accounts.Usuario",
        on_delete=models.CASCADE,
        related_name="enderecos",
        verbose_name=_('Usuário'),
    )

    nome_completo = models.CharField(
        _("Nome Completo"), 
        max_length=200, 
        help_text=("Quem vai receber o pedido"),
    )

    cep = models.CharField(
        _("CEP"),
        max_length=9,
        validators=[
            RegexValidator(
                r'^\d{5}-?\d{3}$',
                _('CEP deve ser no formato XXXXX-XXX ou XXXXXXXX'),
            )
        ],
    )

    estado = models.CharField(
        _("Estado"),
        max_length=2,
        choices=Estado.choices,
    )

    cidade = models.CharField(
        _('Cidade'),
        max_length=50,
    )

    bairro = models.CharField(
        _('Bairro'),
        max_length=50,
    )

    rua = models.CharField(
        _('Rua'),
        max_length=200,
    )

    numero = models.CharField(
        _('Número'),
        max_length=10
    )

    complemento = models.CharField(
        _('Complemento'),
        max_length=100, 
        blank=True,
        help_text=('Apto, block, etc'),
    )

    referencia = models.CharField(
        _('Referência'),
        max_length=200, 
        blank=True,
        help_text=_('Ex: próximo ao mercado'),
    )

    principal = models.BooleanField(
        _('É o endereço principal?'),
        default=False,
    )

    created_at = models.DateTimeField(
        _('Criado em'),
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        _('Atualizado em'),
        auto_now=True,
    )


    class Meta:
        verbose_name = 'Endereco'
        verbose_name_plural = 'Enderecos'
        ordering = ['-principal', '-created_at']
        unique_together = ('usuario', 'numero', 'rua', 'cidade')
        indexes = [
            models.Index(fields=['usuario', 'principal']),
        ]


    def __str__(self):
        """Unicode representation of Endereco."""
        return f"{self.rua}, {self.numero} - {self.cidade}/{self.estado}"

    def get_endereco_formatado(self):
        """Retorna endereço formatado para exibição."""
        endereco = f"{self.rua}, {self.numero}"
        if self.complemento:
            endereco += f" - {self.complemento}"
        endereco += f", {self.bairro}, {self.cidade}/{self.estado} {self.cep}"
        return endereco
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

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
    email = models.EmailField(_("E-mail"), max_length=254, unique=True)     
    nome = models.CharField(_("Nome"), max_length=255)
    telefone = models.CharField(_("Telefone"), max_length=20, blank=True)
    data_nascimento = models.DateField(_("Nascimento"), auto_now=False, auto_now_add=False, null=True, blank=True)

    is_active = models.BooleanField(_("Ativo"), default=True)
    is_staff = models.BooleanField(_("Membro da equipe"), default=False)
    data_joined = models.DateTimeField(_("Data de Cadastro"), auto_now=False, auto_now_add=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('Usuário')
        verbose_name_plural = _('Usuários')

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
        
    """Model definition for Endereco."""

    # TODO: Define fields here
    usuario = models.ForeignKey(
            "accounts.Usuario",
            on_delete=models.CASCADE,
            related_name="enderecos",
        )
    nome_completo = models.CharField(_("Nome Completo"), max_length=200, blank=True)
    cep = models.CharField(max_length=9)
    estado = models.CharField(
        max_length=2,
        choices=Estado.choices
    )
    cidade = models.CharField(max_length=50)
    bairro = models.CharField(max_length=50)
    rua = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True)

    principal = models.BooleanField(default=False)
    referencia = models.CharField(max_length=200, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        """Meta definition for Endereco."""

        verbose_name = 'Endereco'
        verbose_name_plural = 'Enderecos'

    def __str__(self):
        """Unicode representation of Endereco."""
        return f"{self.rua}, {self.numero} - {self.cidade}/{self.estado}"
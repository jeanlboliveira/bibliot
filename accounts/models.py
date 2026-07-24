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
    
        
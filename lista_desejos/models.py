from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class ListaDeDesejosManager(models.Manager):
    def adicionar_ou_remover_item(self, usuario, livro):
        item, criado = self.get_or_create(
            usuario=usuario,
            item=livro,
        )

        if not criado:
            return self.filter(usuario=usuario, item=livro).delete()
        
        return item

    def remover_item(self, usuario, livro):
        return self.filter(usuario=usuario, item=livro).delete()

    def esta_na_lista(self, usuario, livro):
        return self.filter(usuario=usuario, item=livro).exists()

    def get_itens(self, usuario):
        return self.filter(usuario=usuario).select_related('livro', 'usuario')


class ListaDeDesejos(models.Model):
    usuario = models.ForeignKey(
        "accounts.Usuario", 
        verbose_name=_("Usuário"), 
        on_delete=models.CASCADE,
        related_name='wishlist',
    )

    livro = models.ForeignKey(
        "catalogo.Livro", 
        verbose_name=_("Item"),
        on_delete=models.CASCADE,
    )

    adicionado_em = models.DateTimeField(
        _("Adicionado em"), 
        auto_now_add=True,
    )

    objects = ListaDeDesejosManager()

    class Meta:
        verbose_name = _("lista de desejos")
        verbose_name_plural = _("listas de desejos")
        unique_together = ('usuario', 'livro')
        ordering = ['-adicionado_em']
        indexes = [
            models.Index(fields=['usuario', 'livro'])
        ]

    def __str__(self):
        return f'{self.usuario.nome} → {self.livro.titulo}'

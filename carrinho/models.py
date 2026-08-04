from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class CarrinhoManager(models.Manager):
    def adicionar_livro(self, livro, usuario, quantidade=1):
        item, criado = self.get_or_create(
            usuario=usuario,
            livro=livro,
            defaults={
                'quantidade': quantidade
            }
        )

        if not criado:
            item.quantidade += quantidade
            item.save()

        return item

    def remover_livro(self, usuario, livro):
        return self.filter(usuario=usuario, livro=livro).delete()

    def limpar_carrinho(self, usuario):
        return self.filter(usuario=usuario).delete()
    
    def get_itens(self, usuario):
        return self.filter(usuario=usuario)
        
    def diminuir_quantidade(self, usuario, livro):
        item, update = self.update_or_create(
            usuario=usuario,
            livro=livro,
        )

        if not update and item.quantidade > 1:
            item.quantidade -= 1
            item.save()

        return item

    def esta_no_carrinho(self, usuario, livro):
        return self.filter(usuario=usuario, livro=livro).exists()

    def subtotal_carrinho(self, usuario):
        return (
            self.filter(usuario=usuario)
            .aggregate(
                subtotal=models.Sum(models.F("livro__preco" )* models.F('quantidade'))
            )['subtotal'] or 0
        )

class Carrinho(models.Model):
    usuario = models.ForeignKey("accounts.Usuario", verbose_name=_("Usuário"), on_delete=models.CASCADE)
    livro = models.ForeignKey("catalogo.Livro", verbose_name=_("Item"), on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(_("Quantidade"), default=1)

    objects = CarrinhoManager()
    
    @property
    def subtotal(self):
        return self.livro.preco * self.quantidade


    class Meta:
        verbose_name = _("carrinho")
        verbose_name_plural = _("carrinhos")

    def __str__(self):
        return f'user_id: {self.usuario.id} - item: {self.livro.titulo}' 


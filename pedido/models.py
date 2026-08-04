from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _


class Pedido(models.Model):
    usuario = models.ForeignKey(
        "accounts.Usuario",
        on_delete=models.PROTECT,
        related_name="pedidos",
    )

    endereco = models.ForeignKey(
        "pedido.EnderecoPedido",
        on_delete=models.PROTECT,
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    class Status(models.TextChoices):
        AGUARDANDO = "AG", _("Aguardando pagamento")
        PAGO = "PG", _("Pago")
        ENVIADO = "EV", _("Enviado")
        ENTREGUE = "ET", _("Entregue")
        CANCELADO = "CA", _("Cancelado")

    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.AGUARDANDO,
    )

    @property
    def total(self):
        return sum((item.subtotal for item in self.itens.all()), start=Decimal("0.00"))

    def __str__(self):
        return f"Pedido #{self.pk}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="itens",
    )

    livro = models.ForeignKey(
        "catalogo.Livro",
        on_delete=models.PROTECT,
    )

    quantidade = models.PositiveIntegerField(default=1)

    preco_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    @property
    def subtotal(self):
        return self.preco_unitario * self.quantidade

    def __str__(self):
        return self.livro.titulo


class EnderecoPedido(models.Model):
    """Model definition for EnderecoPedido."""

    # TODO: Define fields here
    cep = models.CharField(max_length=9)
    estado = models.CharField(max_length=2)
    cidade = models.CharField(max_length=50)
    bairro = models.CharField(max_length=50)
    rua = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True)
    referencia = models.CharField(max_length=200, blank=True)

    class Meta:
        """Meta definition for EnderecoPedido."""

        verbose_name = 'EnderecoPedido'
        verbose_name_plural = 'EnderecoPedidos'

    def __str__(self):
        """Unicode representation of EnderecoPedido."""
        return f"{self.rua}, {self.numero} - {self.cidade}/{self.estado}"


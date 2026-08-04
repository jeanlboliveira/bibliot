from django.contrib import admin
from .models import  Pedido, ItemPedido, EnderecoPedido
# Register your models here.

admin.site.register(Pedido)
admin.site.register(ItemPedido)
admin.site.register(EnderecoPedido)

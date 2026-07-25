from django.test import SimpleTestCase
from django.urls import resolve, reverse

from carrinho.views import adicionar_item_view, remover_item_view


class CarrinhoUrlsTest(SimpleTestCase):
    def test_url_de_remocao_resolve_para_view_de_remocao(self):
        url = reverse('carrinho:remover_item', kwargs={'livro_id': 7})

        self.assertEqual(url, '/remover/7/')
        self.assertEqual(resolve(url).func, remover_item_view)

    def test_url_de_adicao_resolve_para_view_de_adicao(self):
        url = reverse('carrinho:adicionar_item', kwargs={'livro_id': 7})

        self.assertEqual(url, '/adicionar/7/')
        self.assertEqual(resolve(url).func, adicionar_item_view)

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Endereco


class EnderecoViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='usuario@example.com',
            password='senha123',
            nome='Usuário Teste'
        )

    def test_adicionar_endereco_cria_endereco_e_redireciona(self):
        self.client.login(email='usuario@example.com', password='senha123')

        response = self.client.post(reverse('accounts:adicionar_endereco'), {
            'nome_completo': 'Maria da Silva',
            'cep': '01000-000',
            'estado': 'SP',
            'cidade': 'São Paulo',
            'bairro': 'Centro',
            'rua': 'Rua das Flores',
            'numero': '123',
            'complemento': 'Apto 1',
            'referencia': 'Perto do mercado',
            'principal': 'on',
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:profile'))
        self.assertTrue(Endereco.objects.filter(usuario=self.user).exists())

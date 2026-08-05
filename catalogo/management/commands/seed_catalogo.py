import os
import json
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from django.utils.text import slugify
from catalogo.models import Categoria, Autor, Livro

class Command(BaseCommand):
    help = 'Seed que cria registros e faz upload das capas baixadas'

    def handle(self, *args, **options):
        # Caminho onde estão as imagens (assumindo media/capas/)
        capas_dir = os.path.join(settings.MEDIA_ROOT, 'capas')
        if not os.path.exists(capas_dir):
            self.stdout.write(self.style.ERROR(f'Pasta {capas_dir} não encontrada. Crie-a e coloque as imagens lá.'))
            return

        # 1. Carregar categorias
        with open('catalogo/fixtures/categorias.json', 'r', encoding='utf-8') as f:
            categorias_data = json.load(f)
        self.stdout.write('--- Criando categorias ---')
        for cat_data in categorias_data:
            obj, created = Categoria.objects.get_or_create(
                nome=cat_data['nome'],
                defaults={
                    'descricao': cat_data['descricao'],
                    'ordem': cat_data['ordem']
                }
            )
            self.stdout.write(f"{'Criada' if created else 'Já existia'} categoria: {obj.nome}")

        # 2. Carregar autores
        with open('catalogo/fixtures/autores.json', 'r', encoding='utf-8') as f:
            autores_data = json.load(f)
        self.stdout.write('--- Criando autores ---')
        for aut_data in autores_data:
            obj, created = Autor.objects.get_or_create(
                nome=aut_data['nome'],
                defaults={
                    'descricao': aut_data.get('descricao', ''),
                    'nascimento': aut_data['nascimento'],
                    'morte': aut_data.get('morte'),
                    'foto': aut_data.get('foto')
                }
            )
            self.stdout.write(f"{'Criado' if created else 'Já existia'} autor: {obj.nome}")

        # 3. Carregar livros
        with open('catalogo/fixtures/livros.json', 'r', encoding='utf-8') as f:
            livros_data = json.load(f)
        self.stdout.write('--- Criando livros e fazendo upload das capas ---')
        for livro_data in livros_data:
            autor = Autor.objects.get(nome=livro_data['autor'])
            categoria = Categoria.objects.get(nome=livro_data['categoria'])

            livro, created = Livro.objects.get_or_create(
                isbn=livro_data['isbn'],
                defaults={
                    'titulo': livro_data['titulo'],
                    'autor': autor,
                    'preco': livro_data['preco'],
                    'sinopse': livro_data['sinopse'],
                    'lancamento': livro_data['lancamento']
                }
            )
            livro.categoria.add(categoria)

            # Verifica se o livro já tem capa; se não tiver, tenta fazer upload
            if not livro.capa:
                # Gera o nome do arquivo esperado (ex: slugify(titulo).jpg)
                nome_arquivo = f"{slugify(livro.titulo)}.jpg"
                caminho_arquivo = os.path.join(capas_dir, nome_arquivo)

                if os.path.exists(caminho_arquivo):
                    with open(caminho_arquivo, 'rb') as f:
                        livro.capa.save(nome_arquivo, File(f), save=True)
                    self.stdout.write(self.style.SUCCESS(f'  Capa carregada para "{livro.titulo}"'))
                else:
                    self.stdout.write(self.style.WARNING(f'  Arquivo de capa não encontrado: {nome_arquivo}'))
            else:
                self.stdout.write(f'  Capa já existe para "{livro.titulo}"')

            self.stdout.write(f"{'Criado' if created else 'Atualizado'} livro: {livro.titulo}")

        self.stdout.write(self.style.SUCCESS('\n✅ Seed concluído com sucesso!'))
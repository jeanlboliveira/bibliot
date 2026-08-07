import json
import requests
import os

from django.core.management.base import BaseCommand
from catalogo.models import Categoria, Autor, Livro
from dotenv import load_dotenv

load_dotenv()


class Command(BaseCommand):
    help = "Seed que cria categorias, autores e livros e busca automaticamente as capas"

    def buscar_capa_google_books(self, titulo, autor):
        """Busca capa na Google Books API por título + autor"""
        try:
            api_key = os.getenv("GOOGLE_BOOKS_API_KEY", "")
            
            query = f'intitle:"{titulo}"+inauthor:"{autor}"'
            url = "https://www.googleapis.com/books/v1/volumes"
            
            params = {
                "q": query,
                "maxResults": 1,
            }
            
            if api_key:
                params["key"] = api_key
            
            resposta = requests.get(url, params=params, timeout=10)
            
            if resposta.ok:
                dados = resposta.json()
                
                if dados.get("items"):
                    volume_info = dados["items"][0].get("volumeInfo", {})
                    image_links = volume_info.get("imageLinks", {})
                    
                    return image_links.get("thumbnail")
        
        except requests.RequestException as e:
            self.stdout.write(
                self.style.WARNING(f"⚠ Erro ao buscar capa de {titulo}: {e}")
            )
        
        return None

    def handle(self, *args, **options):
        # Categorias
        with open("catalogo/fixtures/categorias.json", encoding="utf-8") as f:
            categorias_data = json.load(f)

        self.stdout.write("--- Criando categorias ---")

        for cat_data in categorias_data:
            categoria, created = Categoria.objects.get_or_create(
                nome=cat_data["nome"],
                defaults={
                    "descricao": cat_data["descricao"],
                    "ordem": cat_data["ordem"],
                },
            )

            self.stdout.write(
                f"{'Criada' if created else 'Já existia'} categoria: {categoria.nome}"
            )

        # Autores
        with open("catalogo/fixtures/autores.json", encoding="utf-8") as f:
            autores_data = json.load(f)

        self.stdout.write("\n--- Criando autores ---")

        for autor_data in autores_data:
            autor, created = Autor.objects.get_or_create(
                nome=autor_data["nome"],
                defaults={
                    "descricao": autor_data.get("descricao", ""),
                    "nascimento": autor_data["nascimento"],
                    "morte": autor_data.get("morte"),
                    "foto": autor_data.get("foto"),
                },
            )

            self.stdout.write(
                f"{'Criado' if created else 'Já existia'} autor: {autor.nome}"
            )

        # Livros
        with open("catalogo/fixtures/livros.json", encoding="utf-8") as f:
            livros_data = json.load(f)

        self.stdout.write("\n--- Criando livros e buscando capas ---")

        for livro_data in livros_data:
            autor = Autor.objects.get(nome=livro_data["autor"])
            categoria = Categoria.objects.get(nome=livro_data["categoria"])

            livro, created = Livro.objects.get_or_create(
                isbn=livro_data["isbn"],
                defaults={
                    "titulo": livro_data["titulo"],
                    "autor": autor,
                    "preco": livro_data["preco"],
                    "sinopse": livro_data["sinopse"],
                    "lancamento": livro_data["lancamento"],
                    "capa": livro_data["capa"]
                },
            )

            livro.categoria.add(categoria)

            self.stdout.write(
                f"{'Criado' if created else 'Já existia'} livro: {livro.titulo}"
            )

        self.stdout.write(self.style.SUCCESS("\n✅ Seed concluído com sucesso!"))
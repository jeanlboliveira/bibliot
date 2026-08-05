import os
from django.core.management.base import BaseCommand
from django.core.files import File
from catalogo.models import Livro

class Command(BaseCommand):
    help = 'Associa capas baixadas manualmente aos livros (mapeamento exato)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--pasta',
            type=str,
            default='catalogo/fixtures/capas',
            help='Caminho da pasta com as imagens'
        )

    def handle(self, *args, **options):
        pasta = options['pasta']
        if not os.path.exists(pasta):
            self.stdout.write(self.style.ERROR(f'Pasta "{pasta}" não encontrada!'))
            return

        # Mapeamento título -> nome do arquivo (fornecido por você)
        MAPEAMENTO = {
            'Memórias Póstumas de Brás Cubas': 'memorias_postumas.jpg',
            'Dom Casmurro': 'dom_casmurro.jpg',
            'O Cortiço': 'o_cortico.jpg',
            'Gabriela, Cravo e Canela': 'gabriela.jpg',
            'Dona Flor e Seus Dois Maridos': 'dona_flor.jpg',
            'A Hora da Estrela': 'hora_estrela.jpg',
            'O Morro dos Ventos Uivantes': 'morro_ventos.jpg',
            'Orgulho e Preconceito': 'orgulho_preconceito.jpg',
            'Razão e Sensibilidade': 'razao_sensibilidade.jpg',
            'Cem Anos de Solidão': 'cem_anos.jpg',
            'O Amor nos Tempos do Cólera': 'amor_colera.jpg',
            'Melhor que nos Filmes': 'melhor_que_filmes.jpg',
            'O Verão que Mudou a Minha Vida': 'verao_mudou_minha_vida.jpg',
            'É Assim que Acaba': 'assim_acaba.jpg',
            'A Hipótese do Amor': 'hipotese_amor.jpg',
            'Neuromancer': 'neuromancer.jpg',
            '1984': '1984.jpg',
            'Fahrenheit 451': 'fahrenheit.jpg',
            'Admirável Mundo Novo': 'brave_new_world.jpg',
            'O Fim da Infância': 'fim_infancia.jpg',
            'Androides Sonham com Ovelhas Elétricas?': 'androides.jpg',
            'Fundação': 'fundacao.jpg',
            'Duna': 'duna.jpg',
            'Harry Potter e a Pedra Filosofal': 'harry_pedra.jpg',
            'Harry Potter e a Câmara Secreta': 'harry_camara.jpg',
            'Harry Potter e o Prisioneiro de Azkaban': 'harry_azkaban.jpg',
            'Harry Potter e o Cálice de Fogo': 'harry_calice.jpg',
            'Harry Potter e a Ordem da Fênix': 'harry_fenix.jpg',
            'Harry Potter e o Enigma do Príncipe': 'harry_enigma.jpg',
            'Harry Potter e as Relíquias da Morte': 'harry_reliquias.jpg',
            'O Hobbit': 'hobbit.jpg',
            'O Senhor dos Anéis: A Sociedade do Anel': 'lotr_anel.jpg',
            'O Senhor dos Anéis: As Duas Torres': 'lotr_torres.jpg',
            'O Senhor dos Anéis: O Retorno do Rei': 'lotr_rei.jpg',
            'A Guerra dos Tronos': 'guerra_tronos.jpg',
            'A Fúria dos Reis': 'furia_reis.jpg',
            'A Tormenta de Espadas': 'tormenta_espadas.jpg',
            'O Assassinato de Roger Ackroyd': 'roger_ackroyd.jpg',
            'O Cão dos Baskervilles': 'cao_baskerville.jpg',
            'O Mistério dos Diamantes': 'diamantes.jpg',
            'O Jogo da Amarelinha': 'amarelinha.jpg',
            'A Casa dos Espíritos': 'casa_espiritos.jpg',
            'O Código Da Vinci': 'codigo_da_vinci.jpg',
            'Anjos e Demônios': 'anjos_demonios.jpg',
            'Drácula': 'dracula.jpg',
            'Frankenstein': 'frankenstein.jpg',
            'O Iluminado': 'iluminado.jpg',
            'It - A Coisa': 'it.jpg',
            'O Chamado de Cthulhu': 'cthulhu.jpg',
            'A Queda da Casa de Usher': 'usher.jpg',
            'Carrie': 'carrie.jpg',
            'A Ilha do Tesouro': 'ilha_tesouro.jpg',
            'Viagem ao Centro da Terra': 'centro_terra.jpg',
            'Vinte Mil Léguas Submarinas': 'vinte_mil.jpg',
            'Robinson Crusoé': 'robinson.jpg',
            'As Aventuras de Huckleberry Finn': 'huckleberry.jpg',
            'Moby Dick': 'moby_dick.jpg',
            'O Grande Gatsby': 'great_gatsby.jpg',
            'A Letra Escarlate': 'letra_escarlate.jpg',
            'O Retrato de Dorian Gray': 'dorian_gray.jpg',
            'Tempos Difíceis': 'tempos_dificeis.jpg',
            'Pessoas Normais': 'pessoas_normais.jpg',
            'A Redoma de Vidro': 'redoma_vidro.jpg',
            'O Alienista': 'alienista.jpg',
            'A Comédia dos Erros': 'comedia_erros.jpg',
            'Muito Barulho por Nada': 'barulho_nada.jpg',
            'A Megera Domada': 'megera.jpg',
            'Os Contos de Canterbury': 'canterbury.jpg',
            'Dom Quixote': 'quixote.jpg',
            'Sapiens: Uma Breve História da Humanidade': 'sapiens.jpg',
            'Homo Deus: Uma Breve História do Amanhã': 'homo_deus.jpg',
            'A Bibliotecária de Auschwitz': 'bibliotecaria_auschwitz.jpg',
            'O Alquimista': 'alquimista.jpg',
            'O Pequeno Príncipe': 'pequeno_principe.jpg',
            'Meditações': 'meditacoes.jpg',
            'Assim Falou Zaratustra': 'zaratustra.jpg',
            'O Mundo de Sofia': 'mundo_sofia.jpg',
            'Clean Code: A Handbook of Agile Software Craftsmanship': 'clean_code.jpg',
            'O Programador Pragmático': 'pragmatic_programmer.jpg',
            'Estruturas de Dados e Algoritmos com JavaScript': 'estruturas_javascript.jpg',
            'Python para Análise de Dados': 'python_dados.jpg',
            'Introdução à Inteligência Artificial': 'ia_introducao.jpg',
            'O Poder do Hábito': 'poder_habito.jpg',
            'A Coragem de Não Agradar': 'coragem_nao_agradar.jpg',
            'O Milagre da Manhã': 'milagre_manha.jpg',
            'Verity': 'verity.jpg',
            'A Paciente Silenciosa': 'paciente_silenciosa.jpg',
            'O Conto da Aia': 'conto_aia.jpg',
            'Jogos Vorazes': 'jogos_vorazes.jpg',
        }

        livros = Livro.objects.all()
        total = livros.count()
        self.stdout.write(f'Processando {total} livros...')

        for livro in livros:
            nome_arquivo = MAPEAMENTO.get(livro.titulo)
            if not nome_arquivo:
                self.stdout.write(self.style.WARNING(f'⚠ Mapeamento não encontrado para: {livro.titulo}'))
                continue

            caminho = os.path.join(pasta, nome_arquivo)
            if os.path.exists(caminho):
                with open(caminho, 'rb') as f:
                    livro.capa.save(nome_arquivo, File(f), save=True)
                self.stdout.write(self.style.SUCCESS(f'✓ {livro.titulo} -> {nome_arquivo}'))
            else:
                self.stdout.write(self.style.WARNING(f'✗ Arquivo não encontrado: {caminho}'))

        self.stdout.write(self.style.SUCCESS('✅ Processo concluído!'))
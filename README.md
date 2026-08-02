# Bibliot

O *_Bibliot_* é um projeto de estudos onde busco consolidar os meus conhecimentos de Django, construindo uma livraria on-line do zero — do modelo de dados à interface, passando por autenticação, carrinho de compras dinâmico e boas práticas de front-end.

## Sobre o projeto

Mais do que um e-commerce funcional, o Bibliot é um espaço para praticar decisões reais de desenvolvimento: modelagem de relacionamentos entre apps, autenticação customizada, atualização de interface sem reload de página, e organização de CSS escalável.

## Funcionalidades

- **Catálogo de livros** organizado por categorias (relação muitos-para-muitos entre `Livro` e `Categoria`)
- **Página de detalhe do livro**, com autor, sinopse, preço e capa
- **Carrinho de compras dinâmico** — adicionar, remover e ajustar quantidade sem recarregar a página, via Fetch API
- **Autenticação por e-mail**, sem username, através de um Custom User Model
- **Cadastro de usuários** com validação de senha
- **Menu de conta com dropdown**, exibindo foto de perfil ou ícone padrão
- **Header fixo com busca** e placeholders dinâmicos animados
- **Painel administrativo** (Django Admin) para gestão de livros, autores, categorias e usuários

## Apps do projeto

| App | Responsabilidade |
|---|---|
| `core` | Página inicial, seções de destaque e exibição de categorias |
| `catalogo` | Models de `Livro`, `Autor` e `Categoria` |
| `accounts` | Autenticação, cadastro e model customizado de usuário |
| `carrinho` | Lógica do carrinho de compras (adicionar, remover, atualizar quantidade) |

## Tecnologias utilizadas

- **Backend:** Python / Django
- **Banco de dados:** SQLite (ambiente de desenvolvimento)
- **Frontend:** Django Templates, CSS com variáveis customizadas (design tokens), JavaScript puro (Fetch API, event delegation, debounce)

## Modelagem de dados

**Livro**
- Título, slug, ISBN, preço, sinopse, data de lançamento
- `ForeignKey` para `Autor`
- `ManyToManyField` para `Categoria`

**Autor**
- Nome, slug, biografia, datas de nascimento/morte, foto

**Categoria**
- Nome, slug, status de ativação, ordem de exibição

**Usuario** *(Custom User)*
- Autenticação via e-mail, sem username
- Nome, telefone, data de nascimento, foto de perfil

**Carrinho**
- Relaciona usuário e livro, com quantidade e subtotal calculado dinamicamente via `@property`
- Manager customizado com `adicionar_livro`, `remover_livro`, `diminuir_quantidade` e `limpar_carrinho`

## Decisões técnicas

- **Custom User desde o início** — evita a dificuldade de migrar de `User` padrão para um model customizado depois que o banco já está em produção
- **Managers customizados** para regras de negócio reutilizáveis (como "adicionar ao carrinho: cria ou incrementa"), mantendo a lógica fora das views
- **Atualizações dinâmicas via Fetch API**, com debounce para evitar requisições excessivas em cliques repetidos
- **CSS organizado por seções com variáveis centralizadas** (`variables.css`), evitando repetição de valores e facilitando ajustes de identidade visual

## Como rodar o projeto

```bash
# clonar o repositório
git clone <url-do-repositorio>
cd bibliot

# criar e ativar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac

# instalar dependências
pip install -r requirements.txt

# aplicar migrations
python manage.py migrate

# criar superusuário
python manage.py createsuperuser

# rodar o servidor
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/` no navegador.

## Status do projeto

Em desenvolvimento ativo — funcionalidades sendo implementadas de forma incremental como parte do processo de aprendizado.

## Autor

Jean Lucas — Curso Técnico Integrado em Informática, IFRN Campus Pau dos Ferros

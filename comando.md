```
# Tarefa: Limpeza e padronização do CSS do projeto Bibliot

## Objetivo
Revisar todos os templates (`.html`) e arquivos `.css` do projeto, removendo código morto/duplicado e padronizando tudo com o sistema de variáveis já existente em `variables.css`.

## Passo 1 — Levantamento
- Liste todos os arquivos `.css` do projeto e todos os templates que têm `{% block page_style %}` com CSS inline
- Identifique blocos de `page_style` que já foram movidos pro CSS global mas ainda estão duplicados no template (código morto)

## Passo 2 — Remover o que é inútil
- Regras CSS duplicadas (mesmo seletor definido em mais de um lugar)
- Seletores que não correspondem a nenhuma classe/id usada nos templates atuais (classes órfãs)
- Valores fixos (hex, px, rem) que já têm uma variável equivalente em `variables.css` — nesses casos, trocar pelo `var(--nome)` correspondente em vez de remover
- Comentários obsoletos ou blocos de CSS comentados sem uso

## Passo 3 — Padronizar com variáveis
- Qualquer cor, espaçamento, raio de borda, sombra, transição ou fonte que se repete deve usar a variável correspondente de `variables.css`
- Se encontrar um valor repetido que ainda não tem variável (ex: uma cor usada em 3+ lugares), sugerir a criação de uma nova variável em vez de manter hardcoded — mas pedir minha confirmação antes de criar
- Manter a nomenclatura de variáveis já em uso (`--espaco-*`, `--cor-*`, `--sombra-*`, `--transicao-*`, `--border-radius*`)

## Passo 4 — Modularizar em arquivos separados por seção
Organizar em arquivos separados por contexto, seguindo a estrutura:
```

static/css/

├── variables.css

├── base.css        (reset, header, nav, footer — global)

├── home.css

├── carrinho.css

├── wishlist.css

├── auth.css

└── styles.css       (importa todos os outros via @import)

```
- Mover cada bloco de CSS pro arquivo correspondente ao seu contexto
- `styles.css` deve conter apenas os `@import`, na ordem correta (variables primeiro, depois base, depois o resto)
- Remover todo CSS inline dos `{% block page_style %}` dos templates, já que tudo deve estar centralizado nesses arquivos

## Passo 5 — Validação
- Depois de mover tudo, confirme que nenhum template ficou sem estilo (rode o projeto e liste visualmente quais páginas você revisou)
- Aponte qualquer seletor que pareça não ter classe correspondente no HTML, mas NÃO remova sem confirmar comigo primeiro — pode ser algo usado dinamicamente via JavaScript (`classList.add`)

## Regras gerais
- Não altere a lógica ou estrutura dos templates `.html`, só o que está dentro de `{% block page_style %}`
- Antes de fazer qualquer remoção, me mostre um resumo do que será removido/movido
- Prefira commits pequenos e separados por etapa (ex: um commit só de "mover CSS pra arquivos separados", outro de "trocar valores fixos por variáveis")
```                                                                                                                                                                                                
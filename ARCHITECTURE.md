# Arquitetura

**Português** | [English](ARCHITECTURE.en.md)

Como uma LLM Wiki funciona: as camadas, as operações que o agente executa, as convenções do schema e o motivo de manter uma wiki em vez de fazer só RAG.

## Camadas

```
 fontes                 síntese                  regras
┌──────────┐  Ingest  ┌──────────────┐        ┌──────────────────┐
│  raw/    │ ───────▶ │    wiki/     │ ◀───── │ CLAUDE.md        │
│ imutável │          │ do agente    │        │ AGENTS.md        │
└──────────┘          └──────────────┘        │ (schema)         │
                        ▲        │             └──────────────────┘
                 Lint   │        │ Query
                        └────────┴──▶ respostas com citações
```

| Camada | Quem escreve | O que contém |
|---|---|---|
| `raw/` | você | Fontes originais (artigos, transcrições, PDFs, notas), **imutáveis**. O agente só lê. Anexos em `raw/assets/` |
| `wiki/` | o agente | Páginas em markdown: `projects/`, `concepts/`, `entities/`, `sources/`, mais `index.md` e `log.md` |
| `CLAUDE.md` / `AGENTS.md` | você + agente | O schema: domínio, estrutura, convenções e operações. Evolui com o uso. Os dois arquivos têm o mesmo conteúdo (Claude Code lê um, Codex e outros harnesses leem o outro) |

## Operações

**Ingest:** uma fonte nova entra em `raw/`.
1. O agente lê a fonte e discute os pontos principais com você (a menos que você peça ingest em lote).
2. Cria a página da fonte em `wiki/sources/`.
3. Atualiza as páginas afetadas. Uma fonte pode tocar várias.
4. Atualiza o `wiki/index.md` e acrescenta uma entrada `## [AAAA-MM-DD] ingest | Título` ao `wiki/log.md`.

**Query:** você faz uma pergunta.
1. O agente localiza as páginas pelo `index.md` e as lê.
2. Responde citando as páginas de fonte.
3. Se a resposta tiver valor duradouro (uma comparação, uma análise, uma conexão nova), oferece transformá-la em página.
4. Registra a consulta no `log.md`.

**Lint:** a manutenção. Tem duas metades:

| Tipo | Quem faz | Exemplos |
|---|---|---|
| Mecânico | `scripts/lint_wiki.py` (hook opcional + CI) | links quebrados, `.md` vazio, página fora do index, frontmatter, link sem extensão, exemplo `[[link]]` fora de crases, item repetido em lista do frontmatter, fonte sem ingest |
| Semântico | o agente, quando você pede | contradições entre páginas, afirmações superadas por fontes novas, páginas órfãs, conceitos sem página, referências cruzadas faltando |

## Schema e convenções

- **Frontmatter YAML** em toda página da wiki: `title`, `tags`, `date` (AAAA-MM-DD), `status` (`active`/`stale`/`archived`), `sources`. Listas com um item por linha, como o Obsidian grava (lista vazia: `[]`).
- **Wikilinks** no formato `[[Página]]`, com nome de arquivo igual ao título. Compatível com o Obsidian.
- **`index.md`** é o catálogo: toda página precisa estar lá. É por onde o agente (e você) começa.
- **`log.md`** é append-only: cada ingest, query, lint e setup vira uma entrada datada.
- **Proveniência (opcional):** ✅ decidido por você · 💡 sugerido pelo agente (não é decisão) · 🔎 verificado no ambiente. Evita que uma sugestão do agente vire "decisão" com o tempo.
- **Pastas novas** (ex.: `comparisons/`, `decisions/`) são bem-vindas: registre no schema quando criar.

## Por que wiki, e não só RAG

| | RAG | LLM Wiki |
|---|---|---|
| Quando sintetiza | a cada pergunta | uma vez, no ingest, e mantém |
| O que acumula | nada (índice de trechos) | páginas revisadas, ligações, contradições apontadas |
| Custo por pergunta | recuperar e sintetizar de novo | ler poucas páginas já sintetizadas |
| Auditável | difícil (trechos soltos) | sim: markdown versionado no git, com fontes citadas e log |
| Ponto fraco | perguntas que cruzam muitas fontes | exige disciplina de manutenção (daí o lint) |

As duas abordagens não se excluem: a wiki pode ser a camada curada por cima de uma busca nas fontes brutas.

## Ferramentas em volta

- **Lint** (`scripts/lint_wiki.py`): só stdlib e só leitura. Roda à mão, pelo hook opcional (`git config core.hooksPath .githooks`) ou no CI (Python 3.9 e 3.12). Detalhes no [README](README.md#lint).
- **Preset do Obsidian** (`obsidian-preset/`): opcional. Wikilinks, anexos em `raw/assets`, links atualizados ao renomear e grafo colorido por pasta. A `.obsidian/` real nunca é versionada.
- **Branches `example` / `example-en`**: uma wiki fictícia completa, para ver o schema aplicado. A `main` não recebe páginas de exemplo.
- **MemPalace** (opcional, externo): recall do histórico de conversas entre sessões. Não substitui a wiki.

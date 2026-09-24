# llm-wiki-mempalace

**Português** | [English](README.en.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)

Template pronto para instanciar uma **LLM Wiki**: uma base de conhecimento persistente e interligada em markdown, mantida por um agente de LLM (Claude Code, Codex, etc.), em vez de um RAG que rederiva tudo a cada pergunta. Inclui um schema genérico (`CLAUDE.md`/`AGENTS.md`) e, opcionalmente, um script para plugar o [MemPalace](https://github.com/MemPalace/mempalace) como camada de memória entre sessões.

## A ideia

A maioria das experiências de RAG (NotebookLM, uploads de arquivo no ChatGPT, etc.) recupera trechos relevantes na hora da pergunta, mas não acumula nada — cada pergunta subtil que exige sintetizar várias fontes força o LLM a reconstruir tudo do zero.

Aqui a lógica é outra: o agente **constrói e mantém uma wiki persistente**. Ao processar uma nova fonte, ele não só indexa — lê, extrai o que importa, e integra isso na wiki existente: atualiza páginas de entidades, revisa sínteses, aponta onde dados novos contradizem afirmações antigas. O conhecimento é compilado uma vez e **mantido atualizado**, não rederivado a cada consulta.

Ideia originalmente descrita por Andrej Karpathy no [gist `llm-wiki.md`](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). Este repositório é uma implementação pronta pra usar do padrão, mais a integração opcional com MemPalace que testamos e documentamos.

## Estrutura

```
.
├── CLAUDE.md             # schema — como o agente mantém a wiki (edite pro seu domínio)
├── AGENTS.md             # mesmo conteúdo, para Codex CLI / outros harnesses
├── raw/
│   ├── assets/            # imagens baixadas localmente (pasta de anexos do Obsidian, se usar)
│   └── ...                # fontes originais: transcrições, artigos, PDFs, notas
├── wiki/
│   ├── index.md           # catálogo de todas as páginas
│   ├── log.md              # log cronológico, append-only
│   ├── projects/
│   ├── concepts/
│   ├── entities/
│   └── sources/
└── scripts/
    └── setup_mempalace.py # opcional — ver seção MemPalace abaixo
```

## Uso rápido

1. Use este repositório como template (botão "Use this template" no GitHub) ou clone e apague o histórico do git.
2. Abra `CLAUDE.md` e substitua o placeholder `<domain>` — descreva o que essa wiki vai rastrear (pesquisa pessoal, um tópico, um livro, uma equipe, etc.) e ajuste as seções que não fizerem sentido pro seu caso.
3. (Opcional) Abra a pasta no Obsidian como vault — o schema já usa frontmatter YAML e wikilinks `[[Página]]` compatíveis.
4. Solte a primeira fonte em `raw/` e peça ao agente para rodar o fluxo de **Ingest** descrito no `CLAUDE.md`.

## MemPalace (opcional, memória entre sessões)

A wiki funciona sozinha — o MemPalace é uma camada adicional, e propositalmente **desacoplada**: ele resolve "não perder contexto entre sessões longas/reinícios do agente", nunca "como a wiki deve responder perguntas".

### Como as duas peças se encaixam

| | `wiki/` (este repo) | MemPalace |
|---|---|---|
| O que guarda | Síntese **curada**: só o que o agente decidiu que valia a pena virar página | Histórico **verbatim** de tudo — cada conversa, sem filtro |
| Onde vive | Dentro deste repositório, versionado no git | Fora de qualquer repo, num "palace" único por máquina (`~/.config/mempalace`), **compartilhado entre todos os seus projetos** — não é um palace por wiki |
| Você lê direto? | Sim — é markdown, abre no Obsidian, é o produto final | Não — é uma busca (`mempalace search`), não um lugar pra navegar |
| Quando o agente usa | Sempre, pra responder sobre o que **já está** documentado na wiki (`wiki/index.md`) | Só quando falta contexto que não chegou a virar página ainda — ex.: "o que discutimos sobre X na semana passada?" |

Na prática: a wiki é a "versão final" que você cultiva; o MemPalace é uma rede de segurança que evita perder o que ainda não foi promovido a página. Um source pode entrar direto pela wiki (fluxo de Ingest) sem nunca passar pelo MemPalace, e uma conversa pode ficar só no MemPalace pra sempre, se nada nela valer a pena virar página.

**Atenção ao instanciar este template mais de uma vez:** todo repositório na mesma máquina que rodar `setup_mempalace.py` cai no *mesmo* palace (`~/.config/mempalace`) — não é um banco isolado por wiki. Se você criar uma segunda wiki a partir deste template (outro domínio, outro projeto) e rodar o setup nela também, as duas vão compartilhar a mesma memória, e uma busca feita numa consegue trazer conteúdo da outra. Se precisar de isolamento real entre wikis, aponte `palace_path` pra um caminho diferente em cada uma (ver `config.json` do MemPalace) ou use máquinas/perfis separados.

```
python scripts/setup_mempalace.py --dry-run   # ver o que mudaria
python scripts/setup_mempalace.py             # aplicar
```

O script:
- Instala o CLI `mempalace` se não estiver disponível (`uv` → `pipx` → `pip`, o que existir).
- Configura hooks globais do Claude Code (`Stop`/`SessionEnd`/`PreCompact`) usando o comando nativo `mempalace hook run` — sem depender de scripts `.sh`, então funciona igual em Windows/Linux/macOS.
- Adiciona uma nota mínima de recall no `~/.claude/CLAUDE.md` global (idempotente).

O que ele **não** faz automaticamente (decisão sua, quando quiser):
```
mempalace mine ~/.claude/projects/ --mode convos   # minerar conversas passadas
mempalace mine <pasta-do-projeto>                    # minerar código/docs de um projeto
```

Também não registra o bloco `mempalace rules` (protocolo completo de coordenação multi-agente, MCP com 45 ferramentas) — isso é escopo bem maior do que "memória entre sessões", e criaria acoplamento que este template evita de propósito. Se você quiser isso, é uma decisão separada (`mempalace rules --help`).

## Créditos

- Padrão da LLM Wiki: Andrej Karpathy.
- MemPalace: [MemPalace/mempalace](https://github.com/MemPalace/mempalace) (MIT).
- Este template foi montado com [Claude Code](https://claude.com/claude-code).

## Licença

MIT — veja [LICENSE](LICENSE).

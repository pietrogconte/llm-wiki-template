# llm-wiki-template

**Português** | [English](README.en.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Template pronto para instanciar uma **LLM Wiki**: uma base de conhecimento persistente e interligada em markdown, mantida por um agente de LLM (Claude Code, Codex, etc.), em vez de um RAG que rederiva tudo a cada pergunta. Inclui um schema genérico (`CLAUDE.md`/`AGENTS.md`) e a estrutura de pastas pronta.

## A ideia

A maioria das experiências de RAG (NotebookLM, uploads de arquivo no ChatGPT, etc.) recupera trechos relevantes na hora da pergunta, mas não acumula nada — cada pergunta subtil que exige sintetizar várias fontes força o LLM a reconstruir tudo do zero.

Aqui a lógica é outra: o agente **constrói e mantém uma wiki persistente**. Ao processar uma nova fonte, ele não só indexa — lê, extrai o que importa, e integra isso na wiki existente: atualiza páginas de entidades, revisa sínteses, aponta onde dados novos contradizem afirmações antigas. O conhecimento é compilado uma vez e **mantido atualizado**, não rederivado a cada consulta.

Ideia originalmente descrita por Andrej Karpathy no [gist `llm-wiki.md`](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). Este repositório é uma implementação pronta pra usar do padrão.

## Estrutura

```
.
├── CLAUDE.md             # schema — como o agente mantém a wiki (edite pro seu domínio)
├── AGENTS.md             # mesmo conteúdo, para Codex CLI / outros harnesses
├── raw/
│   ├── assets/            # imagens baixadas localmente (pasta de anexos do Obsidian, se usar)
│   └── ...                # fontes originais: transcrições, artigos, PDFs, notas
└── wiki/
    ├── index.md           # catálogo de todas as páginas
    ├── log.md              # log cronológico, append-only
    ├── projects/
    ├── concepts/
    ├── entities/
    └── sources/
```

## Uso rápido

1. Use este repositório como template (botão "Use this template" no GitHub) ou clone e apague o histórico do git.
2. Abra `CLAUDE.md` e substitua o placeholder `<domain>` — descreva o que essa wiki vai rastrear (pesquisa pessoal, um tópico, um livro, uma equipe, etc.) e ajuste as seções que não fizerem sentido pro seu caso.
3. (Opcional) Abra a pasta no Obsidian como vault — o schema já usa frontmatter YAML e wikilinks `[[Página]]` compatíveis.
4. Solte a primeira fonte em `raw/` e peça ao agente para rodar o fluxo de **Ingest** descrito no `CLAUDE.md`.

## Opcional: memória entre sessões

A wiki funciona sozinha. Se quiser que o agente não perca contexto entre sessões longas ou reinícios, dá pra combinar com o [MemPalace](https://github.com/MemPalace/mempalace) — que é configurado uma vez por máquina, não por wiki: veja [pietrogconte/mempalace-setup](https://github.com/pietrogconte/mempalace-setup). A wiki continua sendo a síntese curada; o MemPalace é só recall do histórico de conversas.

## Créditos

- Padrão da LLM Wiki: Andrej Karpathy.
- Este template foi montado com [Claude Code](https://claude.com/claude-code).

## Licença

MIT — veja [LICENSE](LICENSE).

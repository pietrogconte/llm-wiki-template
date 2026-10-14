# llm-wiki-template

**Português** | [English](README.en.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/pietrogconte/llm-wiki-template/blob/main/LICENSE)

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
3. (Opcional) Abra a pasta no Obsidian como vault (veja [Usando com o Obsidian](#usando-com-o-obsidian)).
4. Solte a primeira fonte em `raw/` e peça ao agente para rodar o fluxo de **Ingest** descrito no `CLAUDE.md`.

## Usando com o Obsidian

O Obsidian é um bom leitor para a wiki: o agente escreve, você lê e navega.

1. **Instalação (Windows):** `winget install --id Obsidian.Obsidian -e --source winget`. O instalador é assinado digitalmente (Dynalist Inc), então não esbarra no Smart App Control.
2. **Abra a raiz do repo como cofre** (*Open folder as vault*), não só `wiki/`. As páginas apontam para `raw/` (fontes e anexos em `raw/assets/`), e o `CLAUDE.md` fica à mão. A pasta `.obsidian/` já está no `.gitignore`.
3. **Configurações** (*Settings → Files and links*): **Use `[[Wikilinks]]`** ligado; anexos em `raw/assets`; **Automatically update internal links** ligado. Renomear uma página conta como edição manual (veja o item 6).
4. **Navegação:** comece pelo `wiki/index.md` (catálogo); o `wiki/log.md` tem o histórico. Use o Quick Switcher (`Ctrl+O`), a busca (`Ctrl+Shift+F`), o painel de **backlinks**, o **Graph View** (`Ctrl+G`) e o grafo local (`Ctrl+P` → "Open local graph"). O frontmatter aparece como *Properties*; clique numa tag para listar as páginas com ela. Atenção: clicar num link para uma página inexistente cria um arquivo vazio.
5. **Como ler:** `projects/` tem um projeto ou linha de pesquisa por página; `concepts/` e `entities/` guardam o que aparece em 2+ projetos; `sources/` tem um resumo por fonte; `raw/` guarda as fontes originais, imutáveis. Se o seu schema marcar a proveniência, por exemplo ✅ decidido por você, 💡 sugerido pelo agente e 🔎 verificado, ponha a legenda no topo das páginas.
6. **Fluxo:** quem escreve a wiki é o agente (Ingest, Query e Lint, conforme o `CLAUDE.md`). Se você editar algo à mão, commite pelo terminal e avise o agente na próxima sessão. Nunca edite `raw/`.
7. **Git pelo terminal:**
   ```bash
   git status
   git add -A
   git diff --cached   # revise o que vai entrar (nada de segredos)
   git commit -m "Descreve a mudança"
   git push
   ```
   Plugins da comunidade (inclusive o *Obsidian Git*) são código de terceiros com acesso ao cofre inteiro. Mantenha o **modo restrito** ligado e só instale algo depois de revisar.
8. **Perguntas à wiki:** peça ao agente uma **Query**, citando as páginas relevantes (ex.: "Faça uma Query sobre X, considerando `[[Página A]]` e `[[Página B]]`"). Ele responde com citações, registra a consulta no `log.md` e oferece transformar respostas de valor duradouro em página nova.

## Opcional: memória entre sessões

A wiki funciona sozinha. Se quiser que o agente não perca contexto entre sessões longas ou reinícios, dá pra combinar com o [MemPalace](https://github.com/MemPalace/mempalace) — que é configurado uma vez por máquina, não por wiki: veja [pietrogconte/mempalace-setup](https://github.com/pietrogconte/mempalace-setup). A wiki continua sendo a síntese curada; o MemPalace é só recall do histórico de conversas.

## Créditos

- Padrão da LLM Wiki: Andrej Karpathy.
- Este template foi montado com [Claude Code](https://claude.com/claude-code).

## Licença

MIT — veja o arquivo `LICENSE` na raiz do repositório.

# Log

Log cronológico, append-only, de toda operação na wiki (ingest, query, lint, setup). Para ver as últimas entradas no terminal: `grep "^## \[" wiki/log.md | tail -5`

## [2026-01-03] setup | Wiki criada

Estrutura criada a partir do `llm-wiki-template`. Domínio: panificação caseira. Conteúdo em português. Sem MemPalace.

## [2026-01-10] ingest | 2026-01-10 Diário de alimentação do levain

- Páginas novas: [[2026-01-10 Diário de alimentação do levain]], [[Pão de fermentação natural]], [[Fermentação natural]].

## [2026-01-24] ingest | 2026-01-24 Teste de hidratação 70 vs 75

- Páginas novas: [[2026-01-24 Teste de hidratação 70 vs 75]], [[Hidratação]], [[Panela de ferro fundido]], [[Temperatura de fermentação]]. ✅ 70% como padrão do pão.

## [2026-02-07] ingest | 2026-02-07 Autólise de 30 minutos

- Página nova: [[Autólise]]. Atualizado: [[Pão de fermentação natural]].

## [2026-02-14] ingest | 2026-02-14 Primeira pizza napolitana

- Páginas novas: [[Pizza napolitana]], [[Pedra de pizza]], [[Farinha tipo 00]], [[Forno doméstico]], [[Reação de Maillard]].

## [2026-02-21] ingest | 2026-02-21 Farinha 00 e valor W

- Página nova: [[Força da farinha]]. Atualizado: [[Farinha tipo 00]].

## [2026-02-28] ingest | 2026-02-28 Termômetro de forno

- Atualizado: [[Forno doméstico]] (🔎 temperatura real medida). Repercute em [[Pizza napolitana]].

## [2026-03-07] ingest | 2026-03-07 Focaccia de alta hidratação

- Página nova: [[Focaccia]]. Atualizados: [[Hidratação]], [[Autólise]].

## [2026-03-14] ingest | 2026-03-14 Fermentação a frio

- Atualizado: [[Temperatura de fermentação]] (fermentação a frio). Repercute em [[Focaccia]].

## [2026-03-20] query | Por que a pizza saiu com o fundo pálido?

Resposta a partir de [[Forno doméstico]] e [[Pedra de pizza]]: o forno real é ~20 °C mais frio que o mostrador. 💡 registrado em [[Pizza napolitana]].

## [2026-04-04] ingest | 2026-04-04 Primeiro panetone

- Página nova: [[Panetone]]. Atualizados: [[Fermentação natural]], [[Força da farinha]].

## [2026-04-18] ingest | 2026-04-18 Douradura da casca

- Atualizado: [[Reação de Maillard]]. Repercute em [[Panetone]] (topo escuro).

## [2026-04-18] lint | Checagem

`python scripts/lint_wiki.py --strict`: 0 erros, 0 avisos. Semântica: [[Temperatura de fermentação]], [[Reação de Maillard]] e [[Forno doméstico]] viraram hubs (citados pelos quatro projetos).

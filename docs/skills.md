# Índice de skills

Fonte de execução: `.agents/skills/<nome>/SKILL.md`. O agente deve ler as instruções adequadas; o nome no catálogo sozinho não executa um procedimento. Cada arquivo informa sua versão. ae-diagramar 0.3.0 e ae-revisar 0.2.0 exigem a auditoria do PDF final e os cliques antes da entrega. O titular aprovou o layout; a validação pedagógica pelo leitor permanece pendente.

| Skill | Finalidade | Evidência disponível e limite |
|---|---|---|
| [ae-orquestrar](../.agents/skills/ae-orquestrar/SKILL.md) | Conduzir um pedido de material de concurso do briefing à entrega | fluxo inicial produziu o piloto; retomada independente ainda sem teste registrado |
| [ae-analisar-edital](../.agents/skills/ae-analisar-edital/SKILL.md) | Identificar concurso e converter edital em cobertura rastreável | recorte Dataprev mapeado; edital completo, OCR e retificações exigem outros casos |
| [ae-pesquisar-fontes](../.agents/skills/ae-pesquisar-fontes/SKILL.md) | Pesquisar e registrar fontes de conteúdo com proveniência | fontes do piloto registradas; atualização sistemática pendente |
| [ae-curar-referencias](../.agents/skills/ae-curar-referencias/SKILL.md) | Selecionar modelos de escrita e apresentação editorial | catálogo inicial aplicado; comparação de capítulos completos pendente |
| [ae-analisar-banca](../.agents/skills/ae-analisar-banca/SKILL.md) | Construir um perfil de prova baseado em amostra explícita | dez itens selecionados em duas provas; não há calibração estatística |
| [ae-escrever-capitulo](../.agents/skills/ae-escrever-capitulo/SKILL.md) | Redigir um capítulo didático com teoria desenvolvida e prática | capítulo SQL produzido; avaliação do leitor pendente |
| [ae-ilustrar](../.agents/skills/ae-ilustrar/SKILL.md) | Produzir ou selecionar representações visuais didáticas verificadas | três esquemas SQL e demonstração de switch; modelos reais e outras matérias não validados |
| [ae-questoes-reais](../.agents/skills/ae-questoes-reais/SKILL.md) | Selecionar e conferir questões autênticas com gabarito oficial | três referências oficiais no piloto, com gabarito preliminar explícito |
| [ae-questoes-autorais](../.agents/skills/ae-questoes-autorais/SKILL.md) | Criar itens originais coerentes com objetivos e perfil observado | oito itens no piloto; dificuldade editorial estimada, sem aplicação com alunos |
| [ae-diagramar](../.agents/skills/ae-diagramar/SKILL.md) | Montar apostilas e cadernos navegáveis em HTML e PDF | 0.3.0 aplicada a quatro PDFs; layout aprovado, 118 entradas e 217 áreas conferidas; acessibilidade e novos casos pendentes |
| [ae-revisar](../.agents/skills/ae-revisar/SKILL.md) | Revisar precisão, didática, questões e artefatos finais | 0.2.0 aplicada: rotas, coordenadas, cliques e hashes; 26 testes de navegação; acessibilidade e aceite pedagógico pendentes |
| [ae-gerenciar](../.agents/skills/ae-gerenciar/SKILL.md) | Manter progresso, decisões, backlog e documentação no Segundo Cérebro | notas e entregas no Drive conferidas; publicação GitHub impedida |
| [ae-curar-acervo](../.agents/skills/ae-curar-acervo/SKILL.md) | Importar, buscar, deduplicar e versionar questões | 17 itens em dois materiais; filtros, idempotência e revisões testados; fonte oficial ainda exige consulta do agente |

Ordem usual: orquestrar → edital/fontes/perfil → plano → escrita/figuras/questões → revisão → diagramação → gestão. A curadoria editorial melhora os padrões antes de escalar. As skills são modulares para reutilização; não exigem múltiplos agentes.

As evidências descrevem partes do fluxo observadas nos artefatos, sem certificar validação operacional completa de cada procedimento. Há 13 skills locais: 12 da fundação e ae-curar-acervo, implementada junto da ferramenta. Quatro candidatas permanecem em [prontidão](prontidao.md): simulado, revisão, atualização e acessibilidade. ae-diagramar tem uso validado com ressalvas para apostila/caderno nos casos testados; sua aprovação visual não certifica acessibilidade integral ou aprendizagem. Não há instalação global presumida.

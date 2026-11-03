# Índice de skills

Fonte de execução: `.agents/skills/<nome>/SKILL.md`. O agente deve ler as instruções adequadas; o nome no catálogo sozinho não executa um procedimento. Cada arquivo informa sua versão. ae-diagramar 0.5.0 e ae-revisar 0.4.0 exigem a auditoria do PDF final e os cliques antes da entrega. O titular aprovou o layout; a validação pedagógica pelo leitor permanece pendente.

| Skill | Finalidade | Evidência disponível e limite |
|---|---|---|
| [ae-orquestrar](../.agents/skills/ae-orquestrar/SKILL.md) | Conduzir um pedido de material de concurso do briefing à entrega | fluxo inicial produziu o piloto; retomada do estado 0.4 e reprodução pela CI registradas; novos casos exigem revisão |
| [ae-analisar-edital](../.agents/skills/ae-analisar-edital/SKILL.md) | Identificar concurso e converter edital em cobertura rastreável | recorte Dataprev mapeado; edital completo, OCR e retificações exigem outros casos |
| [ae-pesquisar-fontes](../.agents/skills/ae-pesquisar-fontes/SKILL.md) | Pesquisar e registrar fontes de conteúdo com proveniência | fontes do piloto registradas; atualização sistemática pendente |
| [ae-curar-referencias](../.agents/skills/ae-curar-referencias/SKILL.md) | Selecionar modelos de escrita e apresentação editorial | dois capítulos abertos comparados em páginas PDF representativas; ver curadoria-editorial-aplicada.md |
| [ae-analisar-banca](../.agents/skills/ae-analisar-banca/SKILL.md) | Construir um perfil de prova baseado em amostra explícita | dez itens selecionados em duas provas; não há calibração estatística |
| [ae-escrever-capitulo](../.agents/skills/ae-escrever-capitulo/SKILL.md) | Redigir um capítulo didático com teoria desenvolvida e prática | capítulo SQL produzido; avaliação do leitor pendente |
| [ae-ilustrar](../.agents/skills/ae-ilustrar/SKILL.md) | Produzir ou selecionar representações visuais didáticas verificadas | esquemas SQL e painel genérico detalhado revisados; modelos comerciais exigem seu manual |
| [ae-questoes-reais](../.agents/skills/ae-questoes-reais/SKILL.md) | Selecionar e conferir questões autênticas com gabarito oficial | três referências oficiais no piloto, com gabarito preliminar explícito |
| [ae-questoes-autorais](../.agents/skills/ae-questoes-autorais/SKILL.md) | Criar itens originais coerentes com objetivos e perfil observado | oito itens no piloto; dificuldade editorial estimada, sem aplicação com alunos |
| [ae-diagramar](../.agents/skills/ae-diagramar/SKILL.md) | Montar apostilas e cadernos navegáveis em HTML e PDF | 0.5.0 aplica quatro formatos e auditoria, mantendo navegação/--final; versão anterior aplicada a quatro PDFs; layout aprovado, 118 entradas e 217 áreas conferidas; acessibilidade e novos casos pendentes |
| [ae-revisar](../.agents/skills/ae-revisar/SKILL.md) | Revisar precisão, didática, questões e artefatos finais | 0.4.0 confere formatos/edições/acessibilidade e fidelidade/cobertura; rotas, coordenadas, cliques e hashes conferidos; 26 testes de navegação; acessibilidade e aceite pedagógico pendentes |
| [ae-gerenciar](../.agents/skills/ae-gerenciar/SKILL.md) | Manter progresso, decisões, backlog e documentação no Segundo Cérebro | notas e entregas no Drive conferidas; publicação e CI GitHub confirmadas |
| [ae-curar-acervo](../.agents/skills/ae-curar-acervo/SKILL.md) | Importar, buscar, deduplicar e versionar questões | 17 itens em dois materiais; filtros, idempotência e revisões testados; fonte oficial ainda exige consulta do agente |

| [ae-montar-simulado](../.agents/skills/ae-montar-simulado/SKILL.md) | Matriz, aplicação e pontuação | exemplar com seis questões e testes de pesos/anulações; treino autoral explícito |
| [ae-produzir-revisao](../.agents/skills/ae-produzir-revisao/SKILL.md) | Recuperação ativa e síntese | revisão de matemática com remissões locais; avaliação de utilidade pelo leitor pendente |
| [ae-atualizar-material](../.agents/skills/ae-atualizar-material/SKILL.md) | Impacto, edição e errata | mudanças de conteúdo/fontes/IDs testadas; gabaritos alterados nos testes são sintéticos |
| [ae-auditar-acessibilidade](../.agents/skills/ae-auditar-acessibilidade/SKILL.md) | Teclado, contraste, descrições e estrutura | auditoria executada e marcação corrigida; limites assistivos explícitos |

O fluxo agora começa por texto/foto/print, lê todas as skills e segue [do-pedido-a-entrega.md](do-pedido-a-entrega.md). Foram atualizadas também ae-orquestrar, ae-analisar-edital, ae-pesquisar-fontes, ae-analisar-banca e ae-escrever-capitulo para 0.2.0. Não há nova skill duplicando a orquestração. A ingestão e o contrato final têm testes; uma nova solicitação real completa ainda precisa aplicar o fluxo de ponta a ponta.

Ordem usual: orquestrar → edital/fontes/perfil → plano → escrita/figuras/questões → revisão → diagramação → gestão. A curadoria editorial melhora os padrões antes de escalar. As skills são modulares para reutilização; não exigem múltiplos agentes.

As evidências descrevem partes observadas, sem certificar aplicação universal. Há 17 skills locais: 12 da fundação, ae-curar-acervo e quatro módulos implementados junto das ferramentas de simulado, revisão, edições e acessibilidade. A [prontidão](prontidao.md) distingue base operacional, aplicação por caso e avaliação pelo leitor. Não há instalação global presumida.

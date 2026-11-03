# Índice de skills

Fonte executável: `.agents/skills/<nome>/SKILL.md`. O agente lê todas as skills ao retomar um pedido e registra a versão consultada; o nome no índice não executa o procedimento. São 17 skills locais, aplicadas na validação 0.6. A [matriz de validação](validacao-skills-v06.md) registra evidência por procedimento e seus limites.

| Skill | Finalidade |
|---|---|
| [ae-orquestrar](../.agents/skills/ae-orquestrar/SKILL.md) | Conduzir identificação, pesquisa, produção, revisão e entrega |
| [ae-analisar-edital](../.agents/skills/ae-analisar-edital/SKILL.md) | Conferir identidade, retificações e programa literal, inclusive continuação de prints |
| [ae-pesquisar-fontes](../.agents/skills/ae-pesquisar-fontes/SKILL.md) | Pesquisar fontes com proveniência, localizadores e datas |
| [ae-curar-referencias](../.agents/skills/ae-curar-referencias/SKILL.md) | Aplicar modelos de escrita e apresentação editorial |
| [ae-analisar-banca](../.agents/skills/ae-analisar-banca/SKILL.md) | Analisar amostra explícita de provas e seus limites |
| [ae-escrever-capitulo](../.agents/skills/ae-escrever-capitulo/SKILL.md) | Redigir teoria desenvolvida, exemplos e prática |
| [ae-ilustrar](../.agents/skills/ae-ilustrar/SKILL.md) | Criar figuras didáticas, descritas e rastreáveis |
| [ae-questoes-reais](../.agents/skills/ae-questoes-reais/SKILL.md) | Conferir questões autênticas e gabarito oficial |
| [ae-questoes-autorais](../.agents/skills/ae-questoes-autorais/SKILL.md) | Elaborar itens e distratores coerentes com os objetivos |
| [ae-diagramar](../.agents/skills/ae-diagramar/SKILL.md) | Exportar os quatro formatos com recursos e links auditados |
| [ae-revisar](../.agents/skills/ae-revisar/SKILL.md) | Fazer segunda passagem técnica/editorial e conferir artefatos |
| [ae-gerenciar](../.agents/skills/ae-gerenciar/SKILL.md) | Manter progresso, decisões, backlog e cofre com confirmação |
| [ae-curar-acervo](../.agents/skills/ae-curar-acervo/SKILL.md) | Buscar, deduplicar, importar e preservar revisões de questões |
| [ae-montar-simulado](../.agents/skills/ae-montar-simulado/SKILL.md) | Montar matriz, aplicação e pontuação |
| [ae-produzir-revisao](../.agents/skills/ae-produzir-revisao/SKILL.md) | Propor recuperação ativa e remissões à teoria |
| [ae-atualizar-material](../.agents/skills/ae-atualizar-material/SKILL.md) | Comparar edições, propagar impacto de figuras e registrar errata |
| [ae-auditar-acessibilidade](../.agents/skills/ae-auditar-acessibilidade/SKILL.md) | Medir teclado, contraste, descrições e estrutura com limites |

ae-diagramar 0.6.0 valida recursos de todos os textos antes de incorporá-los; ae-atualizar-material 0.2.0 rastreia figuras e seus usos; ae-revisar 0.5.0 reforça a segunda passagem e os distratores; ae-analisar-edital 0.3.0 distingue o trecho visível da continuação pesquisada. As demais versões constam em seus arquivos.

Ordem usual: orquestração → edital/fontes/perfil → plano → escrita/figuras/questões → revisão → diagramação → gestão. A revisão pode exigir retorno às etapas anteriores. Os procedimentos são modulares e não exigem múltiplos agentes.

Os cartões podem ser classificados conservadoramente como `active-with-caveats` após confirmar seus registros: houve aplicação prática delimitada, sem instalação global, calibração estatística da dificuldade ou aprovação pedagógica presumida. Cada matéria exige pesquisa e revisão próprias. Não há skill obrigatória ainda por criar para o escopo atual; a continuidade é conteúdo sob demanda e retorno do leitor.

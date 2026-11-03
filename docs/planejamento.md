# Plano do produto editorial

## Resultado pretendido

Transformar um pedido de estudo em uma coleção consistente de apostilas, capítulos, cadernos de questões e revisões. O agente consulta instruções versionadas e fontes, produz um lote delimitado, verifica o resultado e deixa o estado pronto para a próxima tarefa.

## Perfis de entrega

| Tipo | Conteúdo mínimo | Navegação |
|---|---|---|
| Apostila completa | mapa do edital, fundamentos, desenvolvimento, figuras, exemplos resolvidos, prática, síntese e glossário | sumário, capítulos, figuras e questões ↔ resoluções |
| Capítulo temático | objetivos, pré-requisitos, teoria desenvolvida e prática progressiva | sumário local e referências |
| Caderno de questões | instruções, origem de cada item, reais e autorais identificadas, gabarito e comentários | cada questão ↔ resolução; resolução → teoria |
| Simulado | matriz de distribuição, regras da prova, bloco sem respostas e gabarito separado | instruções → questões → respostas; sem revelar resposta no enunciado |
| Revisão | relações essenciais, erros frequentes e recuperação ativa | remissão ao capítulo completo |

## Requisitos priorizados por dependência

| ID | Requisito | Evidência de aceite |
|---|---|---|
| R01 | carregar contexto e skills ao iniciar | registro de leitura e plano de execução |
| R02 | identificar edital e retificações | briefing com URLs, versões, data e lacunas |
| R03 | adequar a estrutura ao conteúdo programático | matriz item do edital → objetivo → capítulo → questão |
| R04 | explicação didática desenvolvida | revisão da sequência conceito → mecanismo → exemplo → prática |
| R05 | imagens didáticas rotuladas | manifesto com propósito, legenda, descrição e direitos |
| R06 | questões reais autênticas | prova, caderno, item, gabarito e status conferidos |
| R07 | questões autorais coerentes com a amostra | perfil de banca, matriz cognitiva e revisão de alternativas |
| R08 | links funcionais em HTML e PDF | sumário e 100% dos pares questão/resolução testados |
| R09 | qualidade editorial estável | checklist preenchido, sem defeitos críticos abertos |
| R10 | gestão e continuidade | Progress, Decisions e registro no cofre com evidência |
| R11 | pesquisa de forma editorial | catálogo de referências com padrões adotados e direitos |
| R12 | reprodutibilidade | instruções de build, versões e manifesto da entrega |

## Escopo da primeira etapa

Entregar estrutura, procedimentos utilizáveis, referências pesquisadas, modelos, contratos de dados, roadmap e uma pequena prova de navegação. Não produzir a apostila de um concurso sem que ele seja identificado. Não pressupor aplicativo web ou agente em execução permanente.

## Condição para encerrar o piloto futuro

Um concurso identificado, um recorte do edital, um capítulo revisado, figuras rotuladas, questões reais verificadas disponíveis por link ou reprodução permitida, autorais identificadas, gabarito comentado, HTML e PDF com links conferidos e avaliação do titular. Medir defeitos e tempo do ciclo; não prometer aprovação no concurso ou equivalência psicométrica.

## Estratégia de produção

Trabalhar por capítulo, validar e incorporar correções no manual antes de escalar. Reutilizar explicações e figuras somente quando escopo, atualização e direitos permitirem. Comparar uma versão didática extensa e uma revisão curta no piloto para ajustar densidade, sem fixar número de páginas antes do conteúdo.

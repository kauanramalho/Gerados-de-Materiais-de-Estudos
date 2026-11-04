# Progresso — Ateliê de Estudos

- **Estado:** active — desenvolvimento técnico 0.6 entregue; produção CRECI-ES validada; avaliação pelo leitor em acompanhamento.
- **Prioridade no portfólio:** unassigned.
- **Data do estado:** 2026-11-04.
- **Próxima ação:** registrar tentativa e retorno real do leitor sobre clareza, aprendizagem e dificuldade (AE-009), agora também com a edição CRECI-ES; confirmar a fonte primária da alteração Cofeci 1573/2026 quando acessível.
- **Responsável:** agente pela produção, correções e documentação; titular pelo seu retorno de leitura.
- **Condição técnica atendida:** AE-026/027 corrigidos, caso escolhido com cobertura integral da matéria e aplicação delimitada das 17 skills.
- **Condição ainda aberta para encerrar a avaliação do projeto:** retorno real do leitor; aprovação visual anterior não substitui essa avaliação.
- **GitHub:** [repositório público do titular](https://github.com/kauanramalho/Gerados-de-Materiais-de-Estudos), com histórico inicial preservado. O relatório de cada publicação registra o SHA e a CI efetivamente conferidos.

## Produção CRECI-ES — 04/11/2026

Pedido textual do titular: apostila de conteúdo e caderno de questões para PAS — Analista de T.I., código 407, Vitória, Edital 1/2026, banca Quadrix. Pesquisa iniciada em 03/11 e entrega verificada em 04/11. Todo o programa aplicável foi mapeado: **111 pontos de conhecimentos e uma exigência discursiva**, incluindo Inglês em substituição à informática comum.

- Apostila de **325 páginas**, com **56 capítulos e 25 figuras originais**; caderno de **194 páginas**, com orientações, prática e comentários, sem capítulos expositivos.
- **273 questões autorais**, incluindo seis propostas discursivas com modelo, e **40 referências reais** da Quadrix, com gabaritos definitivos conferidos por cargo. Direitos não confirmados: acesso ao original, sem transcrição de terceiros.
- **143 testes**, 34 verificações de exemplos, 1.775 links internos PDF e 2.195 cliques no HTML correspondente aprovados; **60 URLs externas** responderam à checagem datada. Acessibilidade técnica passou com limites declarados; houve varredura de diagramação e ampliações amostradas.
- Pacote privado preserva fontes normativas, Markdown/JSON/SVG, pedidos, snapshot das instruções, acervo e evidências por hash. Os PDFs enviados ao Drive foram baixados e comparados byte a byte.
- O teste motivou correções: ZIP agora é download sem falso salto de página; prova-alvo futura aceita estado não publicado com evidência e ressalva; sumário lista disciplinas em vez de cada questão, mantendo os destinos e botões individuais.
- Limites: o item 10.1 cita Cofen/Corens de forma incongruente; não foram inventados sistemas internos. A alteração Cofeci 1573/2026 foi corroborada em duas reproduções, com acesso primário indisponível. Não houve avaliação de aprendizagem do candidato ou calibração psicométrica.

Os materiais deste pedido foram entregues em armazenamento privado do titular. O teste de produção não transforma a avaliação aberta AE-009 em aceite humano presumido.

## Resolução da auditoria 0.5

A [auditoria histórica](docs/auditoria-v05.md) encontrou duas falhas e falta de aceite real. A versão 0.6 valida imagens de todos os textos pela AST do Pandoc antes de incorporar recursos, inclui arquivos nos hashes e recusa caminhos externos ou SVG com dependências externas. Mudanças de figura agora sinalizam capítulos e questões afetados; usos fora de capítulo acionam política conservadora explícita. Regressões incluem sintaxe por referência, referências entre arquivos, symlinks e uso compartilhado em capítulo/contexto.

A suíte completa passou em **138 testes**. A integração adicional encontrou e corrigiu contraste insuficiente de números no SQL e contagem indevida de âncoras de código fora da sequência de Tab. CSS, tipografia e sumário aprovados foram preservados; os oito PDFs anteriores mantiveram páginas e geometria de texto. Duas páginas de código mudaram apenas nas cores de destaque para melhorar contraste.

## Caso real escolhido pelo titular

**Banco de Dados — Dataprev/FGV, Perfil 3 Desenvolvimento de Software**, edital 001/2026 retificado em 29/07/2026, páginas 30–31. A seleção cobre todos os **17 itens da matéria**, sem incluir as outras disciplinas do cargo e sem teto artificial de páginas.

- 17 capítulos, 12 diagramas próprios, exemplos resolvidos e recuperação ativa.
- Apostila de 99 páginas e caderno de 62 páginas, ambos vinculados a pedido e exportados com --final.
- 49 questões comentadas: 42 autorais e sete reais por acesso à prova oficial, com gabarito preliminar identificado.
- Programa literal conferido nas duas páginas do edital, portal/retificação/provas/gabaritos pesquisados e amostra intencional de dez itens de 2024/2026 registrada.
- Entrada textual escolhida pelo titular e print de teste renderizado do edital pelo agente. A transcrição termina no trecho visível; a continuação foi pesquisada no PDF oficial.
- Segunda passagem técnica/editorial por IA, 22 verificações SQL em massa independente, comparação de edições e errata. Não se presume avaliação humana.
- Catálogo anterior preservado: 67 questões únicas e 70 revisões, incluindo os comentários anteriores dos três itens reutilizados.

Ver [caso real](docs/validacao-real-dataprev.md), [matriz das 17 skills](docs/validacao-skills-v06.md) e [prontidão](docs/prontidao.md). Pedidos, fontes de consulta, snapshot de instruções, relatórios por hash e recibos ficam no pacote privado. O manifesto público recompõe o conteúdo como referência; testes estruturais sozinhos não comprovam pesquisa ou aprendizagem.

## Continuidade

Não há skill, arquivo de instrução ou correção técnica obrigatória conhecida ainda por desenvolver para o fluxo solicitado. AE-021/023/026/027/028 têm evidências de resolução; AE-009 aguarda [aplicação pelo leitor](docs/avaliacao-pedagogica.md). Novas matérias e concursos exigem nova pesquisa, cobertura e auditoria dos arquivos que forem entregues.

O método opera em sessões do agente com acesso ao projeto e às ferramentas. Gabaritos preliminares e fontes externas exigem nova consulta ao reutilizar. Não houve calibração estatística de dificuldade, ensaio com leitor de tela real ou certificação PDF/UA. O cofre mantém gestão e cartões; Git guarda as fontes executáveis. Nenhum serviço permanente ou instalação global é presumido.

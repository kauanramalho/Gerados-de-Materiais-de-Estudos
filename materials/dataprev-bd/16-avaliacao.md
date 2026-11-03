## Avaliar o modelo contra requisitos e evidências {#bd16}

**Objetivo BD-16 — item 16:** avaliar modelos por correção, cobertura, integridade, histórico e desempenho, explicitando os compromissos.

Um modelo de dados é adequado quando representa o domínio e sustenta as operações e garantias necessárias. Ter muitas tabelas, poucas tabelas ou uma tecnologia recente não basta como critério. A avaliação começa com requisitos e perguntas verificáveis: o modelo representa todas as ocorrências importantes? Quais duplicatas são proibidas? Que histórico deve permanecer disponível? Quais consultas e atualizações são frequentes?

Na avaliação **conceitual**, conferimos significado, cardinalidades, participação e atributos. Na avaliação **lógica**, verificamos chaves, dependências, normalização e preservação das informações. Na avaliação **física**, examinamos tipos, índices, particionamento e comportamento sob carga. Um defeito de significado não deve ser escondido por uma melhoria de índice.

### Casos que revelam erros

Exemplos pequenos são úteis quando incluem os limites do domínio: ocorrência sem relacionamento, vários relacionamentos válidos, tentativa de duplicação, valor ausente, mudança histórica e remoção de uma referência. Um conjunto em que todos possuem exatamente um vínculo não revela se o modelo consegue representar zero ou muitos.

Também é necessário conferir medidas. Se uma tabela possui uma linha por parcela, somar a quantidade de linhas não produz necessariamente a quantidade de matrículas. Se guarda somente o estado atual de uma dimensão, pode não responder a uma pergunta sobre o passado. Essas falhas decorrem do grão e do histórico, mesmo quando todas as consultas executam sem erro de sintaxe.

![Requisitos levam a casos de teste; o modelo é conferido quanto a significado e restrições; a carga representativa permite medir; defeitos retornam à revisão.](figuras/avaliacao.svg)

### Exemplo resolvido: duas propostas de cadastro

**Proposta A:** uma linha por aluno com uma coluna `curso`. **Proposta B:** Aluno, Curso e Matricula, com uma linha por vínculo e chave adequada. O requisito informa que um aluno pode cursar vários cursos e que cada curso pode ter muitos alunos.

**Teste:** Ana cursa SQL e Modelagem. Na proposta A, seria necessário repetir o aluno, guardar uma lista na coluna ou perder um curso. Cada remendo muda as regras do modelo. Na proposta B, duas matrículas representam o requisito diretamente. Depois, verificamos o impedimento de repetir o mesmo vínculo, a referência a alunos e cursos existentes e a regra sobre edições.

**Conclusão:** B responde melhor ao requisito declarado. Isso não prova que seja a melhor estrutura para qualquer relatório: uma camada analítica pode reorganizar esses eventos para agregação. A avaliação deve manter o contexto da finalidade.

### Medir sem fabricar resultados

Para comparar desempenho, defina carga representativa, volume, distribuição, proporção entre leitura e escrita, concorrência e critérios de sucesso. Considere latência, vazão e recursos, além da correção. Uma consulta isolada em uma tabela quase vazia não demonstra comportamento em milhões de registros. Também é preciso registrar ambiente e método, para que o resultado possa ser interpretado e repetido.

No PostgreSQL, estatísticas e estimativas do planejador podem ajudar a entender decisões. EXPLAIN não é um certificado de que o plano estimado será o melhor em toda situação. Medidas reais precisam de execução controlada, especialmente quando o comando modifica dados. Índices podem favorecer leituras e aumentar custos de escrita, o que exige avaliação da carga inteira.

### Critérios de revisão

Uma avaliação consistente reúne rastreabilidade do requisito, casos válidos e inválidos, informação preservada, segurança das alterações e evidências de execução. Desnormalizar ou duplicar dados pode ser uma escolha explícita, desde que haja regra para atualização e compreensão do risco de divergência. “Mais rápido” sem dizer para qual operação e com qual custo é uma conclusão incompleta.

**Recupere:** proponha três dados de teste que poderiam revelar defeitos em um cadastro de matrículas. Inclua pelo menos uma ocorrência sem vínculo e uma situação histórica. Explique o que cada teste observa e qual regra deveria satisfazer.

**Fontes:** F01, F02, F08 e F17. Nenhuma medida de desempenho fictícia foi apresentada como medição de um produto real.

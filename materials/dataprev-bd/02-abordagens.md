## Relações, dimensões e perguntas diferentes {#bd02}

**Objetivo BD-02 — item 2:** comparar as abordagens relacional e multidimensional sem confundir finalidade analítica com tecnologia de armazenamento.

Uma atendente registra uma matrícula; uma gestora compara a receita por curso, mês e região. As duas tarefas trabalham com dados relacionados, mas exigem operações diferentes. O registro transacional precisa conferir se o aluno existe, impedir uma matrícula duplicada e confirmar uma alteração pequena com segurança. A análise percorre muitos registros e resume resultados por diferentes perspectivas.

Na abordagem **relacional**, os dados são representados por relações, usualmente implementadas como tabelas. Cada linha expressa uma ocorrência, cada coluna possui um domínio e as chaves sustentam identidade e associações. A teoria relacional trabalha com conjuntos; SQL admite, em várias operações, linhas duplicadas e usa NULL para situações específicas. Portanto, não transfira sem ressalvas toda propriedade matemática de conjuntos para qualquer resultado SQL.

Na abordagem **multidimensional**, organizamos observações por medidas e dimensões. Receita é uma medida; Curso, Tempo e Região oferecem perspectivas de análise. O chamado cubo representa combinações dessas dimensões; não precisa ter exatamente três eixos. Um modelo com cinco dimensões continua sendo multidimensional, embora seja difícil desenhá-lo como um objeto espacial.

![O mesmo evento pode ser registrado como linha transacional e analisado por Curso, Tempo e Região; as medidas são agregadas conforme o nível escolhido.](figuras/abordagens.svg)

Na figura, o evento continua sendo o mesmo. O que muda é a organização para responder às perguntas. Uma implementação dimensional pode usar tabelas relacionais em estrela e consultas SQL. Assim, “relacional” e “multidimensional” não designam necessariamente produtos concorrentes ou formatos físicos incompatíveis.

### OLTP e OLAP

**OLTP** caracteriza processamento transacional, com muitas operações relativamente curtas e necessidade de manter regras de negócio. **OLAP** caracteriza análise, com consultas que combinam, filtram e agregam observações. Essa distinção descreve cargas de trabalho; não garante que todo sistema OLTP use o mesmo esquema nem que um banco relacional seja incapaz de análise.

Em um modelo analítico, uma hierarquia de Tempo pode organizar Dia → Mês → Ano. **Roll-up** sobe o nível de agregação; **drill-down** detalha. **Slice** fixa um valor de uma dimensão, como um ano. **Dice** seleciona um subconjunto por critérios em dimensões, como dois cursos e três regiões. **Pivot** muda a apresentação dos eixos. A ferramenta pode variar o vocabulário de interface, mas a operação conceitual deve ser reconhecida pelo efeito.

### Exemplo resolvido: agregar e detalhar

Suponha uma tabela de receitas, em valores fictícios: SQL em janeiro = R$ 300; SQL em fevereiro = R$ 500; Modelagem em janeiro = R$ 200; Modelagem em fevereiro = R$ 100. **Pergunta:** qual é a receita dos dois meses por curso?

Somamos apenas valores da mesma medida e moeda. SQL totaliza R$ 800; Modelagem, R$ 300. Agrupar os meses em um nível superior é uma agregação temporal. Voltar do total SQL para janeiro e fevereiro é detalhamento. Selecionar somente janeiro produz uma fatia temporal: SQL R$ 300 e Modelagem R$ 200. Esses números são construídos para o exercício e não representam resultados de uma organização real.

**Limite:** nem toda medida pode ser somada em todos os eixos. Um saldo de R$ 100 na segunda-feira e R$ 120 na terça não implica saldo de R$ 220. Razões e médias exigem atenção aos denominadores. Essa propriedade da medida deve constar do modelo, e não ser decidida apenas pelo botão “somar” de uma ferramenta.

**Erro frequente:** afirmar que cubos são próprios de OLTP ou que a análise multidimensional dispensa agregações. A prova pode trocar a finalidade dos dois tipos de carga. Leia o que a organização está tentando fazer: registrar um evento ou analisar muitos eventos.

**Recupere:** descreva uma consulta OLTP e uma OLAP para a mesma escola. Explique como um esquema em estrela pode continuar sendo implementado em um SGBD relacional.

**Fontes:** F08; prova P24, item 65, e P26, item 49, como evidência de abordagem de prova, sem previsão de frequência.

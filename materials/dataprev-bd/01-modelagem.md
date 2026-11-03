## Do problema ao modelo de dados {#bd01}

**Objetivo BD-01 — item 1 do edital:** distinguir os níveis conceitual, lógico e físico e transformar regras de negócio em um modelo verificável.

Uma escola precisa saber quem se matriculou em cada curso. Começar criando uma planilha com todas as informações parece simples, mas esconde decisões: um aluno pode fazer vários cursos? Um curso admite vários alunos? A mesma pessoa pode se matricular duas vezes na mesma edição? Modelar dados significa explicitar essas regras antes de escolher como armazená-las. O modelo representa o que o sistema precisa conhecer; não é uma cópia de todos os detalhes do mundo.

No nível **conceitual**, descrevemos entidades, atributos relevantes e relacionamentos do negócio. Aluno e Curso são tipos de entidade; Ana e o curso de SQL são ocorrências. Nome é um atributo, enquanto a matrícula pode ser um relacionamento com atributos próprios, como data e nota. Ainda não é necessário escolher índices, tamanhos de páginas ou um fornecedor de SGBD.

No nível **lógico**, organizamos a representação segundo um modelo de dados. No modelo relacional, definimos relações, atributos, domínios, chaves e restrições. No exemplo simplificado, `Aluno(id, nome)`, `Curso(id, titulo)` e `Matricula(aluno_id, curso_id, nota)` representam a estrutura. Chaves estrangeiras associam a matrícula aos registros existentes. Esse nível já resolve como representar o N:M em tabelas, mas não determina um algoritmo de acesso em disco.

No nível **físico**, implementamos a estrutura no SGBD escolhido: tipos concretos, índices, particionamento e organização de armazenamento. Um índice em `Matricula(curso_id)` pode acelerar uma consulta frequente; ele não cria uma nova regra de negócio. Algumas ferramentas misturam níveis no mesmo diagrama, por isso a classificação deve seguir a decisão representada, e não a aparência do desenho.

![Conceitual: Aluno e Curso ligados por matrícula N:M; lógico: tabela Matricula com duas referências; físico: tipos e índice de acesso.](figuras/modelagem.svg)

A figura separa as três perguntas: **o que existe**, **como representar** e **como implementar**. Repare que a tabela associativa aparece na transformação para o modelo relacional. O índice aparece depois, como escolha física.

### Cardinalidades e participação

Cardinalidade máxima responde quantas ocorrências podem se relacionar: 1:1, 1:N ou N:M. A participação mínima distingue obrigatoriedade de possibilidade: um aluno pode ter zero matrículas; cada matrícula deve apontar para exatamente um aluno. Confundir mínimo com máximo produz erros: permitir vários cursos não significa obrigar todo aluno a possuir um curso.

Uma **chave candidata** identifica uma ocorrência de forma única e sem atributos supérfluos. A chave primária é a candidata escolhida como principal. Usar um identificador artificial não elimina a necessidade de preservar a unicidade de uma chave de negócio, quando essa regra existe. Um CPF fictício de exercício pode ser único no cadastro, mas seu uso real exige cuidados que não são objeto deste capítulo.

### Exemplo resolvido: transformar N:M

**Problema:** Ana pode cursar SQL e Modelagem; SQL pode ter Ana e Beto. Queremos guardar a nota de cada vínculo. **Estratégia:** localizar a informação que pertence à associação. A nota não é propriedade permanente de Ana nem do curso SQL; pertence à matrícula.

Criamos as tabelas Aluno, Curso e Matricula. Na hipótese de uma única matrícula por par aluno–curso, a chave de Matricula é `(aluno_id, curso_id)`. As duas colunas também são chaves estrangeiras, cada uma para sua entidade. A chave é **composta**; cada coluna isolada pode se repetir. Se houver novas edições de um curso, o par deixa de identificar o vínculo: será necessário incluir a edição ou criar uma identificação com restrição de unicidade adequada.

**Conferência:** Ana–SQL e Ana–Modelagem são válidos; Ana–SQL repetido viola a regra escolhida. Colocar apenas `curso_id` em Aluno permitiria um só curso por aluno e perderia o N:M. Um array de cursos pode existir em outro modelo, mas não substitui automaticamente o mapeamento relacional pedido.

**Recupere sem olhar:** explique por que uma chave estrangeira pertence ao modelo lógico e a escolha de um índice pertence ao físico. Depois descreva uma regra que faria a chave de Matricula mudar.

**Fontes:** F01, F03; edital E26, páginas 30–31. Os exemplos e a figura são originais.

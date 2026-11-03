## O problema que vamos resolver {#objetivos}

Uma escola mantém cadastros de alunos, cursos e matrículas. A coordenação quer responder perguntas simples: quem está matriculado, quantos alunos estão ativos em cada curso e quem ainda não recebeu nota. A dificuldade aparece quando uma consulta mistura conceitos distintos: um aluno pode existir sem matrícula, uma matrícula pode existir sem nota, e a nota zero é diferente de uma nota ainda não informada.

Este capítulo ensina a seguir uma consulta linha por linha, em vez de decorar palavras de SQL. Ao final, você deverá conseguir identificar uma associação N:M, distinguir chave primária de estrangeira, prever a quantidade de linhas de uma junção, tratar NULL corretamente e explicar o resultado de contagens e agrupamentos.

O recorte se vincula ao Perfil 3 — Desenvolvimento de Software, bloco Banco de Dados, do Edital 001/2026 da Dataprev: abordagem relacional, integridade referencial, SQL e aspectos de DDL/DML. A referência é o edital retificado em 29/07/2026, página 30. Não se pretende cobrir todo o bloco, nem indicar que este concurso seja sua prioridade atual.

**Pré-requisitos:** reconhecer uma tabela como conjunto de linhas e colunas e compreender comparações simples. Os exemplos usam um subconjunto comum de SQL. Os resultados foram executados em SQLite com chaves estrangeiras habilitadas; as referências conceituais incluem PostgreSQL 17. Recursos específicos de um SGBD exigem conferir seu manual.

## Enxergue as relações antes do código {#relacoes}

Um registro de Aluno descreve uma pessoa cadastrada. Um registro de Curso descreve uma oferta de conteúdo. Uma matrícula liga um aluno a um curso e guarda informações dessa ligação, como situação e nota. A nota não pertence ao aluno isoladamente: a mesma pessoa pode ter notas diferentes em cursos diferentes. Por isso, ela fica na tabela da associação.

Um aluno pode participar de vários cursos e um curso pode reunir vários alunos. A relação conceitual é N:M. No modelo relacional do exemplo, ela é representada por Matricula, com duas chaves estrangeiras e uma chave primária composta. Cada linha identifica um par aluno/curso, como mostra a Figura 1.

![Figura 1 — O cadastro Aluno e o cadastro Curso se ligam por Matricula. O par aluno_id/curso_id identifica a matrícula; cada componente também referencia a chave primária de seu cadastro. As extremidades admitem cadastros ainda sem matrícula. Esquema original.](figuras/relacoes.svg)

**Chave primária** identifica cada linha sem repetição e sem NULL em suas colunas. **Chave estrangeira** exige correspondência com uma chave referenciada, nas condições definidas pela restrição. Ela não precisa ser única: várias matrículas podem apontar para o mesmo aluno. Confundir essas duas funções costuma produzir modelos ou conclusões errados. [Fonte T01](#fonte-t01)

O modelo impõe uma decisão de negócio: um aluno só pode ter uma matrícula por curso. Se fossem permitidas várias edições ou tentativas, seria necessário incluir essa informação na identificação. Chave não é apenas detalhe técnico; expressa o que o domínio considera uma ocorrência distinta.

```sql
CREATE TABLE Aluno (
  id INTEGER PRIMARY KEY,
  nome TEXT NOT NULL,
  nota_maxima REAL
);
CREATE TABLE Curso (
  id INTEGER PRIMARY KEY,
  titulo TEXT NOT NULL
);
CREATE TABLE Matricula (
  aluno_id INTEGER NOT NULL REFERENCES Aluno(id),
  curso_id INTEGER NOT NULL REFERENCES Curso(id),
  nota REAL,
  status TEXT NOT NULL,
  PRIMARY KEY (aluno_id, curso_id)
);
```

Na massa de dados, Ana tem duas matrículas; Beto e Caio têm uma cada; Dora ainda não tem nenhuma. Essa distribuição é deliberada: impede que um exemplo excessivamente regular esconda os efeitos das junções.

| Aluno | Nome | Curso da matrícula | Nota | Situação |
|---|---|---|---|---|
| 1 | Ana | 10 — SQL | 8 | ativa |
| 1 | Ana | 20 — Redes | NULL | cancelada |
| 2 | Beto | 10 — SQL | 6 | ativa |
| 3 | Caio | 20 — Redes | NULL | ativa |

Além das linhas acima, existe Aluno(4, Dora). Curso também contém 30 — Linux, ainda sem matrículas. Esta tabela é uma visão explicativa da massa, não a estrutura física: os nomes não são repetidos em Matricula.

## O que acontece ao excluir um cadastro {#integridade}

Uma chave estrangeira protege a ligação entre linhas, mas a reação à exclusão precisa ser definida. Com ON DELETE CASCADE, excluir a linha referenciada remove as linhas dependentes que a apontam. Isso não significa que excluir um dependente apague o cadastro principal. A direção importa.

Com NO ACTION, a operação não pode deixar a restrição violada no momento em que ela é verificada. Em uma restrição imediata, tentar excluir um aluno ainda referenciado provoca falha. Alguns sistemas permitem adiar a verificação; por isso, NO ACTION e RESTRICT não devem ser tratados como sinônimos absolutos em todos os SGBDs. Neste capítulo, os testes usam verificação imediata. [Fontes T01](#fonte-t01) e [T09](#fonte-t09)

**Exemplo resolvido:** em um cenário separado, sem outras referências que impeçam a exclusão, imagine uma tabela de presença com aluno_id referenciando Aluno(id) e ação CASCADE. Se Ana tiver três presenças e for excluída de Aluno, as três presenças dependentes são removidas. Excluir apenas uma presença não exclui Ana. Para conferir a resposta, desenhe uma seta da FK para a chave referenciada e identifique de qual tabela a operação parte.

Trocar a ação referencial muda o comportamento, mas não transforma uma FK em chave primária. Também não elimina a necessidade de pensar no negócio: remover automaticamente histórico acadêmico pode ser inadequado para um sistema real, embora seja um mecanismo válido do banco.

## Estrutura e regras da massa

Use os dados abaixo nas questões autorais, salvo indicação expressa. As tabelas são Aluno(id PK, nome, nota_maxima), Curso(id PK, titulo) e Matricula(aluno_id FK, curso_id FK, nota, status). A chave primária de Matricula é o par (aluno_id, curso_id). As FKs apontam para Aluno(id) e Curso(id), usam verificação imediata e não possuem CASCADE. As duas colunas da chave composta são obrigatórias; nota aceita NULL.

Nos trechos SQL, a é o alias de Aluno e m é o alias de Matricula. Os exemplos comparam resultados da massa inicial; uma questão não altera a massa da questão seguinte. Os valores iniciais de nota_maxima são 99 para todos os alunos.

**Cadastro de alunos:** 1 — Ana; 2 — Beto; 3 — Caio; 4 — Dora.

**Cadastro de cursos:** 10 — SQL; 20 — Redes; 30 — Linux.

| aluno_id | curso_id | nota | status |
|---|---|---|---|
| 1 | 10 | 8 | ativa |
| 1 | 20 | NULL | cancelada |
| 2 | 10 | 6 | ativa |
| 3 | 20 | NULL | ativa |

Dora não possui matrícula. Linux ainda não possui matrículas. Uma nota nula não significa que a matrícula não existe. As questões reais são acessadas na prova oficial e usam os dados próprios de seus enunciados.

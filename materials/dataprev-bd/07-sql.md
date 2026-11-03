## Ler a consulta pelo efeito que ela produz {#bd07}

**Objetivo BD-07 — item 7:** interpretar filtros, junções, agregações, subconsultas e operações de conjunto, com atenção a duplicações e NULL.

SQL permite declarar o resultado desejado, deixando ao SGBD a escolha de um plano de execução. A ordem escrita de uma consulta não deve ser confundida com uma sequência física obrigatória. Para raciocinar sobre um SELECT simples, é útil considerar FROM/JOIN, WHERE, GROUP BY, HAVING, SELECT, DISTINCT e ORDER BY como uma ordem lógica de interpretação; o otimizador pode executar operações de outra forma, preservando o resultado exigido.

Considere `Aluno(id,nome)` com Ana, Beto e Caio. Existem três matrículas: Ana em SQL com nota 8; Ana em Modelagem com nota 9; Beto em SQL com nota NULL. Caio não possui matrícula. Esses dados fictícios serão usados nos exemplos; NULL significa nota ainda ausente, e não nota zero.

### Junções e multiplicidade

Um INNER JOIN retorna combinações que satisfazem a condição. Ana aparece duas vezes ao juntar alunos com suas matrículas, porque há dois vínculos. Isso não é, por si só, um defeito de duplicação. Um LEFT JOIN preserva os alunos e preenche com NULL as colunas da matrícula quando não existe correspondência. A preservação depende da consulta completa: um filtro posterior em uma coluna da matrícula pode eliminar as linhas sem correspondência.

```sql
SELECT a.nome, m.curso_id
FROM Aluno AS a
LEFT JOIN Matricula AS m ON m.aluno_id = a.id
ORDER BY a.id, m.curso_id;
```

O resultado contém duas linhas para Ana, uma para Beto e uma para Caio com curso nulo. Se acrescentarmos `WHERE m.nota >= 7`, ficam apenas as matrículas de Ana: o predicado não é verdadeiro para a nota nula de Beto nem para a linha sem matrícula de Caio. Mover um filtro para ON pode mudar o resultado, porque muda a condição de correspondência sem necessariamente eliminar o aluno preservado.

### NULL, contagens e grupos

Comparações comuns com NULL resultam em desconhecido; por isso usamos `IS NULL` e `IS NOT NULL`. WHERE conserva linhas em que a condição é verdadeira. `COUNT(*)` conta linhas; `COUNT(nota)` conta valores não nulos de nota. SUM, AVG, MIN e MAX normalmente ignoram entradas nulas; em conjunto vazio, COUNT retorna zero, enquanto SUM e MAX retornam NULL, não um zero inventado.

```sql
SELECT curso_id, COUNT(*) AS matriculas,
       COUNT(nota) AS avaliadas, AVG(nota) AS media
FROM Matricula
GROUP BY curso_id
HAVING COUNT(*) >= 1
ORDER BY curso_id;
```

Para SQL, há duas matrículas, uma nota conhecida e média 8. Para Modelagem, há uma matrícula, uma nota e média 9. A média de SQL não é 4: a ausência de nota não foi convertida em zero. WHERE filtra linhas antes da formação dos grupos; HAVING filtra grupos. Não use uma fórmula de agregação no lugar errado sem observar o dialeto e a semântica.

### Subconsultas e operações de conjunto

Uma subconsulta **correlacionada** faz referência a uma linha do contexto externo. Uma subconsulta escalar deve produzir um valor compatível; várias linhas, quando não admitidas, causam erro. `EXISTS` verifica existência, sem exigir que os valores selecionados sejam usados como resultado. Para encontrar alunos sem matrícula, `NOT EXISTS` evita a armadilha de um `NOT IN` cujo conjunto contenha NULL.

`UNION` elimina linhas duplicadas entre resultados compatíveis; `UNION ALL` preserva multiplicidades. `INTERSECT` e `EXCEPT` representam interseção e diferença, observadas as opções e o suporte do SGBD. Uma CTE com WITH pode organizar uma consulta; não é garantia universal de materialização. Uma função de janela, como `ROW_NUMBER() OVER (ORDER BY id)`, calcula sobre uma janela sem reduzir necessariamente o conjunto a uma linha por grupo. Dentro de OVER, PARTITION BY separa janelas; a numeração de ROW_NUMBER recomeça em cada uma, segundo a ordenação indicada. Empates exigem critérios adicionais quando é necessário um resultado determinístico.

**Exemplo resolvido:** para listar Caio, use `WHERE NOT EXISTS (SELECT 1 FROM Matricula m WHERE m.aluno_id = a.id)`. A subconsulta encontra matrículas de Ana e Beto e não encontra a de Caio. Portanto, apenas Caio satisfaz a negação. Sem ORDER BY, a apresentação das linhas não tem ordem garantida.

**Recupere:** explique a diferença entre uma linha sem correspondência no LEFT JOIN e uma matrícula real cuja nota é NULL. Depois calcule COUNT(*) e COUNT(nota) sem executar a consulta.

**Fontes:** F03, F04 e F17; exercícios executáveis deste material. As instruções usam um subconjunto portável de SQL, com execução de conferência em SQLite e referência conceitual ao PostgreSQL.

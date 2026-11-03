## Base comum dos exercícios

Quando o item disser **contexto-base**, use exclusivamente os dados abaixo. Outros cenários estão definidos nos próprios enunciados. Todos os nomes e valores são fictícios e didáticos.

| Aluno.id | nome |
|---:|---|
| 1 | Ana |
| 2 | Beto |
| 3 | Caio |

| Curso.id | titulo |
|---:|---|
| 10 | SQL |
| 20 | Modelagem |

| Matricula.aluno_id | curso_id | nota |
|---:|---:|---:|
| 1 | 10 | 8 |
| 1 | 20 | 9 |
| 2 | 10 | NULL |

Matricula tem chave primária `(aluno_id, curso_id)` e referências para Aluno e Curso. A nota admite NULL; NULL não é nota zero. Caio não tem matrícula. As consultas usam um subconjunto comum de SQL, e diferenças de produto são indicadas quando relevantes. Na massa de conferência em SQLite, chaves estrangeiras são habilitadas explicitamente.

Cada questão é independente: comece novamente pelo estado acima, salvo indicação contrária. Uma alteração de um item não afeta os dados do seguinte. Quando houver ordenação relevante ao exemplo, o SQL utiliza ORDER BY; uma ordem não declarada não é garantida.

## Como usar os itens oficiais

Os sete itens reais pertencem à prova Dataprev/FGV 2026, Desenvolvimento de Software, tipo 1, questões 46–52, páginas 13–14. Abra o link da própria questão para ler seu enunciado e as cinco alternativas originais. Não aplique a esses itens o contexto-base acima: eles têm seus próprios dados na prova.

Os comentários deste caderno são originais e ficam no próprio arquivo, com retorno à questão. O gabarito de 2026 consultado é preliminar; seu status deve ser novamente conferido antes de uso oficial. As referências à teoria indicam IDs da apostila; o caderno não fabrica ligações entre dois PDFs independentes.

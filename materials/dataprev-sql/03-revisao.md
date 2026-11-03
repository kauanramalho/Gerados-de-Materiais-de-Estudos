## Um método para resolver sem adivinhar {#metodo}

Leia a pergunta e marque qual objeto está sendo contado: alunos, matrículas, linhas da junção ou notas preenchidas. Em seguida, identifique a tabela de partida e decida se linhas sem correspondência devem permanecer. Só depois avalie os filtros e as agregações.

Para validar uma hipótese, use um caso com duas correspondências, outro com uma correspondência nula em atributo opcional e outro sem correspondência. Ana, Caio e Dora foram escolhidos para cumprir esses três papéis. Um resultado correto em uma massa sem exceções não basta para demonstrar que a interpretação está correta.

| Se o enunciado pede… | Verifique… | Erro que o exemplo revela |
|---|---|---|
| Todos os alunos, mesmo sem matrícula | Qual lado é preservado | INNER JOIN exclui Dora |
| Número de matrículas por aluno | Qual coluna é contada | COUNT(*) conta a linha preservada |
| Notas ainda não informadas | IS NULL | Igualdade com NULL não faz esse teste |
| Alunos com pelo menos duas matrículas | GROUP BY e HAVING | Filtro de grupo confundido com filtro de linha |
| Excluir cadastro com dependentes | Direção e ação da FK | CASCADE interpretado ao contrário |
| Atualização por subconsulta | Alvo do UPDATE e conjunto vazio | Ausência confundida com preservação automática |

## Glossário de consulta {#glossario}

- **Cardinalidade:** quantidade de ocorrências que podem se relacionar; no resultado de uma consulta, também se usa o termo para sua quantidade de linhas.
- **PK:** chave primária; identifica a linha de modo único e não nulo.
- **FK:** chave estrangeira; liga uma referência a uma chave de outra tabela ou da própria tabela.
- **Junção externa:** conserva linhas de um lado mesmo sem correspondência do outro.
- **NULL:** ausência de valor; não equivale a zero, texto vazio ou falso.
- **Agregação:** cálculo que resume valores de um conjunto ou grupo.
- **Subconsulta correlacionada:** consulta interna que referencia a linha ou o contexto da consulta externa.

## Recuperação ativa {#recuperacao}

Feche o capítulo e explique por que Caio e Dora podem aparecer com uma nota nula por motivos diferentes. Depois reconstrua a tabela de contagens sem olhar os resultados. Por último, diga o que muda ao deslocar o filtro de situação do ON para o WHERE.

Ao corrigir as questões, classifique o erro: conceito, leitura do enunciado, simulação das linhas, tratamento de NULL ou desconhecimento de sintaxe. Essa classificação orienta uma revisão mais útil do que apenas registrar “acertei” ou “errei”.

**Prática reproduzível:** os arquivos massa.sql e verificacoes.json acompanham este piloto. O comando `python scripts/check_sql.py materials/dataprev-sql/verificacoes.json` executa os exemplos e compara os resultados esperados. A execução não substitui a compreensão do raciocínio nem testa equivalência integral entre SGBDs.

## Limites do recorte

Este material não esgota normalização, modelagem multidimensional, NoSQL, índices, transações ou otimização. Também não oferece previsão de incidência de assuntos na próxima prova. A dificuldade das questões autorais é uma estimativa editorial; a avaliação de aprendizagem depende de aplicação com o leitor.

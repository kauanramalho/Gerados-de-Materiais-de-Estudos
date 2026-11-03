## Alterar dados e prever todas as linhas atingidas {#bd09}

**Objetivo BD-09 — item 9:** interpretar INSERT, UPDATE, DELETE e operações de sincronização, conferindo filtros, subconsultas e efeitos de transações.

A linguagem de manipulação de dados, **DML**, altera o conteúdo das estruturas. INSERT acrescenta linhas; UPDATE modifica linhas existentes; DELETE remove linhas. SELECT é tratado como consulta em algumas classificações e incluído em um sentido amplo de manipulação em outras. Essa diferença de nomenclatura não muda os efeitos dos comandos.

Uma operação deve ser lida em três partes: tabela-alvo, linhas escolhidas e valores atribuídos. Em UPDATE, o WHERE seleciona as linhas; o SET define as alterações. Sem WHERE, todas as linhas da tabela-alvo são candidatas à atualização. Isso continua valendo quando a expressão atribuída contém uma subconsulta: a ausência de uma linha correspondente não faz, por si só, a linha-alvo ser ignorada.

### Exemplo resolvido: máximo de conjunto vazio

Suponha a tabela `ResumoAluno(id, maior_nota)` com três alunos e a tabela Matricula dos capítulos anteriores. A coluna maior_nota admite NULL.

```sql
UPDATE ResumoAluno AS r
SET maior_nota = (
  SELECT MAX(m.nota)
  FROM Matricula AS m
  WHERE m.aluno_id = r.id
);
```

**Passo 1:** não há WHERE externo; as três linhas do resumo serão consideradas. **Passo 2:** a subconsulta é correlacionada pelo aluno. Para Ana, as notas 8 e 9 produzem máximo 9. Para Beto, existe uma matrícula, mas sua nota é NULL; o máximo dos valores conhecidos é NULL. Para Caio, não existe matrícula; MAX sobre o conjunto vazio também resulta em NULL. **Conclusão:** os resumos ficam 9, NULL e NULL. Os dois últimos têm causas diferentes, embora produzam o mesmo valor.

Para preservar o valor anterior quando não há valor conhecido, uma solução possível usa `COALESCE(subconsulta, r.maior_nota)`. Isso precisa refletir a regra de negócio: “preservar” não é sinônimo de “preencher com zero”. Um filtro externo com EXISTS também pode restringir as linhas, mas deve definir se basta haver matrícula ou se é preciso haver nota não nula.

### Inserir, excluir e sincronizar

INSERT pode informar valores ou usar o resultado de um SELECT. A lista de colunas evita depender da ordem física de definição da tabela. Valores padrão, restrições e gatilhos ainda podem afetar a operação. Ao copiar dados de uma consulta, não se deve presumir que duplicatas desaparecem automaticamente.

DELETE com um filtro remove as linhas que o satisfazem; não remove a definição da tabela. As restrições referenciais podem impedir ou propagar a exclusão. Antes de uma alteração importante, executar um SELECT com o mesmo predicado ajuda a conferir o alvo, embora não elimine problemas de concorrência entre a conferência e a alteração.

MERGE expressa ações de correspondência entre origem e destino, podendo atualizar ou inserir conforme o caso. O suporte, as condições permitidas e as garantias dependem do SGBD. No PostgreSQL, existe MERGE; a alternativa `INSERT ... ON CONFLICT` atende outros cenários. Nenhuma forma de sincronização dispensa definir uma chave de negócio e decidir como lidar com duplicatas da origem.

### Transações e confirmação

Uma transação reúne operações que precisam formar uma unidade lógica. BEGIN inicia um bloco nos produtos que usam essa sintaxe; COMMIT confirma; ROLLBACK desfaz alterações não confirmadas conforme o mecanismo transacional. Em uma transferência, subtrair de uma conta e somar em outra deve ser tratado em conjunto. A atomicidade não é criada apenas por colocar duas instruções próximas no arquivo: é preciso usar a transação e tratar falhas.

**Recupere:** explique por que Caio recebe NULL no exemplo, e como mudaria o comportamento se maior_nota fosse NOT NULL. A violação precisaria ser tratada pelo SGBD; não é correto supor que a coluna conservaria silenciosamente o valor antigo.

**Fontes:** F04, F06 e F07; P26, item 51, como evidência de cobrança de efeitos de subconsultas, com exemplo autoral distinto.

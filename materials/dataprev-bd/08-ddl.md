## Definir estrutura e regras verificáveis {#bd08}

**Objetivo BD-08 — item 8:** interpretar e escrever DDL, diferenciando estrutura, restrições e decisões físicas.

A linguagem de definição de dados, **DDL**, reúne comandos para criar, alterar e remover estruturas. CREATE TABLE define uma tabela; ALTER TABLE altera sua definição; DROP TABLE remove a estrutura. CREATE INDEX cria um caminho de acesso, e CREATE VIEW define uma consulta nomeada. A classificação de alguns comandos varia entre referências; compreender seu efeito é mais seguro do que decorar siglas sem contexto.

O tipo de uma coluna descreve os valores que podem ser representados e como operações sobre eles são interpretadas. Um identificador numérico não precisa aceitar cálculos de negócio apenas por usar INTEGER. Para valores monetários, tipos decimais exatos podem ser preferíveis a aproximações binárias, conforme os requisitos. A precisão e a escala devem comportar os valores; escolher um tipo não substitui definir moeda e regra de arredondamento.

### Exemplo resolvido: uma estrutura de matrícula

```sql
CREATE TABLE Aluno (
  id INTEGER PRIMARY KEY,
  nome VARCHAR(80) NOT NULL,
  email VARCHAR(160) UNIQUE
);
CREATE TABLE Curso (
  id INTEGER PRIMARY KEY,
  titulo VARCHAR(120) NOT NULL
);
CREATE TABLE Matricula (
  aluno_id INTEGER NOT NULL,
  curso_id INTEGER NOT NULL,
  nota DECIMAL(4,2),
  PRIMARY KEY (aluno_id, curso_id),
  FOREIGN KEY (aluno_id) REFERENCES Aluno(id),
  FOREIGN KEY (curso_id) REFERENCES Curso(id),
  CHECK (nota >= 0 AND nota <= 10)
);
```

**Leitura guiada:** a chave de Matricula impede repetir o mesmo par aluno–curso. As referências exigem alunos e cursos existentes. A nota admite ausência; quando for não nula, a condição deve ser respeitada. Declarar `NOT NULL` na nota mudaria o requisito, pois impediria cadastrar uma matrícula ainda sem avaliação. A regra de uma só matrícula por par é uma hipótese deste exercício, não uma regra universal de escolas.

**Conferência:** tentar inserir o mesmo par duas vezes deve falhar; uma nota 11 deve falhar; uma nota NULL deve ser permitida. O tratamento de tipos e de restrições depende do produto: a conferência em SQLite exige `PRAGMA foreign_keys = ON`, e sua afinidade de tipos não equivale à implementação de todos os tipos do PostgreSQL. Não use um teste em um motor como prova de uma particularidade de outro.

### Alterar e remover com cuidado

Adicionar uma coluna com ALTER TABLE pode exigir valor padrão, preenchimento e conferência de restrições para os registros existentes. Mudar o tipo pode envolver conversão. Remover uma tabela pode ser impedido por dependências ou exigir uma política de remoção. Uma VIEW comum guarda a definição da consulta, e não necessariamente uma cópia persistente de todas as linhas; uma visão materializada possui outro comportamento de armazenamento e atualização.

TRUNCATE costuma remover linhas de uma tabela de forma distinta de DELETE, mas suas regras de transação, gatilhos, identidade e referências variam. Não é correto afirmar universalmente que todo DDL confirma implicitamente a transação ou que nunca pode ser desfeito. O PostgreSQL, por exemplo, suporta muitas operações DDL dentro de transações; outros produtos possuem comportamentos diferentes.

Um índice pode acelerar filtros e junções, mas consome espaço e trabalho adicional de manutenção em inserções e alterações. Criar um índice em toda coluna não é uma estratégia automaticamente boa. A declaração da chave e a escolha de índices se relacionam na implementação, embora expressem decisões distintas.

**Recupere:** identifique qual regra impediria nota negativa, matrícula duplicada e aluno inexistente. Explique por que nenhuma delas, isoladamente, obriga todo aluno a ter pelo menos uma matrícula.

**Fontes:** F03 e F05. Os testes locais registram o motor e suas opções; as diferenças de dialeto não são ocultadas.

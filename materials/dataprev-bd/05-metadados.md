## Os dados que explicam os dados {#bd05}

**Objetivo BD-05 — item 5:** reconhecer metadados técnicos, de negócio e de processo e usá-los para interpretar corretamente uma informação.

Uma coluna chamada `valor` não informa, sozinha, se representa reais ou dólares, receita bruta ou líquida, valor por matrícula ou total do mês. Mesmo conhecendo o número armazenado, ainda falta saber o que ele significa e como foi produzido. **Metadados** descrevem estrutura, significado, origem e outras características dos dados. Não se limitam ao nome de um arquivo ou à data de sua criação.

Os **metadados técnicos** descrevem a representação e a estrutura: nome de uma tabela, tipo de uma coluna, precisão numérica, chave primária, restrição de nulidade e relacionamento. `valor_pago DECIMAL(10,2) NOT NULL` contém informação técnica. O tipo limita uma representação; não explica automaticamente quais descontos o negócio considera.

Os **metadados de negócio** definem significado e uso: “receita líquida corresponde ao valor recebido após descontos e estornos, expresso em reais”. O responsável pela definição, a regra de cálculo e o glossário ajudam áreas diferentes a produzir o mesmo indicador. Duas colunas com tipos iguais podem representar conceitos diferentes; duas representações técnicas diferentes podem expressar o mesmo conceito.

Os **metadados de processo**, também chamados operacionais em certos catálogos, descrevem execução e movimentação: horário de uma carga, quantidade de linhas lidas, rejeitadas e gravadas, duração, estado e versão do procedimento. O vocabulário de classificação varia entre referências. Na prova, classifique a informação efetivamente apresentada e observe a terminologia das alternativas.

### Dicionário, catálogo e linhagem

Um **dicionário de dados** reúne descrições de elementos, tipos e regras. Um **catálogo** facilita descobrir conjuntos de dados, seus responsáveis, descrições e condições de uso. **Linhagem** registra de onde uma informação veio e por quais transformações passou. Um catálogo pode combinar essas funções; ter um catálogo não garante, sozinho, que todas as descrições sejam corretas ou estejam atualizadas.

O catálogo interno de um SGBD registra objetos como tabelas, colunas e restrições. O `information_schema`, quando suportado, oferece visões padronizadas sobre parte desses objetos. Um glossário de negócio não surge completo a partir desse catálogo: o SGBD pode conhecer a precisão de uma coluna sem conhecer a definição institucional de “aluno ativo”.

### Exemplo resolvido: localizar uma divergência

Duas áreas informam receitas diferentes para o mesmo mês. A equipe A soma pagamentos confirmados menos estornos, considerando a data de confirmação; a B soma matrículas emitidas, considerando a data de criação. Ambas usam uma coluna decimal.

**Passo 1:** comparar a definição do indicador. A diferença de conceito e de período é de negócio, mesmo que os tipos técnicos sejam iguais. **Passo 2:** conferir a origem e as transformações pela linhagem. **Passo 3:** verificar se a carga foi concluída e se houve rejeições, usando metadados operacionais. **Passo 4:** conferir tipos e restrições se houver suspeita de arredondamento ou truncamento. A investigação passa por categorias diferentes, sem tratar todas como uma única informação.

Uma execução fictícia leu 1.000 registros e gravou 980. O número 980 é um metadado de processo quando descreve o resultado dessa execução. Para avaliar completude, precisamos explicar os outros 20: foram rejeitados por erro, eliminados por deduplicação prevista ou ainda não processados? A simples diferença não prova perda indevida.

**Erro frequente:** chamar o tipo DECIMAL de metadado de negócio ou chamar uma definição de “receita líquida” de descrição puramente técnica. Outra confusão é considerar que metadados são sempre externos ao banco; eles também podem estar em tabelas e catálogos internos.

**Recupere:** classifique “nota entre zero e dez”, “coluna NUMERIC(4,2)” e “carga concluída às 02h15”. A primeira frase pode ser regra de negócio; a segunda descreve representação; a terceira registra execução. Explique por que implementar a primeira como CHECK não elimina sua origem no negócio.

**Fontes:** F09, F03 e P26, item 48. A terminologia de processo foi alinhada ao item oficial consultado.

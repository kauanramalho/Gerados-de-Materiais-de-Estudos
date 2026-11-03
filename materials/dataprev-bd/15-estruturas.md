## Estrutura, significado e representação {#bd15}

**Objetivo BD-15 — item 15:** distinguir dados estruturados, semiestruturados e não estruturados sem confundir a categoria com o nome de um produto.

**Dados estruturados** seguem uma organização previamente definida, com elementos e relações interpretados por um esquema. Uma tabela de matrículas com colunas e tipos conhecidos é um exemplo. O esquema permite validar condições, executar consultas e comparar registros de maneira consistente, embora a qualidade do conteúdo ainda dependa de regras e conferências.

**Dados semiestruturados** possuem elementos de organização, como nomes de campos, marcadores e hierarquias, sem exigir necessariamente a mesma disposição rígida para todas as ocorrências. JSON e XML são representações comuns. Sua sintaxe é estruturada e pode ser validada; o prefixo “semi” não significa que o arquivo seja um texto sem qualquer organização. Um esquema adicional também pode ser imposto a esses documentos.

**Dados não estruturados**, no sentido usado nessa classificação, não chegam organizados integralmente em campos do esquema de análise pretendido. Um áudio de aula, uma fotografia e o corpo textual de um documento são exemplos frequentes. Eles continuam tendo uma estrutura técnica de arquivo e podem possuir metadados, como formato, tamanho e data. A classificação não afirma que são sequências de bytes sem regra.

### O mesmo conteúdo pode ter diferentes usos

Uma redação em PDF pode ser tratada como conteúdo textual a interpretar, enquanto seu título e sua data de criação estão em campos estruturados de um catálogo. Uma imagem pode ser associada a rótulos, dimensões e resultados de processamento. Extrair informação de um conteúdo não estruturado gera novas representações que precisam de validação; não transforma automaticamente toda interpretação em fato confiável.

CSV costuma representar dados tabulares, mas a extensão não garante que os registros sejam válidos: delimitadores, aspas, tipos e convenções de ausência precisam ser respeitados. Da mesma forma, um JSON bem formado pode conter um valor inadequado para o negócio, como uma nota em texto quando a aplicação exige um número entre zero e dez.

### Exemplo resolvido: integrar três fontes

Uma escola recebe: uma tabela de matrículas com colunas fixas; formulários JSON com campos opcionais de preferências; gravações de aulas. **Classificação inicial:** a tabela representa dados estruturados; os formulários são um exemplo de semiestrutura; o conteúdo das gravações é não estruturado em relação ao esquema de análise das aulas.

**Passo seguinte:** definir o que se quer extrair. Para contar matrículas, a tabela pode bastar. Para analisar preferências, é necessário interpretar campos opcionais e distinguir ausência de um campo de uma resposta explícita. Para localizar temas em gravações, pode ser necessária transcrição, cuja exatidão exige conferência. Armazenar tudo em um mesmo serviço não torna os três conteúdos semanticamente equivalentes.

**Conferência:** se um JSON não tem o campo `preferencia`, isso não prova que a preferência seja uma string vazia ou que tenha sido negada. A semântica de ausência precisa ser definida. Em SQL, NULL também não é automaticamente igual a zero ou a texto vazio; cada representação exige suas regras.

### Relação com escolhas de armazenamento

Um SGBD relacional pode oferecer tipos ou funções para documentos; um banco documental pode armazenar registros com estrutura bastante uniforme. Logo, não é correto classificar um conteúdo apenas pela categoria do produto que o recebeu. O modelo de dados, as operações e a validação devem ser avaliados em conjunto.

**Recupere:** explique por que “JSON tem sintaxe definida” e “JSON pode representar dados semiestruturados” são afirmações compatíveis. Depois descreva os metadados estruturados que podem acompanhar uma fotografia sem eliminar a necessidade de interpretar seu conteúdo visual.

**Fontes:** F09, F10, F12 e F13. A classificação é relativa à organização utilizada na análise, com exemplos construídos para o edital.

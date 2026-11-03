# Produção de materiais — versão 0.3

O agente pesquisa e redige; o publicador monta e verifica os arquivos preparados. Esta versão já aceita materiais novos por manifesto e exporta apostila e caderno de questões. Não há chamada automática a um LLM ou serviço de recebimento permanente.

## Da solicitação ao primeiro lote

1. Ler AGENTS, Progress, Decisions e as skills pertinentes. Identificar concurso/cargo e recuperar os materiais existentes antes de perguntar.
2. Conferir edital e retificações na fonte oficial. Delimitar um recorte; registrar objetivos, cobertura parcial e lacunas.
3. Buscar provas e gabaritos relacionados. Registrar ano, perfil, tipo, item, página, status e hash; separar análise da amostra de previsão de incidência.
4. Redigir capítulos com explicação, mecanismo, limites, exemplos resolvidos e recuperação ativa. Produzir figuras originais com legenda e descrição.
5. Preparar as questões autorais e os comentários. Itens reais com direitos não confirmados recebem acesso ao original por link. Nunca misturar um gabarito de outro ano/tipo.
6. Montar o manifesto e executar a pré-validação, as verificações técnicas pertinentes e a publicação. Revisar o conteúdo e inspecionar o PDF.
7. Entregar os arquivos, atualizar estado e decisões e registrar evidências no Segundo Cérebro quando acessível.

## Arquivos de entrada

Uma pasta de material contém material.json, capítulos Markdown, questoes.json, fontes.json, figuras.json e cobertura.json. Um contexto de exercícios é recomendado para que o caderno possa ser resolvido sem depender das páginas de teoria. O perfil da banca pode ser registrado em arquivo próprio.

Os capítulos começam no nível H2; o H1 e seu ID são gerados a partir do manifesto. Figuras ficam dentro da pasta, são declaradas no manifesto de figuras e recebem descrição no Markdown. As questões apontam para um objetivo ensinado e uma seção de teoria existente.

Os arquivos passam pelos JSON Schemas de material, questão, fontes, figuras e cobertura, com validação de datas e tipos. Campos desconhecidos não são ignorados silenciosamente. Os hashes de prova/gabarito de um item real precisam corresponder às fontes declaradas. Instale `requirements-core.txt`; a dependência é incluída em `requirements-pdf.txt`.

O exemplo completo está em [materials/dataprev-sql](../materials/dataprev-sql/README.md). O [modelo de manifesto](../templates/manifesto-material.json) e o [modelo de conteúdo](../templates/conteudo-capitulo.md) são pontos de partida. Os contratos estão em schemas; a pré-validação também verifica referências entre arquivos.

O [piloto de matemática](../materials/matematica-basica/README.md) demonstra fórmulas com `$...$` e `$$...$$`, convertidas para MathML nativo com descrição em palavras no texto. Não há carregamento de MathJax remoto. Confira fórmulas no PDF e mantenha equivalentes textuais; isso não certifica acessibilidade integral.

## Comandos

```sh
python scripts/build_material.py materials/dataprev-sql/material.json --check
python scripts/check_sql.py materials/dataprev-sql/verificacoes.json --report build/dataprev-sql/sql-validation.json
python scripts/build_material.py materials/dataprev-sql/material.json --pdf
python scripts/build_material.py materials/dataprev-sql/material.json --kind caderno --pdf
```

Use --output para escolher outra pasta de saída. Sem --pdf, o comando gera Markdown, HTML e relatório; os números de página no sumário são preenchidos quando o PDF é exportado. --check não gera o material.

Após revisar o lote, importe o manifesto no [acervo](acervo.md). Alterações em edições já registradas exigem nova versão. Revisões de questões são explícitas e preservam histórico; arquive o banco e a exportação fora do Git/cofre.

## O que as verificações garantem

- Arquivos de entrada locais, existentes e dentro da pasta do material.
- IDs de fontes/questões, objetivos, figuras e matriz sem referências inexistentes.
- Itens reais com identificação e hashes dos documentos; reprodução integral exige evidência de permissão.
- Itens somente-link sem reprodução automática do enunciado e alternativas, mesmo que esses campos existam na entrada.
- Sumário com páginas obtidas do PDF e conferidas após nova renderização; pares questão/resolução resolvidos.
- Relatório JSON com hashes de entradas e saídas, versão das ferramentas e resultado estrutural.
- No piloto SQL: resultados das consultas e erros esperados de integridade em bases em memória independentes.

Essas verificações não provam autenticidade pelo hash sozinho, equivalência de dificuldade, exatidão de todo conteúdo ou aprendizagem. A consulta aos documentos, a revisão técnica, a inspeção visual e a avaliação do leitor continuam necessárias.

## Melhorias verificadas no piloto

O caderno inclui a massa necessária para as questões. Questões e comentários são mantidos juntos quando couberem na página. SVGs incorporados respeitam a largura da coluna para não reduzir silenciosamente o tamanho de todo o texto. A auditoria do PDF registra a mediana do tamanho de trechos longos e impede publicação quando ela fica abaixo de 10 pt.

## Limites atuais

O sumário usa até dois níveis. A tipografia e os formatos são os desta versão; não há conformidade PDF/UA certificada. A revisão editorial é registrada separadamente dos checks. O publicador aceita conteúdo preparado pelo agente e não decide sozinho se uma fonte é confiável.

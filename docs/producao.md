# Produção de materiais — versão 0.7

O agente pesquisa e redige; o publicador monta e verifica os arquivos preparados. Esta versão já aceita materiais novos por manifesto e exporta apostila, caderno, simulado e revisão. Os dois novos formatos têm planos próprios; ver docs/simulados.md e docs/revisao-aprendizagem.md. Não há chamada automática a um LLM ou serviço de recebimento permanente.

## Da solicitação à entrega completa

Seguir [do-pedido-a-entrega.md](do-pedido-a-entrega.md). Aceitar texto, foto ou print; ler todas as skills/instruções e registrar o pedido. Em pedido completo, os lotes são unidades internas até concluir o escopo integral. Para entrega de concurso, vincular pedido.json e executar --check --final e --pdf --final. Os comandos dos pilotos abaixo permanecem builds de referência.

1. Ler README, AGENTS, Progress, Decisions, todas as skills, políticas/modelos/contratos e referências. Interpretar texto/imagem, pesquisar identidade e recuperar material disponível antes de perguntar.
2. Conferir edital e retificações oficiais. Mapear todo o programa do cargo, ou toda a matéria/seleção expressamente pedida; não reduzir para recorte por conveniência. Registrar IDs, objetivos e lacunas.
3. Buscar provas e gabaritos relacionados. Registrar ano, perfil, tipo, item, página, status e hash; separar análise da amostra de previsão de incidência.
4. Redigir capítulos com explicação, mecanismo, limites, exemplos resolvidos e recuperação ativa. Produzir figuras originais com legenda e descrição.
5. Preparar as questões autorais e os comentários. Itens reais com direitos não confirmados recebem acesso ao original por link. Nunca misturar um gabarito de outro ano/tipo.
6. Montar o manifesto e executar a pré-validação, as verificações técnicas pertinentes e a publicação. Revisar o conteúdo e inspecionar o PDF.
7. Concluir todas as unidades selecionadas, revisar cobertura e entregar os arquivos solicitados. Atualizar estado/decisões e evidências no Segundo Cérebro. Sem teto artificial de páginas; manter checkpoint de unidades pendentes até terminar.

## Arquivos de entrada

Uma pasta de material contém material.json, capítulos Markdown, questoes.json, fontes.json, figuras.json e cobertura.json. Um contexto de exercícios é recomendado para que o caderno possa ser resolvido sem depender das páginas de teoria. O perfil da banca pode ser registrado em arquivo próprio.

Os capítulos começam no nível H2; o H1 e seu ID são gerados a partir do manifesto. Figuras ficam dentro da pasta, são declaradas no manifesto de figuras e recebem descrição no Markdown. As questões apontam para um objetivo ensinado e uma seção de teoria existente.

Pandoc também é necessário em --check. A versão 0.6 usa a árvore de imagens do mesmo leitor Markdown da exportação, abrangendo sintaxe de referência, títulos e caminhos com espaços. Todos os formatos preparados são conferidos: capítulos, revisões, contexto de questões, perfil, enunciados e comentários. Uma figura pode ser exclusiva da revisão ou do contexto, desde que declarada e incluída nos hashes. Imagens remotas, caminhos fora da pasta e dependências externas/ativas dentro de SVG são recusados antes da incorporação. Não usar novos recursos em um objeto já carregado sem recarregar seu manifesto.

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

Antes de entregar, executar scripts/acessibilidade.py e registrar seus limites, além da [auditoria de links](navegacao.md) com --browser e --external. A exportação PDF já bloqueia rotas internas incorretas e grava *-navigation.json. Arquivar esse manifesto com HTML/PDF e conferir o mesmo hash após upload. O sumário e os links usam o mesmo contrato em apostilas de conteúdo e cadernos de questões.

O sumário inteiro é obrigatoriamente clicável nos quatro formatos. O publicador 0.7 converte links internos para destinos diretos de página/posição e confere número, título, página e intervalo contínuo de cada linha, incluindo o pontilhado. Qualquer falha bloqueia o PDF. Uma mudança nesse motor exige teste adicional em visualizador PDF independente, além do teste HTML; registrar a ferramenta e os bytes usados conforme docs/navegacao.md.

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

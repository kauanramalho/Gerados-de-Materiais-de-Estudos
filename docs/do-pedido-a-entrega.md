# Do pedido simples à apostila do concurso

## Compromisso de funcionamento

O usuário pode escrever “Vou fazer o concurso X, quero a apostila”, enviar uma foto/print com esse pedido ou pedir “quero um caderno de questões”. Não precisa conhecer skills, preparar JSON, fornecer edital ou descobrir a banca. Com o projeto disponível na sessão, o agente assume identificação, pesquisa, planejamento, escrita, revisão, publicação dos arquivos e documentação.

**Escopo padrão:** todo o programa vigente aplicável ao cargo/especialidade identificado. Se o usuário escolher uma matéria ou recorte, cobrir integralmente essa seleção. Não converter um pedido completo em capítulo piloto, resumo, pequena amostra ou plano de trabalho. Os pilotos existentes são referências de validação e não definem o tamanho da entrega.

**Extensão:** não há teto artificial de páginas, capítulos ou questões. Produzir a explicação, as figuras, os exemplos e a prática necessários aos objetivos, sem enchimento ou redução da fonte para caber. Trabalhar internamente por unidades e registrar continuidade até concluir o escopo; uma unidade concluída não encerra o pedido completo. Limites reais de ferramenta/sessão devem ser registrados com o estado recuperável, sem chamar um resultado parcial de completo nem prometer execução em segundo plano. O publicador não fixa máximo de páginas; isso não significa recursos computacionais infinitos.

## 1. Receber texto, foto ou print

Preservar o pedido original e a imagem em `work/<pedido>/`, fora do Git público. Abrir a imagem com ferramenta de visão; transcrever órgão, cargo, especialidade, ano, banca e endereço que estiverem legíveis. OCR é auxiliar: conferir a leitura contra a imagem, especialmente números e nomes. Marcar `conferida` somente depois dessa inspeção. Uma imagem publicitária ou recorte de notícia serve como pista e não substitui o edital oficial.

Pesquisar por conta própria antes de perguntar. Perguntar somente quando identidade, cargo/especialidade ou versão continuarem materialmente ambíguos depois da pesquisa, ou quando a imagem não permitir recuperar uma informação indispensável. Enquanto isso, avançar no que for independente. Não escolher um cargo por conveniência.

O agente pode iniciar o registro com:

```sh
python scripts/pedido.py iniciar --id concurso-x --texto 'Vou fazer o concurso X, quero a apostila' --output work/concurso-x
python scripts/pedido.py iniciar --id concurso-x-questoes --imagem /caminho/print.png --origem print --tipo caderno --output work/concurso-x-questoes
```

PNG, JPEG e WebP são aceitos na ingestão local. Converter outros formatos com ferramenta adequada, preservando o original privado. A CLI preserva bytes/hash e cria estado pendente; a visão e a pesquisa são tarefas do agente, não funções de OCR/busca escondidas no script.

## 2. Carregar todo o método

Ler README, AGENTS, Progress e Decisions; todas as 17 skills; os documentos de políticas, os modelos, os contratos e o catálogo de referências do projeto. Ler o índice do acervo e os materiais anteriores antes de decidir o que reutilizar; abrir os exemplos e fontes anteriores pertinentes ao novo conteúdo. Não importar cegamente conteúdo de um piloto para outro concurso.

`pedido.contexto` lista instruções, skills, documentos, modelos, schemas e referências com seus hashes. `lido_em` começa nulo. O agente só preenche a data depois de ler o arquivo. `python scripts/pedido.py contexto` produz o inventário atual; arquivo novo ou alterado exige nova leitura antes da entrega final. Esse registro documenta uma ação do agente; gerar o inventário não lê nem compreende os arquivos automaticamente. Progress e Decisions são consultados como estado mutável, sem confundi-los com as instruções permanentes.

## 3. Pesquisar o concurso e a banca

Executar e registrar as oito etapas do pedido, inclusive nos cadernos de questões:

| Etapa | Pesquisa e evidência |
|---|---|
| Identificação | página oficial do órgão/banca, cargo, especialidade, ano e modalidade |
| Edital | versão aplicável, anexo do cargo, conteúdo programático literal, URL, páginas, data e hash |
| Retificações | consulta ao portal oficial e documentos que alterem conteúdo ou regras; registrar o que foi encontrado |
| Banca | regras da prova, formato dos itens, disciplinas, pesos, penalidades e tempo quando publicados |
| Provas do alvo | edições anteriores do mesmo concurso/cargo, cadernos e gabaritos correspondentes |
| Provas relacionadas | mesma banca, área, nível e objetivos; justificar aproximações e excluir itens fora do programa atual |
| Fontes de conteúdo | legislação/documentação oficial, referências técnicas e acadêmicas pertinentes, vigência e direitos |
| Acervo | recuperar o catálogo disponível, procurar itens e versões, conferir novamente a fonte oficial antes de reutilizar |

Guardar em `pesquisa` consultas efetivamente feitas, resultado, URL/referência, localizador, data e natureza oficial. Resultado de busca serve para descoberta; abrir o documento necessário antes de afirmá-lo como consultado. “Não localizado” descreve o resultado da pesquisa, não prova inexistência. Fontes indisponíveis ficam como lacuna, sem questões reais inventadas. Ausência de acervo local deve ser registrada e não impede pesquisa externa.

Para a prova relacionada, priorizar: mesmo concurso/cargo → mesma banca e área/nível → mesma banca e objetivo → outra banca com compatibilidade justificada. A proximidade nunca autoriza incluir assunto fora do edital escolhido ou atribuir uma questão de outro concurso ao concurso-alvo. Frequência e perfil se apoiam na amostra efetivamente lida, sem prometer incidência futura.

Identidade e edital ainda não publicados/conferidos permitem pesquisa e rascunho com limites claros; não permitem rotular como apostila final completa do edital vigente. Diante de pré-edital, registrar essa condição e o programa de referência explicitamente acordado, sem substituir silenciosamente um edital futuro por um antigo.

## 4. Converter o edital em cobertura completa

Enumerar em `programa` todos os itens e subitens aplicáveis ao cargo, preservando texto e localizador da fonte, sem agrupar omissões sob “demais assuntos”. Em pedido completo, `escopo.selecao` contém todos esses IDs. Em pedido de matéria/recorte, selecionar somente os itens pedidos e registrar a delimitação. O agente prepara esse registro; o usuário não precisa preenchê-lo.

Na matriz, `edital_id` liga o item selecionado aos objetivos, capítulos e questões. O texto de `edital_item` deve coincidir com o programa registrado. Cada questão precisa avaliar um objetivo daquele item. Pré-requisito necessário é identificado e justificado; não vira um bloco de questões alheias ao concurso. Usar o perfil da banca para forma e nível editorial, e o edital para decidir o que entra.

## 5. Produzir o formato solicitado

**Apostila:** cobrir todos os itens selecionados com explicação desenvolvida, fundamentos necessários, exemplos resolvidos, figuras que ensinem, prática progressiva, sínteses e referências. Aplicar o layout aprovado. Não reduzir o programa para terminar um número arbitrário de páginas.

**Caderno:** realizar a mesma pesquisa e a mesma seleção do edital. Reunir questões reais autênticas compatíveis e criar autorais identificadas para a matriz, com comentários por alternativa, justificativa do resultado e dados necessários à resolução. Registrar ausência de itens reais em algum assunto e preencher com autorais adequadas; nunca forjar origem. A quantidade decorre da cobertura e variedade dos objetivos; não criar uma cota idêntica para todo assunto sem justificativa. Os comentários ficam no próprio PDF; remissões à teoria obedecem ao suporte de navegação documentado.

Reaproveitar material existente apenas após conferir pertinência, versão técnica/legal, direitos e gabarito. Separar resposta oficial, comentário do projeto e dificuldade estimada. Conferir figuras e cálculos; não declarar calibração empírica ou qualidade didática perfeita por validação automática.

## 6. Conferir e entregar

Adicionar `"pedido": "pedido.json"` ao manifesto do material, mantendo o pedido e seus anexos dentro da pasta desse material. A pasta privada criada na ingestão pode se tornar a pasta do material; preparar ali os capítulos e as listas JSON. Não colocar pedido pessoal/imagem no repositório público. A CLI bloqueia caminhos para fora da pasta.

```sh
python scripts/pedido.py verificar work/concurso-x/pedido.json
python scripts/build_material.py work/concurso-x/material.json --check --final
python scripts/build_material.py work/concurso-x/material.json --pdf --final
python scripts/audit_links.py build/concurso-x/apostila.pdf --browser --external --report build/concurso-x/auditoria-entrega.json
```

Para caderno, usar `--kind caderno` nos dois comandos do publicador e auditar `caderno.pdf`. `--output` escolhe a pasta dos artefatos. Uma execução sem `--final` é rascunho/referência e não certifica o atendimento de um pedido de concurso.

O modo final exige identidade/edital, leitura atual das instruções, todas as etapas de pesquisa documentadas, formato correto, texto/IDs compatíveis e conteúdo/prática completos para cada item solicitado. Detecta questões e objetivos fora da matriz, omissões, leitura desatualizada e edital com hash diferente das fontes. Os metadados não provam sozinhos a veracidade da pesquisa, a exatidão da extração do edital ou a profundidade pedagógica: o agente precisa comparar a matriz com o documento oficial e revisar o conteúdo.

Somente depois corrigir defeitos críticos, consolidar o PDF, conferir sumário e todos os links, arquivar os hashes e verificar os bytes no destino. Entregar o material solicitado, não apenas um plano. Registrar cobertura, limitações, fontes, edição e evidências no projeto/Segundo Cérebro. A necessidade de uma confirmação de identidade não deve ser repetida como autorização de publicação já concedida.

## Retomada de materiais extensos

Usar [estado-producao.md](../templates/estado-producao.md) como checkpoint: IDs concluídos e pendentes, arquivos, fontes, defeitos, próxima unidade e instruções já lidas. Se uma ferramenta falhar, retomar daí e continuar até consolidar todo o pedido. Arquivos parciais são identificados como parciais. O suporte a links entre PDFs separados continua exigindo implementação própria; não fabricar links entre volumes com base na validação de um único PDF.

O fluxo opera numa sessão do agente com acesso ao projeto, visão, pesquisa e ferramentas de arquivos. Não exige que o usuário opere a CLI. Em outra conversa, é necessário disponibilizar o projeto/pacote ou recuperá-lo pelo Drive; a documentação não cria memória automática nem um serviço permanente.

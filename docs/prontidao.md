# O que falta para o Ateliê de Estudos ficar pronto

Diagnóstico de 03/11/2026, após conferir código, instruções, exemplos, marcos e registros do projeto. Base técnica examinada: revisão `fa65ffb`. Esta análise não substitui a avaliação de aprendizagem pelo leitor.

## O que já funciona

O projeto já pode ser usado em uma tarefa acompanhada por um agente: pesquisar o concurso, preparar conteúdo e gerar apostila ou caderno a partir de um manifesto. Há 12 skills redigidas, manual editorial, padrões visuais, políticas de fontes/questões, modelos e contratos. O piloto SQL produziu 24 páginas de apostila e 15 de caderno, três diagramas, oito questões autorais e três questões reais por link oficial. Foram registrados 18 testes, 13 verificações SQL e navegação conferida nos PDFs.

Isso é uma primeira versão utilizável. Ainda não comprova qualidade constante em qualquer matéria, acervo pesquisável, cobertura de um edital inteiro ou execução permanente sem uma sessão do agente.

## Três significados de pronto

| Nível | Critério de conclusão | Situação |
|---|---|---|
| Produzir um lote acompanhado | fontes conferidas, conteúdo revisado, figuras e questões coerentes, HTML/PDF navegáveis, limites declarados | aplicado ao piloto; aceite do leitor pendente |
| V1 para uso recorrente | fluxo repetível em matérias distintas, revisões registradas, formatos prometidos testados e manutenção de edições | faltam as entregas abaixo |
| Coleção de um concurso | cada item do edital tem conteúdo e prática, ou lacuna justificada; todas as unidades passam pela revisão | depende do concurso e dos lotes que forem solicitados |

Um serviço que recebe documentos e trabalha continuamente é uma evolução opcional. Aplicativo web, APIs pagas, instalação global e agendamento não são requisitos para cumprir o modelo original de projeto operado pelo agente. Também não é necessário escrever materiais de todos os concursos para terminar o método.

## Pendências por entrega

| Entrega | O que existe | O que falta e como encerrar | Backlog |
|---|---|---|---|
| Publicação GitHub | Git local, ZIP, bundle e workflow básico | criar/acessar repositório público, enviar histórico, ler árvore/SHA e verificar execução remota | AE-004 |
| Avaliação didática | revisão técnica e visual inicial | registrar clareza, densidade, leitura das figuras e tentativa de exercícios; converter achados em correções, sem inventar aceite | AE-009 |
| Referência editorial profissional | catálogo de páginas e guias; estilo e sumário próprios | comparar páginas efetivas de dois ou três capítulos abertos: explicação, exemplo, legenda, exercícios e respiro; registrar páginas e ajustes | AE-015 |
| Publicador em outras matérias | manifesto, apostila e caderno validados em SQL | testar fórmulas, tabelas longas, imagens detalhadas e texto normativo; verificar paginação e links; corrigir falhas encontradas | AE-010, AE-016 |
| Acervo reutilizável | registros locais do piloto e perfil com dez itens selecionados | catálogo consultável por banca/cargo/ano/assunto, identidade estável, deduplicação, direitos e atualização de gabaritos; testar busca e revisões | AE-011 |
| Simulados | regra editorial prevista | seleção e distribuição por matriz, tempo e pontuação conforme fonte da banca, respostas separadas e conferência de pontuação/anulações | AE-017 |
| Revisões | síntese dentro do capítulo | formato próprio de revisão curta, perguntas de recuperação e retorno ao capítulo; validar que não substitui o ensino inicial | AE-018 |
| Contratos e erros | schemas de briefing/questão/material e validações manuais na CLI | schemas de fontes, figuras e cobertura; validação consistente dos tipos e datas, erros compreensíveis e testes de entradas incorretas | AE-019 |
| Acessibilidade | hierarquia e descrições no HTML; checagens visuais e links | testar teclado/leitura, contraste, alternativas textuais, fórmulas e ordem de leitura do PDF; corrigir e documentar limites. Não declarar PDF/UA sem auditoria | AE-012 |
| Atualização e erratas | política geral e versões nos manifestos | procedimento de retificação de edital, norma, fonte ou gabarito; localizar capítulos afetados, revisar respostas, preservar IDs e emitir errata verificável | AE-020 |
| Retomada e reprodução | instruções, hashes e verificações locais | executar instalação/build em ambiente limpo e retomar um pedido com contexto mínimo; ampliar CI para artefatos e conferir o resultado remoto | AE-022 |
| Validação das skills | procedimentos escritos e aplicação inicial de vários deles | registrar entrada, saída, limites e evidência por procedimento, corrigindo instruções genéricas a partir dos próximos lotes | AE-023 |
| Coleção completa | recorte SQL com lacunas declaradas | produzir capítulos, figuras e questões dos demais itens do edital escolhido; auditar cobertura e links entre volumes | AE-021 |

## Skills: ampliar as existentes e criar só módulos distintos

As 12 skills básicas já existem. Não é necessário reescrevê-las para começar. A aplicação de um piloto não fecha a validação de todas elas; veja [o inventário e as evidências](skills.md).

**Aprofundar as atuais:** `ae-analisar-edital` e `ae-pesquisar-fontes` para OCR, retificações e vigência; `ae-analisar-banca` para critérios de amostragem por formato; `ae-escrever-capitulo` e `ae-ilustrar` para matérias e figuras diferentes; `ae-questoes-autorais` para revisão de ambiguidades e originalidade; `ae-diagramar` e `ae-revisar` para fórmulas, tabelas e acessibilidade; `ae-gerenciar` para fechamento verificável das edições.

Cinco módulos candidatos têm responsabilidade distinta. Estão **planejados, ainda não criados nem instalados**:

| Skill candidata | Procedimento a desenvolver | Evidência necessária |
|---|---|---|
| `ae-curar-acervo` | catalogar, buscar, deduplicar e versionar provas/questões | localizar itens corretos, reconhecer duplicatas e atualizar status sem perder histórico |
| `ae-montar-simulado` | montar matriz, selecionar questões, separar respostas e pontuar | simulado conferido contra regras oficiais e teste de anulação/pontuação |
| `ae-produzir-revisao` | condensar o que já foi ensinado e criar recuperação ativa | revisão com remissões corretas e avaliação de utilidade pelo leitor |
| `ae-atualizar-material` | analisar mudanças de fontes/edital/gabarito e emitir errata | exemplo de mudança com impacto rastreado, edição revisada e IDs preservados |
| `ae-auditar-acessibilidade` | verificar equivalentes textuais, navegação e ordem de leitura | relatório com testes efetivos, defeitos corrigidos e limites explícitos |

Criar um SKILL.md não implementa sozinho catálogo, pontuação ou atualização. Cada módulo deve nascer junto do fluxo e da evidência que o sustentam. OCR pode permanecer como parte das skills existentes, sem virar uma skill duplicada.

## Markdown e documentação ainda necessários

Esta revisão acrescenta este diagnóstico, um [modelo de avaliação do piloto](../templates/avaliacao-piloto.md) e um [checklist preenchível de revisão](../templates/checklist-revisao.md). Os demais arquivos abaixo são entregas planejadas; os nomes são propostas, não arquivos já disponíveis.

| Arquivo proposto | Conteúdo que precisa ser desenvolvido | Momento |
|---|---|---|
| `docs/acervo.md` | identidade, seleção, busca, deduplicação, direitos e revisão do catálogo | AE-011 |
| `docs/simulados.md` e `templates/plano-simulado.md` | distribuição, regras de aplicação, pontuação e respostas separadas | AE-017 |
| `docs/revisao-aprendizagem.md` e `templates/revisao.md` | revisão curta e recuperação ativa com remissões | AE-018 |
| `docs/acessibilidade.md` | testes, limitações e decisões de exportação por formato | AE-012 |
| `docs/manutencao-edicoes.md` e `templates/errata.md` | mudanças, impacto e histórico de correções | AE-020 |
| `docs/validacao-multimateria.md` | resultados dos novos pilotos; não criar parecer de aprovação antes dos testes | AE-016 |
| `materials/<lote>/README.md` e relatório da execução | escopo, fontes, cobertura, revisão e entrega de cada lote | durante a produção |

**No Segundo Cérebro:** manter este plano e seus estados, a avaliação do leitor quando ocorrer, decisões editoriais que mudarem o padrão, evidências por skill e índice das edições com links. Novas skills recebem cartões independentes e entrada no índice quando realmente forem criadas. Os cartões atuais não certificam instalação global. PDF, HTML, anexos e backups ficam no Drive fora do cofre; segredos e originais privados não vão ao Git público. Não criar capturas repetidas de cada atualização de status.

## Materiais que faltam produzir para testar o método

1. **Piloto visual em outra matéria:** um capítulo com componentes identificados, por exemplo redes e equipamentos, apoiado em fonte técnica do modelo ou rotulado como esquema genérico.
2. **Recorte com fórmulas e tabelas:** exemplo resolvido, notação, unidades, impressão e alternativas textuais conferidos.
3. **Recorte normativo quando pertinente ao edital:** dispositivo, vigência e data de corte, com atualização rastreável. Pode ser combinado com o lote de outra matéria se cobrir esses casos de teste.
4. **Simulado e revisão curta:** primeiros exemplares completos para validar os novos formatos.
5. **Coleção do concurso escolhido:** produzida por lotes após ajustar o padrão; quantidade de páginas e questões depende da cobertura, sem metas arbitrárias.

Esses são recortes de validação propostos. Ainda não foram produzidos como novos materiais nem atribuídos a uma prioridade pessoal do titular.

## Ordem recomendada

Avaliar e ajustar o piloto enquanto se resolve o acesso GitHub; aprofundar a comparação editorial; validar outra matéria e os casos de impressão; consolidar contratos, acessibilidade e reprodução; estruturar acervo e manutenção; então adicionar simulado/revisão e ampliar a coleção. Feedback do leitor não bloqueia pesquisa e desenvolvimento que independam dele.

## Correções de estado nesta revisão

O backlog anterior marcava AE-009 e AE-011 como concluídos e AE-012 em execução. Não havia registro de avaliação do titular, implementação do catálogo consultável nem auditoria de acessibilidade em andamento que sustentassem esses estados. Foram reconciliados como planejados. A revisão técnica do piloto e os registros locais de questões continuam preservados. O resumo da arquitetura foi atualizado para reconhecer a CLI 0.2 já existente.

## Publicação: autorização e capacidade técnica

A autorização pública foi reiterada pelo titular. Nesta revisão, a conta autenticada foi confirmada, a consulta do destino retornou 404 e as tentativas por GraphQL e REST retornaram 403 `Resource not accessible by integration`. A conexão instalada não conseguiu criar o repositório. Não houve push, issues ou CI remota. É necessário acesso técnico que permita criar o destino ou um repositório vazio acessível à integração. Não falta nova autorização textual do titular.

# Backlog executável

Estados: pronto, em execução, concluído, impedido, planejado. A ordem abaixo é de dependência, sem substituir prioridade definida pelo titular.

| ID | Entrega | Aceite | Dependência | Estado |
|---|---|---|---|---|
| AE-001 | fundação e 12 skills | procedimentos e links locais válidos | nenhuma | concluído |
| AE-002 | catálogo editorial | fontes abertas consultadas, decisões e licenças registradas | AE-001 | concluído |
| AE-003 | prova de navegação | HTML/PDF com figura, sumário e questão ↔ solução conferidos | AE-001 | concluído |
| AE-004 | publicação GitHub | repositório público, árvore e SHA confirmados | permissão de criação ou repo vazio | impedido |
| AE-005 | registro no Segundo Cérebro | projeto, cartões, índice e relatório lidos após escrita | regras do cofre | concluído |
| AE-006 | identificar primeiro concurso | órgão/cargo/ano e edital/retificações confirmados | referência metodológica Dataprev/FGV; sem alterar prioridade | concluído |
| AE-007 | analisar provas relacionadas | perfil de banca com amostra e limitações | AE-006 | concluído |
| AE-008 | produzir capítulo piloto | estrutura editorial completa e revisão técnica | AE-007 | concluído |
| AE-009 | avaliar piloto com titular | retorno real registrado e comentários convertidos em ajustes verificáveis | AE-008 | planejado |
| AE-010 | generalizar publicador | entradas estruturadas, erros claros e testes de navegação | piloto técnico; aceite pedagógico pendente | em execução |
| AE-011 | acervo consultável de provas e questões | busca e deduplicação testadas; proveniência, direitos e atualização preservados | AE-007; registros do piloto são entrada, não acervo concluído | planejado |
| AE-012 | exportação acessível | teclado, descrições, contraste, fórmulas e ordem de leitura testados; limites registrados | AE-010 | planejado |
| AE-013 | verificação SQL em massa independente | 13 casos com resultados esperados conferidos | AE-008 | concluído |
| AE-014 | controle de impressão | escala SVG, quebras de questões e tamanho do texto conferidos no piloto | AE-008 | concluído |
| AE-015 | comparar referências editoriais em páginas reais | dois ou três capítulos abertos analisados, edição/páginas e ajustes próprios registrados | AE-002 | planejado |
| AE-016 | validar matérias e casos de impressão distintos | novo lote e casos de fórmulas, tabelas, figuras detalhadas e texto normativo revisados | AE-010; feedback não bloqueia testes independentes | planejado |
| AE-017 | formato de simulado | matriz, respostas separadas, regras de pontuação e anulação testadas em um exemplar | AE-010, AE-007 | planejado |
| AE-018 | formato de revisão e recuperação ativa | revisão curta com perguntas e remissões à teoria, aplicada em um exemplar | AE-008 | planejado |
| AE-019 | consolidar contratos e erros da CLI | schemas de fontes/figuras/cobertura e validações coerentes de tipos/datas com erros úteis | AE-010 | planejado |
| AE-020 | manutenção de edições e erratas | mudança de fonte/gabarito com impacto rastreado, nova edição e IDs preservados | AE-008; articulação com AE-011 | planejado |
| AE-021 | coleção de um concurso | itens do edital cobertos ou com lacuna justificada; capítulos e prática revisados | concurso/recorte definidos e padrão ajustado | planejado |
| AE-022 | reprodução e retomada | build em ambiente limpo e retomada de tarefa registrados; CI remota conferida quando publicada | AE-010; AE-004 para execução remota | planejado |
| AE-023 | validar e aprofundar skills | evidência por procedimento; módulos novos criados junto do fluxo que implementam | lotes pertinentes; ver docs/prontidao.md | planejado |

Responsável pela execução: agente na tarefa autorizada; titular decide concurso, preferência visual final e prioridades pessoais. Issues no GitHub devem espelhar os itens abertos quando o repositório existir; não afirmar que foram criadas antes da confirmação remota.

## Reconciliação de 03/11/2026

AE-009 e AE-011 estavam marcados como concluídos, e AE-012 como em execução, sem evidência suficiente para esses estados. Retorno do titular, acervo consultável e auditoria de acessibilidade permanecem planejados. O material do piloto e suas verificações continuam válidos dentro dos limites registrados. A autorização para publicar foi reiterada, mas AE-004 continua impedido pelo 403 observado na integração.

Ver [diagnóstico de prontidão](prontidao.md) para skills candidatas, Markdown previsto, critérios e ordem de execução. A produção dos próximos lotes não exige terminar todo o acervo ou contratar um serviço.

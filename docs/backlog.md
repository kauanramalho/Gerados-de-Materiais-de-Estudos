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
| AE-009 | avaliar piloto com titular | layout aprovado em 03/11/2026; clareza, aprendizagem e dificuldade ainda sem avaliação do leitor | AE-008 | em execução |
| AE-010 | generalizar publicador | entradas estruturadas, erros claros e navegação testados em SQL/matemática, apostila/caderno | núcleo 0.3 entregue; novos formatos em AE-017/018 | concluído |
| AE-011 | acervo consultável de provas e questões | 17 itens, filtros, deduplicação, revisões e direitos testados | AE-007; expansão por lote e consulta oficial permanecem necessárias | concluído |
| AE-012 | exportação acessível | teclado, descrições, contraste, fórmulas e ordem de leitura testados; limites registrados | AE-010 | planejado |
| AE-013 | verificação SQL em massa independente | 13 casos com resultados esperados conferidos | AE-008 | concluído |
| AE-014 | controle de impressão | escala SVG, quebras de questões e tamanho do texto conferidos no piloto | AE-008 | concluído |
| AE-015 | comparar referências editoriais em páginas reais | dois ou três capítulos abertos analisados, edição/páginas e ajustes próprios registrados | duas seções HTML consultadas; comparação PDF completa pendente | em execução |
| AE-016 | validar matérias e casos de impressão distintos | novo lote e casos de fórmulas, tabelas, figuras detalhadas e texto normativo revisados | matemática/fórmulas/tabela entregues; texto normativo/equipamento detalhado pendentes | em execução |
| AE-017 | formato de simulado | matriz, respostas separadas, regras de pontuação e anulação testadas em um exemplar | AE-010, AE-007 | planejado |
| AE-018 | formato de revisão e recuperação ativa | revisão curta com perguntas e remissões à teoria, aplicada em um exemplar | AE-008 | planejado |
| AE-019 | consolidar contratos e erros da CLI | schemas de fontes/figuras/cobertura, tipos/datas e erros úteis com testes negativos | publicador 0.3 | concluído |
| AE-020 | manutenção de edições e erratas | mudança de fonte/gabarito com impacto rastreado, nova edição e IDs preservados | AE-008; articulação com AE-011 | planejado |
| AE-021 | coleção de um concurso | itens do edital cobertos ou com lacuna justificada; capítulos e prática revisados | concurso/recorte definidos e padrão ajustado | planejado |
| AE-022 | reprodução e retomada | build em ambiente limpo e retomada de tarefa registrados; CI remota conferida quando publicada | Python isolado no mesmo host testado; retomada/CI remota pendentes | em execução |
| AE-023 | validar e aprofundar skills | evidência por procedimento; módulos novos criados junto do fluxo que implementam | ae-curar-acervo aplicada; demais validações ainda pendentes | em execução |
| AE-024 | tornar obrigatória a navegação correta | sumário, questão/resolução/retorno/teoria, áreas reais e hashes auditados; regressões negativas e cliques nos quatro materiais | AE-010; contrato em docs/navegacao.md | concluído |

Responsável pela execução: agente na tarefa autorizada; titular decide concurso, preferência visual final e prioridades pessoais. Issues no GitHub devem espelhar os itens abertos quando o repositório existir; não afirmar que foram criadas antes da confirmação remota.

## Reconciliação de 03/11/2026

Na auditoria inicial, AE-009 e AE-011 estavam marcados como concluídos, e AE-012 como em execução, sem evidência suficiente. Os estados foram corrigidos. Na entrega 0.3 posterior, AE-011 foi implementado e testado. Depois, o titular aprovou o layout e pediu a checagem contínua dos links; AE-009 passou a em execução e AE-024 foi implementado. Avaliação pedagógica do titular e auditoria integral de acessibilidade continuam pendentes. AE-004 permanece impedido pelo 403 observado na integração; nenhuma autorização adicional foi inferida como acesso técnico.

Ver [diagnóstico de prontidão](prontidao.md) para skills candidatas, Markdown previsto, critérios e ordem de execução. A produção dos próximos lotes não exige terminar todo o acervo ou contratar um serviço.

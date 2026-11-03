# Backlog executável

Estados: pronto, em execução, concluído, impedido, planejado. A ordem abaixo é de dependência, sem substituir prioridade definida pelo titular.

| ID | Entrega | Aceite | Dependência | Estado |
|---|---|---|---|---|
| AE-001 | fundação e 12 skills | procedimentos e links locais válidos | nenhuma | concluído |
| AE-002 | catálogo editorial | fontes abertas consultadas, decisões e licenças registradas | AE-001 | concluído |
| AE-003 | prova de navegação | HTML/PDF com figura, sumário e questão ↔ solução conferidos | AE-001 | concluído |
| AE-004 | publicação GitHub | repositório público, histórico inicial preservado, SHA e CI confirmados | destino informado pelo titular | concluído |
| AE-005 | registro no Segundo Cérebro | projeto, cartões, índice e relatório lidos após escrita | regras do cofre | concluído |
| AE-006 | identificar primeiro concurso | órgão/cargo/ano e edital/retificações confirmados | referência metodológica Dataprev/FGV; sem alterar prioridade | concluído |
| AE-007 | analisar provas relacionadas | perfil de banca com amostra e limitações | AE-006 | concluído |
| AE-008 | produzir capítulo piloto | estrutura editorial completa e revisão técnica | AE-007 | concluído |
| AE-009 | avaliar piloto com titular | layout aprovado em 03/11/2026; clareza, aprendizagem e dificuldade ainda sem avaliação do leitor | AE-008 | em execução |
| AE-010 | generalizar publicador | entradas estruturadas, erros claros e navegação testados em SQL/matemática, apostila/caderno | núcleo 0.3 entregue; novos formatos em AE-017/018 | concluído |
| AE-011 | acervo consultável de provas e questões | 17 itens, filtros, deduplicação, revisões e direitos testados | AE-007; expansão por lote e consulta oficial permanecem necessárias | concluído |
| AE-012 | exportação acessível | teclado/foco, contraste, descrições, MathML, tags e títulos medidos; limites assistivos declarados | AE-010 | concluído |
| AE-013 | verificação SQL em massa independente | 13 casos com resultados esperados conferidos | AE-008 | concluído |
| AE-014 | controle de impressão | escala SVG, quebras de questões e tamanho do texto conferidos no piloto | AE-008 | concluído |
| AE-015 | comparar referências editoriais em páginas reais | dois ou três capítulos abertos analisados, edição/páginas e ajustes próprios registrados | páginas PDF de dois capítulos comparadas; curadoria registrada | concluído |
| AE-016 | validar matérias e casos de impressão distintos | novo lote e casos de fórmulas, tabelas, figuras detalhadas e texto normativo revisados | SQL, matemática e demonstrador redes/LGPD verificados | concluído |
| AE-017 | formato de simulado | matriz, respostas separadas, regras de pontuação e anulação testadas em um exemplar | AE-010, AE-007 | concluído |
| AE-018 | formato de revisão e recuperação ativa | revisão curta com perguntas e remissões à teoria, aplicada em um exemplar | AE-008 | concluído |
| AE-019 | consolidar contratos e erros da CLI | schemas de fontes/figuras/cobertura, tipos/datas e erros úteis com testes negativos | publicador 0.3 | concluído |
| AE-020 | manutenção de edições e erratas | mudança de fonte/gabarito com impacto rastreado, nova edição e IDs preservados | AE-008; articulação com AE-011 | concluído |
| AE-021 | coleção de uma seleção de edital | todos os 17 itens de Banco de Dados, Dataprev/FGV Perfil 3, com teoria e prática revisadas | recorte escolhido pelo titular; outras matérias não incluídas | concluído |
| AE-022 | reprodução e retomada | estado 0.4 retomado e pipeline reproduzido em host GitHub; verify/artifacts aprovados | CI remota e evidências de fechamento | concluído |
| AE-023 | validar e aprofundar skills | 17 procedimentos aplicados com evidências e limites; cartões individuais | caso real BD e regressão dos formatos existentes | concluído |
| AE-024 | tornar obrigatória a navegação correta | sumário, questão/resolução/retorno/teoria, áreas reais e hashes auditados; regressões negativas e cliques nos quatro materiais | AE-010; contrato em docs/navegacao.md | concluído |
| AE-025 | pedido simples e cobertura focada no concurso | texto/foto/print preservados, pesquisa/contexto registrados, escopo integral sem teto de páginas e --final com testes negativos | contrato/ingestão entregues; aplicação real completa permanece em AE-021/028 | concluído |
| AE-026 | validar imagens em todas as entradas renderizadas | revisão e contexto rejeitam recursos não declarados/fora da pasta antes do Pandoc; recursos válidos entram nos hashes; regressões negativas e positivas | regressões e caso real 0.6 | concluído |
| AE-027 | propagar mudanças de figuras na comparação de edições | imagem alterada sinaliza capítulos dependentes e revisão relacionada, ou usa sinalização conservadora explícita; regressão reproduzível | regressões e caso real 0.6 | concluído |
| AE-028 | comprovar pedido real de ponta a ponta | texto e print de edital conferidos, fontes oficiais pesquisadas; apostila/caderno cobrem os 17 itens, --final e revisão editorial por IA; artefatos auditados | caso BD escolhido pelo titular; retorno real de aprendizagem separado em AE-009 | concluído |

Responsável pela execução: agente na tarefa autorizada; titular decide concurso, preferência visual final e prioridades pessoais. Issues no GitHub devem espelhar os itens abertos quando o repositório existir; não afirmar que foram criadas antes da confirmação remota.

## Reconciliação de 03/11/2026

Na auditoria inicial, AE-009 e AE-011 estavam marcados como concluídos, e AE-012 como em execução, sem evidência suficiente. Os estados foram corrigidos. Na entrega 0.3 posterior, AE-011 foi implementado e testado. Depois, o titular aprovou o layout e pediu a checagem contínua dos links; AE-009 passou a em execução e AE-024 foi implementado. Avaliação pedagógica do titular e auditoria integral de acessibilidade continuam pendentes. O titular forneceu destino público com escrita confirmada; AE-004 passou a em execução. O 403 de criação fica como histórico, sem substituir a conferência de envio/CI.

Ver [diagnóstico de prontidão](prontidao.md) para skills candidatas, Markdown previsto, critérios e ordem de execução. A produção dos próximos lotes não exige terminar todo o acervo ou contratar um serviço.

## Auditoria completa de 03/11/2026

AE-026/027 registram defeitos novos, ainda sem correção; AE-028 separa o aceite real dos contratos sintéticos já entregues em AE-025 e da reprodução técnica em AE-022. AE-009 e AE-023 continuam abertos. A [auditoria](auditoria-v05.md) contém provas, limites e critérios de encerramento. Os parágrafos anteriores descrevem a evolução histórica; não significam que o projeto inteiro esteja concluído.

## Resolução dos achados — versão 0.6

AE-026/027 corrigidos com regressões; AE-021/028 comprovados no recorte real escolhido, e AE-023 com aplicação delimitada das 17 skills. A auditoria 0.5 e os estados anteriores permanecem como histórico. São 138 testes locais e 22 verificações SQL. Ver [caso real](validacao-real-dataprev.md) e [matriz das skills](validacao-skills-v06.md).

Somente AE-009 permanece em acompanhamento: retorno real de clareza, aprendizagem e dificuldade. O [protocolo](avaliacao-pedagogica.md) está pronto. Não há arquivo, skill ou correção técnica obrigatória conhecida ainda por desenvolver para o funcionamento pedido. Novas coleções e rechecagem de fontes são execuções futuras do método, não cobertura universal já produzida.

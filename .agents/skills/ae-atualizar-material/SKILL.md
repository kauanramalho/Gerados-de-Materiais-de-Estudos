---
name: ae-atualizar-material
description: Analisar alterações e emitir nova edição com impacto e errata rastreáveis.
version: 0.1.0
---

# Analisar alterações e emitir nova edição com impacto e errata rastreáveis.

## Quando usar

Em uma tarefa deste procedimento no Ateliê de Estudos, após ler o contexto e as políticas do projeto.

## Entradas

Edição anterior preservada, fontes/questões novas, motivo e evidência da mudança.

## Procedimento

1. Leia AGENTS e docs/manutencao-edicoes.md. Consulte a fonte oficial quando mudar edital, norma ou gabarito; não confundir teste sintético com retificação real.
2. Preserve a edição anterior e seus artefatos. Mantenha IDs dos itens que continuam sendo os mesmos; incremente a versão quando mudar conteúdo.
3. Execute scripts/edicoes.py com manifestos anterior/novo, --motivo, --report e --errata. Revise questões, capítulos e fontes sinalizados; mudança de fonte exige revisão conservadora de todos os capítulos.
4. Complete a errata com trecho anterior, correção, fundamento e revisor. IDs removidos devem ter justificativa; o relatório de impacto não aprova automaticamente a correção.
5. Recalcule e revise questões, regenere PDFs e reaudite links/acessibilidade. Confira bytes publicados; mantenha catálogo e histórico coerentes com a edição e documente no Segundo Cérebro.

## Saídas

Nova edição, impacto, errata preenchida e artefatos preservados.

## Validação

Alterações têm motivo e fundamento; versão mudou, IDs permaneceram rastreáveis e artefatos anteriores foram preservados.

## Limites

Procedimento local operado pelo agente, sem instalação global ou serviço permanente. Não inventar fontes, aprovação humana, equivalência de dificuldade, conformidade ou evidência. Conteúdo privado e originais ficam fora do Git público; preservar autoria por IA no Segundo Cérebro.

---
name: ae-orquestrar
description: Conduzir um pedido de material de concurso do briefing à entrega.
version: 0.1.0
---

# Conduzir um pedido de material de concurso do briefing à entrega

## Quando usar

Quando o usuário trouxer um concurso, edital, matéria ou pedido de apostila/caderno.

## Entradas

Pedido, contexto disponível e estado do projeto. Consulte AGENTS.md e as políticas em docs/ antes de executar.

## Procedimento

1. Leia AGENTS.md, Progress.md, Decisions.md e o índice de skills. Identifique tipo de material e escopo; procure informações já disponíveis antes de perguntar.
2. Acione ae-analisar-edital para identidade e cobertura, ae-pesquisar-fontes para evidências e ae-analisar-banca quando houver questões por perfil.
3. Produza um plano de capítulo/questões e figuras; use as skills de escrita, ilustração e questões conforme o lote. Priorize uma unidade completa e verificável.
4. Passe o conteúdo por ae-revisar; use ae-diagramar para exportar e testar navegação. Corrija falhas materiais antes da entrega final.
5. Use ae-gerenciar para atualizar estado, evidências e próximos passos; informe lacunas reais e links dos artefatos.

## Saídas

Briefing, plano, material, relatório de validação e estado atualizado.

## Validação

Um pedido pode ser retomado pelos registros; nenhuma fonte, entrega ou automação é inventada.

## Limites

Não inventar evidência, fontes, capacidades ou aprovação humana. Ausência de acesso deve ser registrada com seu efeito na entrega. Esta skill é uma instrução de projeto, não um serviço ou instalação global. Validação pedagógica em concurso real permanece pendente do piloto.

---
name: ae-orquestrar
description: Conduzir um pedido de material de concurso do briefing à entrega.
version: 0.2.0
---

# Conduzir um pedido de material de concurso do briefing à entrega

## Quando usar

Quando o usuário trouxer um concurso, edital, matéria ou pedido de apostila/caderno.

## Entradas

Pedido, contexto disponível e estado do projeto. Consulte AGENTS.md e as políticas em docs/ antes de executar.

## Procedimento

1. Receba texto, foto ou print sem exigir formulário. Leia README, AGENTS, Progress, Decisions, todas as skills, políticas, modelos, contratos e referências; registre a leitura atual no pedido conforme docs/do-pedido-a-entrega.md. Preserve a imagem e confira sua transcrição. Pesquise identidade e escopo antes de perguntar.
2. Acione ae-analisar-edital para identidade e cobertura, ae-pesquisar-fontes para evidências e ae-analisar-banca quando houver questões por perfil.
3. Pedido sem recorte abrange todo o programa do cargo. Mapeie todos os itens e subitens e planeje capítulos, questões e figuras. Produza unidades verificáveis internamente até completar o pedido, sem teto artificial de páginas ou substituição por piloto. Use templates/estado-producao.md para retomada.
4. Passe o conteúdo por ae-revisar. Vincule pedido.json ao manifesto, confira todo o escopo com --check --final e exporte com --pdf --final; audite links e bytes entregues. Corrija falhas antes de encerrar o pedido completo. O mesmo fluxo de pesquisa vale para cadernos.
5. Use ae-gerenciar para atualizar estado, evidências e próximos passos; informe lacunas reais e links dos artefatos.

## Saídas

Briefing, plano, material, relatório de validação e estado atualizado.

## Validação

Um pedido pode ser retomado pelos registros; nenhuma fonte, entrega ou automação é inventada.

## Limites

Não inventar evidência, fontes, capacidades ou aprovação humana. Ausência de acesso deve ser registrada com seu efeito na entrega. Esta skill é uma instrução de projeto, não um serviço ou instalação global. Validação pedagógica em concurso real permanece pendente do piloto.

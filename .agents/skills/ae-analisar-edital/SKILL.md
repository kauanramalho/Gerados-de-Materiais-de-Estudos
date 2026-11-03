---
name: ae-analisar-edital
description: Identificar concurso e converter edital em cobertura rastreável.
version: 0.2.0
---

# Identificar concurso e converter edital em cobertura rastreável

## Quando usar

Ao receber nome, link, edital, retificação ou novo escopo de concurso.

## Entradas

Nome, texto, foto/print ou documento/link; cargo se disponível. Consulte AGENTS.md e docs/do-pedido-a-entrega.md. Não exigir edital ou banca previamente fornecidos pelo usuário.

## Procedimento

1. Localize órgão, cargo, especialidade, ano e banca em fontes oficiais. Havendo homônimos, avance na pesquisa e esclareça só a ambiguidade que afeta a matéria.
2. Obtenha edital e retificações pertinentes; registre URL, versão, data de acesso e hash dos arquivos locais. Confira se uma retificação altera conteúdo ou regras.
3. Extraia todos os itens e subitens aplicáveis ao cargo, mantendo numeração, texto e localizador; confira OCR/transcrição visualmente. Registre programa e seleção em pedido.json. Pedido completo seleciona todo o programa; matéria/recorte seleciona todos os itens pedidos.
4. Preencha a matriz: edital_id → texto literal → objetivo → capítulo → questão. Compare-a com o anexo oficial para detectar omissões. Identifique pré-requisitos necessários e complementos justificados; não acrescente assunto de outro concurso.
5. Registre lacunas e data de corte; não suponha cronograma, banca ou pesos ainda não confirmados.

## Saídas

Briefing e matriz de cobertura com fontes.

## Validação

Identidade e versão verificadas; cada objetivo tem item do edital ou justificativa de complemento.

## Limites

Não inventar evidência, fontes, capacidades ou aprovação humana. Ausência de acesso deve ser registrada com seu efeito na entrega. Esta skill é uma instrução de projeto, não um serviço ou instalação global. Validação pedagógica em concurso real permanece pendente do piloto.

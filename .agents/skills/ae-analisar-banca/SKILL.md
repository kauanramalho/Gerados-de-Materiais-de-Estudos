---
name: ae-analisar-banca
description: Construir um perfil de prova baseado em amostra explícita.
version: 0.1.0
---

# Construir um perfil de prova baseado em amostra explícita

## Quando usar

Quando houver pedido de questões na linha de um concurso/banca.

## Entradas

Concurso identificado, objetivos e provas relacionadas. Consulte AGENTS.md e as políticas em docs/ antes de executar.

## Procedimento

1. Busque provas e gabaritos oficiais da mesma banca, área/cargo e nível; amplie a seleção explicitando o motivo.
2. Registre amostra: provas, anos, cadernos, itens, inclusão/exclusão e quantidade efetivamente lida.
3. Classifique formatos, contextos, objetivos cognitivos, estilo de alternativas e erros explorados; cite itens de apoio por metadados.
4. Calcule frequências somente com denominador da amostra e método. Não declare probabilidade futura ou dificuldade equivalente como fato.
5. Crie matriz de questões autorais com distribuição justificada; registre lacunas e nível editorial estimado.

## Saídas

Perfil de banca e matriz de elaboração.

## Validação

Cada padrão tem evidência; a limitação da amostra é legível e não há estereótipos sem suporte.

## Limites

Não inventar evidência, fontes, capacidades ou aprovação humana. Ausência de acesso deve ser registrada com seu efeito na entrega. Esta skill é uma instrução de projeto, não um serviço ou instalação global. Validação pedagógica em concurso real permanece pendente do piloto.

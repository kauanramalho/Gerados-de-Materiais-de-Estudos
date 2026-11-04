---
name: ae-revisar
description: Revisar precisão, didática, questões e artefatos finais.
version: 0.6.0
---

# Revisar precisão, didática, questões e artefatos finais

## Quando usar

Antes de qualquer entrega marcada revisada.

## Entradas

Material, fontes, edital, perfil de banca e checklist. Consulte AGENTS.md e as políticas em docs/ antes de executar.

## Procedimento

1. Aplique docs/qualidade.md em passagens separadas: técnica, pedagógica/linguística e visual/navegação.
2. Reconfira afirmações mutáveis e resolva exercícios de forma independente. Compare alternativas, respostas e comentários; registre divergências oficiais.
3. Verifique cobertura dos objetivos, progressão, explicação das figuras e utilidade dos exemplos. Elimine excesso sem remover etapas necessárias.
4. Execute as ferramentas estruturais e scripts/audit_links.py com --browser e --external nos arquivos finais. Conferir cada área clicável, destino, página e retorno, incluindo seções na mesma página e links com quebra de linha. Não aceitar somente contagem/presença de âncoras ou aprovação de outro hash. Ver docs/navegacao.md.
5. Registre defeitos e correções. Falha crítica impede rótulo de entrega final; identifique rascunho e lacunas quando necessário.
6. Registre o aceite visual já dado ao layout, preservando-o. Não o transforme em aprovação de precisão, aprendizagem ou dificuldade das questões; essas dimensões exigem suas próprias evidências.

7. Conferir ordem/matriz e pontuação/anulação de simulados, síntese/remissões de revisão e impacto/errata de edições. Executar acessibilidade.py e registrar limites assistivos.
8. Comparar pedido, imagem/transcrição, programa oficial completo, seleção, capítulos e cada questão. Não aceitar unidade parcial como conclusão de pedido completo. Executar --check --final e revisar fidelidade da extração, evidências e pertinência; o validador estrutural não comprova leitura real das fontes.
9. Na segunda passagem, conferir hipóteses de transação/versão, grão e unidades, pertinência das remissões e plausibilidade de cada distrator. Distratores absurdos e respostas denunciadas pelo formato não calibram o nível da banca. Registrar o que foi corrigido e separar revisão editorial por IA de avaliação com leitor; usar docs/avaliacao-pedagogica.md.
10. Exigir sumário inteiro clicável no PDF de todos os formatos, incluindo número, título, pontilhado/espaços e página. Conferir destino direto /XYZ, página real e posição da seção; testar que a página indicada e o intervalo pontilhado pertencem à área ativa. Qualquer entrada incorreta bloqueia a entrega. Registrar separadamente checagem PDF, cliques HTML e visualizador PDF independente, sem reaproveitar resultados de outro hash.

## Saídas

Checklist, defeitos, correções e parecer de entrega.

## Validação

Não restam falhas críticas ocultas e a evidência descreve exatamente o que foi validado.

## Limites

Não inventar evidência, fontes, capacidades ou aprovação humana. Ausência de acesso deve ser registrada com seu efeito na entrega. Esta skill é uma instrução de projeto, não um serviço ou instalação global. Validação pedagógica em concurso real permanece pendente do piloto.

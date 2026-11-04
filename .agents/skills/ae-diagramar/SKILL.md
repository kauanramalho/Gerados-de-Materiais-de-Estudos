---
name: ae-diagramar
description: Montar apostilas e cadernos navegáveis em HTML e PDF.
version: 0.7.0
---

# Montar apostilas e cadernos navegáveis em HTML e PDF

## Quando usar

Após revisão de conteúdo ou para testar uma proposta visual.

## Entradas

Capítulos, questões, figuras, metadados e padrões visuais. Consulte AGENTS.md e as políticas em docs/ antes de executar.

## Procedimento

1. Organize capa, orientações, sumário, capítulos/questões, resoluções, glossário e referências conforme o tipo de material.
2. Atribua IDs persistentes, gere sumário clicável e todos os links questão → resolução → questão; inclua remissões à teoria.
3. Aplique hierarquia, margens, tipografia e quebras; evite separar dados essenciais, figuras e legendas. Em simulados, mantenha respostas separadas.
4. Prepare o manifesto e execute scripts/build_material.py com --check; depois exporte com --pdf. Use --kind caderno para o caderno com dados suficientes aos exercícios. Consulte docs/producao.md. A amostra examples/redes permanece como demonstração inicial.
5. Confira o manifesto *-navigation.json: todos os links visíveis precisam de área clicável e destino esperado no PDF, incluindo título/página do sumário e pares questão/resolução. A CLI deve bloquear falha interna. Execute scripts/audit_links.py nos PDFs finais com --browser e --external; siga docs/navegacao.md e registre limitações externas.
6. Preserve o layout aprovado. Compare paginação e posições do texto quando a mudança for só técnica. Inspecione o PDF, corrija falhas e arquive relatórios com hashes da mesma exportação. Não reaproveite aprovação de um arquivo alterado.

7. Usar --kind simulado ou revisao com os planos próprios para esses formatos. Executar acessibilidade.py nos artefatos finais e conferir tags PDF e nomes acessíveis de SVGs; registrar limites, sem presumir certificação PDF/UA.
8. Em entrega final de concurso, exigir pedido.json vinculado e usar --check --final e --pdf --final; acrescentar --kind do formato quando pertinente. Não impor limite artificial de páginas nem reduzir fonte para encurtar. Pilotos sem --final são referências e não demonstram cobertura do pedido completo.
9. A pré-validação requer Pandoc e lê as imagens com o mesmo parser da exportação: capítulos, revisão, contexto, perfil e questões. Declarar todas em figuras.json, mesmo quando usadas apenas no caderno ou revisão. Usar arquivos dentro da pasta e SVGs independentes; não contornar a validação por sintaxe de referência ou recursos aninhados. Se o inventário mudar, recarregar o manifesto antes de publicar.
10. Sumário 100% clicável é obrigatório nos quatro formatos: número, título, pontilhado/espaços e página, em toda entrada. O exportador normaliza destinos diretos PDF /XYZ e confere componentes e área contínua da linha. Conferir o manifesto versão 2 do mesmo hash, preservar edição anterior e recusar qualquer falha; não tratar esse requisito como opção. Quando o motor mudar, testar também um visualizador PDF independente e registrar a versão e os cliques realmente realizados, distinguindo-os dos cliques HTML.

## Saídas

HTML, PDF, manifesto e validação de navegação.

## Validação

Todos os links internos obrigatórios funcionam no arquivo final; páginas e figuras foram inspecionadas.

## Limites

Não inventar evidência, fontes, capacidades ou aprovação humana. Ausência de acesso deve ser registrada com seu efeito na entrega. Esta skill é uma instrução de projeto, não um serviço ou instalação global. Validação pedagógica em concurso real permanece pendente do piloto.

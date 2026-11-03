# Validação da fundação — 03/11/2026

## Evidência local

- `python scripts/check.py`: estrutura, contratos das 12 skills, existência dos destinos de links Markdown, integridade das duas questões e navegação interna do HTML aprovadas.
- `python -m unittest discover -s tests -v`: 9 testes aprovados, incluindo rejeição de IDs duplicados, resposta fora das alternativas, comentário ausente e atribuição real sem proveniência.
- Contratos JSON conferidos com jsonschema; as duas questões da amostra passaram no schema. O verificador padrão não pretende executar todos os recursos do JSON Schema.
- `python scripts/build_sample.py --pdf`: HTML autocontido e PDF A4 gerados com Pandoc, Playwright e Chromium. O publicador é restrito à amostra autoral.
- PDF de 5 páginas: 18 links internos com destinos nomeados resolvidos e páginas válidas; 2 links externos. Os pares das duas questões levam às resoluções na página 4 e retornam à página 3.
- Cinco páginas renderizadas e inspecionadas: sumário, texto, esquema rotulado, prática, comentários e referências sem cortes observados. Não foi realizada auditoria PDF/UA ou aplicação pedagógica com aluno.

## Limites e integrações

Revisão de apresentação solicitada em 03/11/2026: sumário redesenhado com numeração hierárquica, recuos, linhas pontilhadas e páginas alinhadas. As 12 referências de página foram obtidas dos destinos nomeados do PDF e conferidas após a segunda passagem. A exportação agora usa PyMuPDF para essa conferência e mostra rodapés numerados; preserva 5 páginas, 18 links internos e os dois pares questão/resolução.

A pesquisa editorial consultou as páginas do catálogo; não realizou comparação completa de capítulos em PDF. O material de switch é uma demonstração curta, sem edital, banca ou questões reais. Os procedimentos aguardam piloto em concurso identificado.

GitHub: conta conferida, mas criação recusada pela integração com erro 403. Não há push, issues ou CI remota confirmados. O workflow está preparado; somente verificações locais foram executadas.

Drive: o resultado de arquivamento e as URLs são registrados no relatório privado da tarefa após leitura de confirmação. Acesso a ferramentas não implica sincronização automática com Obsidian.

## Ajuste do publicador

Navegação `file://` foi bloqueada pela política do navegador do ambiente. A exportação validada usa Playwright para renderizar o HTML autocontido, sem requisições externas, e imprimir com Chromium. Não exige servidor permanente.

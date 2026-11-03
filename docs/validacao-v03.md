# Validação da entrega 0.3 — 03/11/2026

## Resultado observado

- 50 testes aprovados: integridade anterior, contratos malformados, catálogo, seis cálculos de matemática e integração Pandoc/MathML.
- JSON Schemas de material, questão, fontes, figuras e cobertura aplicados antes da composição. Schema de briefing também disponível e estruturalmente conferido.
- Acervo inicial: 17 questões, sendo 14 autorais e três reais por link, em dois materiais. Reimportação do SQL reutilizou 11 itens sem duplicação. Filtros combinados, histórico e rollback de importação foram testados.
- Exportação JSON preserva materiais, ocorrências e revisões. O banco completo é o artefato para recuperação; não existe importador reverso genérico de JSON.

| Material / formato | Páginas | Links internos | Entradas de sumário | Pares questão/resolução |
|---|---:|---:|---:|---:|
| SQL / apostila | 24 | 94 | 47 | 11 |
| SQL / caderno | 15 | 52 | 30 | 11 |
| Matemática / apostila | 16 | 41 | 23 | 6 |
| Matemática / caderno | 9 | 30 | 18 | 6 |

Os quatro builds passaram pela auditoria de navegação/paginação; texto longo com mediana de 11,5 pt. No novo piloto, 25 páginas foram rasterizadas e inspecionadas em folhas de contato, com ampliação de fórmulas, diagramas, continuação da tabela e glossário. O SQL foi reconstruído e teve inspeção pontual de regressão; a inspeção integral inicial está registrada em validacao-piloto.md.

## Ambiente reproduzido

A suíte de 50 testes e os quatro builds passaram em venv novo, sem pacotes herdados, no mesmo host Linux/Python 3.12. Dependências resolvidas: jsonschema 4.26.0, Playwright 1.64.1 e PyMuPDF 1.28.2. Pandoc 3.1.11.1 e Chromium 154.0.8037.57 vieram do host. O código usa o namespace pymupdf e aceita também Chromium instalado pelo Playwright.

Isso demonstra isolamento de dependências Python, sem afirmar reprodução em outro sistema operacional. O workflow foi ampliado para testes, quatro PDFs e catálogo com artifacts; sua execução remota depende da publicação GitHub e não foi confirmada.

## Evidências e limites

Os relatórios de build registram hashes de entradas, saídas, schemas e código, além das versões de ferramentas e resultados de paginação. Os testes de mudanças de gabarito usam fixtures sintéticas isoladas. Os três itens reais conservam o gabarito preliminar registrado no piloto, sem retificação oficial presumida.

A busca local usa metadados/texto normalizados; não é busca semântica ou rastreador de provas. O novo material é autoral, sem vínculo a concurso. Não há aplicação com aluno, dificuldade calibrada ou conformidade PDF/UA certificada.

AE-010, AE-011 e AE-019 foram concluídos no escopo descrito. Novos casos editoriais, acessibilidade completa, retomada independente e execução remota continuam separados no backlog. A próxima implementação é o formato de simulado, sem bloquear o retorno pedagógico do leitor.

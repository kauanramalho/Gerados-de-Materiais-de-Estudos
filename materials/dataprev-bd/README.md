# Banco de Dados — Dataprev/FGV 2026

Matéria desenvolvida para o caso real de validação escolhido pelo titular. Abrange os **17 itens de Banco de Dados** do Anexo I, Perfil 3 — Desenvolvimento de Software, edital 001/2026 retificado em 29/07/2026, páginas 30–31. Não abrange as demais disciplinas do concurso.

São 17 capítulos, 12 figuras originais e 49 questões comentadas: 42 autorais e sete reais por link para a prova oficial. As referências oficiais mantêm o gabarito preliminar de 2026 explicitamente identificado. As instruções, contratos, figuras e textos são fontes de produção, sem teto artificial de páginas.

O manifesto público não contém pedido ou imagem pessoal. A execução final vinculada à pesquisa e aos pedidos de validação por texto e print é feita em área privada de trabalho, com relatórios de hashes, cobertura, revisão e navegação. O print de teste é uma renderização do edital oficial, não uma fotografia recebida do usuário. As versões públicas abaixo são builds de referência da mesma fonte editorial:

```sh
python scripts/build_material.py materials/dataprev-bd/material.json --check
python scripts/check_sql.py materials/dataprev-bd/verificacoes.json --report build/dataprev-bd/sql-validation.json
python scripts/build_material.py materials/dataprev-bd/material.json --pdf
python scripts/build_material.py materials/dataprev-bd/material.json --kind caderno --pdf
```

Os exemplos de SQL têm massa independente em `massa.sql`, com resultados esperados declarados em `verificacoes.json`. O motor local é SQLite com chaves estrangeiras habilitadas; diferenças do PostgreSQL foram identificadas no texto. O perfil de banca registra a amostra de dez itens de 2024/2026, o método e as limitações.

Fonte oficial: [portal Dataprev/FGV 2026](https://conhecimento.fgv.br/concursos/dataprev26). Os exemplos, diagramas, enunciados autorais e comentários foram elaborados com assistência de IA e passam por revisão técnica separada. A aprovação visual anterior do layout não é apresentada como avaliação de aprendizagem deste conteúdo novo.

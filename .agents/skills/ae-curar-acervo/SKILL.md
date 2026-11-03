---
name: ae-curar-acervo
description: Importar, buscar, deduplicar e versionar questões com proveniência e histórico.
version: 0.1.0
---

# Curar o acervo local de provas e questões

## Quando usar

Ao reutilizar questões, preparar um lote ou registrar mudança de gabarito/evidência. É um procedimento local do projeto; não instala serviço nem executa pesquisa externa por conta própria.

## Entradas

Manifesto e arquivos de um material, fontes conferidas, versão da edição e banco SQLite local em build/ ou work/. Leia AGENTS.md, docs/acervo.md e a política de questões. A nova execução precisa recuperar o banco arquivado ou reconstruir a base dos manifestos; não presumir persistência do ambiente cloud.

## Procedimento

1. Confira a evidência oficial com ae-questoes-reais e ae-pesquisar-fontes. A CLI valida metadados e hashes declarados, mas não comprova sozinha autenticidade nem autorização de reprodução.
2. Valide o manifesto com scripts/build_material.py --check. Importe com scripts/acervo.py --db build/acervo.sqlite importar <manifesto>. Uma edição já registrada não pode receber entradas diferentes; incremente a versão quando houver mudança.
3. Busque por --banca, --ano, --assunto, --origem e --status. Abra a prova/gabarito antes de reutilizar um item real. Atribuição de banca só vale para a fonte original; autorais não herdam a banca de referência.
4. Confira duplicatas e conflitos. Identidade real usa banca/órgão/cargo/ano/caderno/número normalizados; autorais usam texto e alternativas preservando operadores. Semelhanças aproximadas, cadernos equivalentes e variações de cadastro exigem análise editorial.
5. Para revisão confirmada, use --aceitar-revisoes e --motivo com o novo manifesto. Preserve o histórico; não rebaixe definitivo para preliminar nem substitua resposta oficial sem nova evidência. Consulte historico <id-estável>.
6. Exporte JSON e arquive o banco, o pacote fonte e o relatório no destino autorizado. Itens somente-link não armazenam texto/alternativas originais no catálogo. Releia o resultado e atualize Progress e o Segundo Cérebro, sem dados privados no Git público.

## Saídas

Catálogo consultável, relatório de importação, histórico de revisões e exportação JSON com ocorrências por material/edição.

## Validação

Reimportação idempotente; filtros combinados; nenhuma atribuição autoral falsa; duplicatas reconhecidas nos critérios documentados; revisão explícita com estado anterior preservado; falha de lote sem gravação parcial; exportação sem texto proibido. O lote inicial contém 17 questões e foi aplicado a SQL e matemática.

## Limites

Busca local, sem crawler, OCR automático ou medição psicométrica. Casos de revisão oficial nos testes são sintéticos e não alteram o gabarito real da banca. Não presumir que similaridade textual prove cópia ou equivalência de questões. Não declarar validação pedagógica ou instalação global.

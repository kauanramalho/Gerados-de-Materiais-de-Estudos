# Edições, mudanças de fonte e erratas

Preservar a edição anterior, seus PDFs, inputs e hashes antes de corrigir. Mudar versão quando houver alteração de conteúdo; manter os IDs de questões que continuam sendo os mesmos. Remover um ID exige justificativa. Não sobrescrever um gabarito oficial com uma análise própria nem apresentar teste sintético como retificação de banca.

```sh
python scripts/edicoes.py work/anterior/material.json work/nova/material.json --motivo 'Correção fundamentada na fonte' --report work/impacto.json --errata work/errata.md
```

A comparação é somente leitura das edições. Identifica arquivos, fontes, questões adicionadas/removidas/alteradas e capítulos a revisar. Mudança de fonte sinaliza todos os capítulos: o projeto não tem índice confiável de dependência por frase e não deve presumir que um capítulo ficou imune. Mudança de resposta/comentário também sinaliza os objetivos e capítulos correspondentes.

O Markdown gerado é um início de errata, não parecer de aprovação. Completar com trecho anterior, correção, fundamento, data, revisão técnica e links da nova edição. Recalcular questões, reconstruir PDFs e auditar novamente links e acessibilidade. Os relatórios anteriores pertencem aos hashes anteriores. Reimportar o catálogo como nova edição e preservar suas revisões; uma mudança no banco não recompõe PDFs entregues.

Os testes que mudam gabarito são sintéticos. O exemplo editorial de fechamento modifica uma explicação autoral mantendo a resposta correta, para demonstrar impacto e rastreabilidade sem simular mudança oficial.

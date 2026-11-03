# Progresso — Ateliê de Estudos

- **Estado:** active — piloto técnico produzido e publicador 0.2 em validação.
- **Prioridade no portfólio:** unassigned.
- **Data do estado:** 2026-11-03.
- **Próxima ação:** avaliar clareza, densidade, figuras e comentários do piloto com o leitor e incorporar o resultado ao próximo lote.
- **Responsável:** agente para revisão e ajustes; titular para relatar sua experiência de leitura.
- **Condição de conclusão:** observações convertidas em correções verificadas e limites pedagógicos registrados.
- **Pendência independente:** publicação pública autorizada e reiterada pelo titular; nesta retomada, a conta foi confirmada, o destino retornou 404 e as tentativas de criação por GraphQL/REST retornaram 403. Falta acesso técnico da integração, não nova autorização textual. Isso não impede desenvolver e entregar no Drive.

## Estado e evidências

O piloto usa um recorte público do edital Dataprev/FGV 2026, Desenvolvimento de Software, sem mudar prioridade pessoal. Entregas: apostila de 24 páginas, caderno de 15, três esquemas, oito questões autorais e três reais por link com comentário. As respostas oficiais de 2026 estão identificadas como preliminares.

A CLI aceita manifesto, valida referências, gera os dois formatos e registra hashes. Dezoito testes de integridade e treze casos SQL passaram. Foram conferidos 94 links internos na apostila, 52 no caderno e 11 pares questão/resolução por arquivo. As páginas foram inspecionadas; a mediana do texto longo é 11,5 pt. Ver [Validação do piloto](docs/validacao-piloto.md) e [Produção](docs/producao.md).

## Marcos e limites

M0 concluído; M0.1 mantém publicação GitHub pendente. M1 teve execução técnica entregue e aguarda aceite pedagógico. M2 tem implementação inicial aplicada ao piloto, ainda sem validação em outras matérias. Não há geração sem agente, scheduler, instalação global ou CI remota validada.

## Diagnóstico de prontidão

O [inventário de pendências](docs/prontidao.md) distingue uso acompanhado, V1 recorrente e coleção por edital. Registra cinco skills candidatas, aprofundamentos nas 12 existentes, documentos e materiais de validação ainda necessários. Foram criados modelos de avaliação do leitor e checklist de revisão. Backlog reconciliado: avaliação do titular, acervo consultável e auditoria de acessibilidade não estavam concluídos ou em execução com evidência suficiente. Os estados foram corrigidos sem revogar os resultados técnicos do piloto.

## Riscos

Gabaritos preliminares podem mudar; revalidar na banca. As questões autorais não têm dificuldade calibrada. O recorte não cobre todo o edital. Relatórios automáticos não substituem revisão de fontes, conteúdo e experiência do leitor.

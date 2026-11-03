# Contrato de navegação — obrigatório em cada entrega

O sumário deve ser clicável no PDF: clicar no número, título ou página leva à seção correspondente. Toda questão leva à sua própria resolução, que retorna à mesma questão. Remissões teóricas da apostila e referências internas precisam levar aos seus destinos. O requisito vale para qualquer concurso/matéria nos formatos já suportados: apostila e caderno. O layout atual foi aprovado pelo titular e permanece como padrão.

## Verificação automática na exportação

1. O publicador gera IDs estáveis para as rotas obrigatórias e confere HTML contra o pareamento esperado, definido pelos metadados das questões e pelas entradas do sumário.
2. Todos os links internos visíveis recebem identificação de origem. Referências técnicas invisíveis usadas pelo Pandoc para linhas de código não são tratadas como botões do leitor.
3. A auditoria abre o PDF final, encontra cada área clicável, confere página e posição do destino e verifica o título/texto esperado. Uma página existente não basta: duas resoluções na mesma página têm posições distintas.
4. Links que se dividem em linhas têm seus fragmentos conferidos. Destinos com acentos são decodificados corretamente. Nenhuma anotação interna pode ficar sem correspondência.
5. Sumário impresso e destinos são conferidos após a paginação estabilizar. Alteração de layout pode mudar páginas; números não são digitados manualmente.
6. Falha interna interrompe o build. Relatórios antigos de sucesso são removidos antes de reconstruir. O novo relatório de navegação registra hashes de PDF/HTML, rotas, áreas e resultados.

Os metadados de auditoria não acrescentam conteúdo visível nem redesenham a apostila. A inspeção visual e a revisão de conteúdo continuam necessárias: uma referência escrita pelo autor pode apontar a uma seção existente e ainda precisar de avaliação de pertinência.

## Reauditar antes de entregar

Guardar o PDF, HTML e *-navigation.json juntos. O manifesto está vinculado aos bytes da exportação. Exemplos:

```sh
python scripts/build_material.py materials/dataprev-sql/material.json --pdf
python scripts/build_material.py materials/dataprev-sql/material.json --kind caderno --pdf
python scripts/audit_links.py build/dataprev-sql/apostila.pdf build/dataprev-sql/caderno.pdf --browser --external --report build/auditoria-links.json
```

O comando retorna erro se o hash divergir, se uma rota interna falhar ou se a verificação externa solicitada não for confirmada. `--browser` executa cliques nativos no HTML autocontido, incluindo número/título/página do sumário e os fragmentos de links quebrados em linhas. O navegador não usa JavaScript do conteúdo nem acessa recursos remotos para esses cliques. Ajustes de animação existem somente no teste.

`--external` consulta referências HTTPS, elimina duplicatas por fragmento e registra data/status. Uma URL de PDF precisa responder com arquivo PDF; páginas de erro/login não bastam. Bloqueio, timeout e erro HTTP não são aprovados silenciosamente. A disponibilidade é uma observação da entrega: sites de terceiros podem mudar depois. Sem acesso à rede, registrar a revisão externa pendente e seus efeitos; não declarar que foi verificada.

Para PDF renomeado, usar `--manifest caminho/arquivo-navigation.json` em uma chamada com um PDF. O HTML associado precisa estar na pasta do manifesto. Esses arquivos auxiliares são necessários para reauditoria, não para o leitor clicar no PDF.

## Publicação e novos formatos

- Entregar somente o PDF cujo hash foi aprovado; reler bytes ou metadados após o upload e manter a associação dos relatórios.
- Arquivar versões anteriores antes de substituir arquivos de entrega. Edição posterior do PDF invalida a auditoria anterior e exige nova conferência.
- Novo formato, motor de impressão ou mudança nas rotas exige atualizar contrato e testes antes de ser habilitado. Links entre PDFs separados ainda exigem implementação/testes próprios; não presumir suporte a partir do caderno atual.
- A CI prepara regressões e auditoria dos quatro PDFs; sua execução remota depende de acesso GitHub. Falha interna não deve ser ignorada para publicar.

## Regressões que devem continuar passando

Troca de questão/resolução, retorno incorreto, destino errado na mesma página, deslocamento vertical, botão ausente, área invisível, sumário com página desatualizada, título diferente no destino, ID duplicado, relatório de outro hash e aprovação antiga falsamente reutilizada. Incluir também links em duas linhas e IDs em português com acentos.

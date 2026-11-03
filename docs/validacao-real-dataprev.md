# Caso real — Banco de Dados do Dataprev/FGV

## Escolha e abrangência

O titular escolheu Banco de Dados do Dataprev/FGV para validar o método. Foi mantido o Perfil 3 — Desenvolvimento de Software da referência já existente, edital 001/2026 retificado em 29/07/2026. A matéria inteira possui 17 itens nas páginas 30–31. A seleção é uma matéria expressamente delimitada, não todo o programa do cargo nem uma escolha pessoal inferida de concurso.

Fontes editoriais em [materials/dataprev-bd](../materials/dataprev-bd/README.md): 17 capítulos, 12 diagramas e 49 questões, sendo 42 autorais e sete reais por link. Os 22 casos em verificacoes.json conferem consultas, NULL, agregações, alterações, chaves e rollback em massa própria. As diferenças de motor e o gabarito preliminar de 2026 estão identificados.

## Entradas e pesquisa efetiva

O pedido textual preserva a escolha do titular. A rota de print usa uma renderização real da página 30 do edital oficial, produzida pelo agente para o teste; não é uma foto recebida do usuário. A imagem foi inspecionada e sua transcrição termina onde a página termina. O restante do item 12 e os itens 13–17 são recuperados na página 31, sem atribuí-los à parte visível do print.

Foram abertos portal oficial, edital consolidado, primeira retificação, prova e gabarito de 2026, prova e gabarito definitivo de 2024 e fontes acadêmicas/técnicas. A primeira retificação não muda Banco de Dados do Perfil 3. A amostra de prova tem dez itens intencionais: 46–52 de 2026 e 65–67 de 2024. Não é uma amostra aleatória nem uma previsão de frequência. A data de corte é 03/11/2026.

Os sete itens de 2026 foram conferidos visualmente na prova e no gabarito preliminar, página 13: A, E, D, A, D, D, C. Enunciados e alternativas originais ficam na prova por link; comentários próprios foram desenvolvidos para cada alternativa. Fontes indisponíveis ou mudanças posteriores devem ser novamente tratadas, sem inventar atribuição ou resposta.

## Protocolo de aceite

1. Preservar entradas e anexos em área privada; criar pedidos por texto e print usando scripts/pedido.py.
2. Ler instruções, skills, modelos, contratos e referências; registrar seus hashes, a pesquisa efetiva e a seleção BD-01 a BD-17.
3. Conferir programa literal contra as duas páginas do edital; vincular cada capítulo e questão ao objetivo correspondente.
4. Revisar tecnicamente texto, figuras e cada alternativa; executar a massa de 22 casos. Manter um rascunho anterior ao aperfeiçoamento editorial e registrar impacto/errata com IDs e respostas oficiais preservados.
5. Vincular cada pedido ao manifesto privado e executar --check --final e --pdf --final para apostila e caderno.
6. Auditar os PDFs finais e seus hashes, sumário, questão/resolução/retorno, fontes externas, cliques nativos e acessibilidade com os limites declarados. Reler os bytes depois do upload.
7. Arquivar fontes de produção, anexos, relatórios, catálogo e evidências; registrar no Segundo Cérebro a aplicação das 17 skills e o que depende do leitor.

O manifesto público não contém o pedido privado. A CI recompõe os mesmos textos como referência; os relatórios da execução vinculada aos pedidos ficam no pacote de evidências. Isso distingue uma exportação reproduzível do registro de visão/pesquisa realmente realizado pelo agente.

## Limites e retorno

A revisão editorial por IA é separada da [avaliação com leitor](avaliacao-pedagogica.md). Não se presume aprovação pedagógica do titular, dificuldade equivalente estatisticamente à banca, certificação PDF/UA ou leitura com tecnologia assistiva real. Fotografias com enquadramento e ruído diferentes exigem nova conferência; o caso atual exercita texto e print legível de edital.

Resultados finais e hashes são registrados em Progress.md, no relatório da execução e nas issues AE-021/023/028. As instruções guardam o método; os relatórios datados identificam os artefatos efetivamente aprovados.

## Resultado da execução 0.6

Foram produzidos com --final a apostila de **99 páginas** e o caderno de **62 páginas**. A revisão de paginação eliminou uma página que continha somente a nota de fontes do capítulo de transações. Os dois PDFs passaram nas auditorias de navegação e acessibilidade; foram conferidos 576 e 419 cliques nativos, respectivamente. No conjunto de dez PDFs recompostos, passaram 1.720 cliques, 442 entradas de sumário e a consulta de 38 endereços externos. São 264 páginas no conjunto, sem teto de extensão aplicado.

As 22 verificações SQL passaram. A suíte completa passou em 138 testes. Os oito PDFs de referência mantiveram contagem de páginas e geometria de texto; 101 de suas 103 páginas ficaram visualmente idênticas, com duas páginas de SQL alteradas somente na cor de destaque para melhorar contraste. O CSS aprovado permaneceu idêntico.

Os PDFs vinculados a pedidos e o pacote de evidências ficam nos artefatos privados do Drive. As sete questões reais oferecem acesso ao enunciado completo no PDF oficial; o caderno não reproduz integralmente a prova de terceiros. O leitor recebe comentários próprios para cada alternativa. O retorno de aprendizagem permanece em AE-009; ele não é substituído pelos checks ou pela revisão por IA.

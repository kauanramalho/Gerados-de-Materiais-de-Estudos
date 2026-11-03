# Progresso — Ateliê de Estudos

- **Estado:** active — publicador 0.3, acervo local e segundo piloto entregues tecnicamente.
- **Prioridade no portfólio:** unassigned.
- **Data do estado:** 2026-11-03.
- **Próxima ação:** implementar o formato de simulado com respostas separadas e pontuação verificável, mantendo a avaliação do leitor em paralelo.
- **Responsável:** agente para desenvolvimento/revisão; titular para relatar sua experiência de leitura quando disponível.
- **Condição de conclusão:** exemplar navegável, matriz e regras de pontuação explícitas, testes de resposta/anulação e relatório registrado.
- **Pendência independente:** publicação pública autorizada; a última consulta do destino retornou 404 e as tentativas de criação GraphQL/REST retornaram 403. O acesso técnico continua sem confirmação; não houve push ou CI remota.

## Estado e evidências

A entrega 0.3 concluiu o núcleo do publicador genérico, a validação consistente dos contratos de entrada e o acervo consultável. AE-010, AE-011 e AE-019 têm evidência para encerramento nesse escopo. Há 13 skills locais, incluindo ae-curar-acervo aplicada à ferramenta.

O acervo contém 17 itens: 14 autorais e três reais por link, com filtros, deduplicação, importação idempotente, revisões explícitas e exportação com histórico. Uma revisão de gabarito no catálogo não altera um PDF já entregue. Testes de retificação são sintéticos; não indicam que a banca mudou o gabarito real.

Passaram 50 testes, incluindo seis cálculos do novo piloto e exportação MathML. A suíte e quatro builds foram reproduzidos em um ambiente Python isolado, no mesmo host; isso não equivale a CI remota ou novo sistema operacional. Ver [validação 0.3](docs/validacao-v03.md) e [acervo](docs/acervo.md).

## Materiais

- **SQL:** apostila de 24 páginas e caderno de 15, três esquemas, oito questões autorais e três reais por link. Referência metodológica Dataprev/FGV, sem alterar prioridade pessoal. Gabarito oficial consultado continua identificado como preliminar. Regressão 0.3 preservou 94/52 links internos e 11 pares questão/resolução por arquivo.
- **Matemática:** apostila de 16 páginas e caderno de 9, dois diagramas e seis questões autorais, sem atribuição de edital/banca. Sete fórmulas em MathML na apostila, tabela com continuação e seis cálculos conferidos. Navegação: 41/30 links internos, 23/18 entradas de sumário e seis pares por arquivo. Texto longo: mediana de 11,5 pt.

## Marcos e limites

M0 concluído; M0.1 mantém publicação GitHub pendente. M1 aguarda aceite pedagógico. M2 e M3 têm núcleos locais entregues, com expansão definida no backlog. AE-015/016 avançaram com duas seções HTML de referência e matemática; comparação de capítulos PDF, texto normativo e equipamentos detalhados ainda faltam. AE-022 tem reprodução Python isolada, com retomada e CI pendentes. Simulado, revisão curta, manutenção/erratas, coleção completa e auditoria integral de acessibilidade ainda precisam ser desenvolvidos.

O [inventário de prontidão](docs/prontidao.md) mantém as pendências atuais. Não há serviço sem agente, scheduler, instalação global de skills ou sincronização automática com Drive.

## Riscos

Gabaritos preliminares podem mudar; conferir a fonte antes de reutilizar. Dificuldade autoral é estimada. O catálogo não deduplica semanticamente nem pesquisa a web. Perder o banco completo pode perder revisões que não estejam nos manifestos recuperados; arquivar banco e exportação. Verificações automáticas e inspeção visual não substituem revisão de fontes, pedagogia e acessibilidade.

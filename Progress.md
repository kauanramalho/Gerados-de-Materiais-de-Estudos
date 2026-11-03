# Progresso — Ateliê de Estudos

- **Estado:** active — publicador 0.4, entrada por texto/foto/print e contrato de entrega focada no pedido, com layout e navegação preservados.
- **Prioridade no portfólio:** unassigned.
- **Data do estado:** 2026-11-03.
- **Próxima ação:** implementar o formato de simulado com respostas separadas e pontuação verificável, mantendo a avaliação do leitor em paralelo.
- **Responsável:** agente para desenvolvimento/revisão; titular para relatar sua experiência de leitura quando disponível.
- **Condição de conclusão:** exemplar navegável, matriz e regras de pontuação explícitas, testes de resposta/anulação e relatório registrado.
- **Pendência independente:** publicação pública autorizada; a última consulta do destino retornou 404 e as tentativas de criação GraphQL/REST retornaram 403. O acesso técnico continua sem confirmação; não houve push ou CI remota.

## Estado e evidências

A entrega 0.3 concluiu o núcleo do publicador genérico, a validação consistente dos contratos de entrada e o acervo consultável. AE-010, AE-011 e AE-019 têm evidência para encerramento nesse escopo. Há 13 skills locais, incluindo ae-curar-acervo aplicada à ferramenta.

O acervo contém 17 itens: 14 autorais e três reais por link, com filtros, deduplicação, importação idempotente, revisões explícitas e exportação com histórico. Uma revisão de gabarito no catálogo não altera um PDF já entregue. Testes de retificação são sintéticos; não indicam que a banca mudou o gabarito real.

Passaram 76 testes, incluindo regressões de destinos incorretos, botões ausentes, links em duas linhas, acentos e relatórios de outro hash. Os quatro PDFs têm 118 entradas de sumário e 217 áreas internas de clique conferidas, incluindo os 34 pares questão/resolução. Cada exportação confere destinos exatos no PDF e bloqueia falhas internas; a entrega exige reauditoria e cliques no HTML. Ver [contrato de navegação](docs/navegacao.md). Referências externas são verificadas com data; disponibilidade futura depende dos sites de origem.

O titular aprovou o layout em 03/11/2026. CSS, tipografia e apresentação do sumário foram preservados; a comparação das 64 páginas verifica pixels e posições do texto. Esse retorno encerra a preferência visual atual, mas não presume avaliação de clareza, aprendizagem ou dificuldade das questões. A suíte e quatro builds foram reproduzidos no ambiente Python isolado do mesmo host; isso não equivale a CI remota ou novo sistema operacional. Ver também [validação histórica 0.3](docs/validacao-v03.md) e [acervo](docs/acervo.md).

## Pedido simples e cobertura — 0.4

O fluxo aceita texto, foto ou print, com pesquisa pelo agente e leitura de todas as instruções/skills. Sem recorte, cobre todo o programa aplicável ao cargo, sem teto artificial de páginas. A ingestão preserva imagem/hash; --final exige pedido, pesquisa documentada, leitura atual e cobertura integral da seleção, detectando omissões e questões fora do escopo. Ver [contrato](docs/do-pedido-a-entrega.md).

Passaram 20 testes novos de ingestão/cobertura e 96 na suíte completa, incluindo pré-validação final positiva pela CLI, com metadados sintéticos claramente identificados. Eles não comprovam OCR ou pesquisa real de um novo concurso. O agente continua responsável por visão, consulta às fontes oficiais, extração fiel do edital e revisão pedagógica; ainda falta validar o fluxo completo numa nova solicitação real. Os dois pilotos permanecem recortes de referência.

## Materiais

- **SQL:** apostila de 24 páginas e caderno de 15, três esquemas, oito questões autorais e três reais por link. Referência metodológica Dataprev/FGV, sem alterar prioridade pessoal. Gabarito oficial consultado continua identificado como preliminar. Regressão 0.3 preservou 94/52 links internos e 11 pares questão/resolução por arquivo.
- **Matemática:** apostila de 16 páginas e caderno de 9, dois diagramas e seis questões autorais, sem atribuição de edital/banca. Sete fórmulas em MathML na apostila, tabela com continuação e seis cálculos conferidos. Navegação: 41/30 links internos, 23/18 entradas de sumário e seis pares por arquivo. Texto longo: mediana de 11,5 pt.

## Marcos e limites

M0 concluído; M0.1 mantém publicação GitHub pendente. M1 aguarda aceite pedagógico. M2 e M3 têm núcleos locais entregues, com expansão definida no backlog. AE-015/016 avançaram com duas seções HTML de referência e matemática; comparação de capítulos PDF, texto normativo e equipamentos detalhados ainda faltam. AE-022 tem reprodução Python isolada, com retomada e CI pendentes. Simulado, revisão curta, manutenção/erratas, coleção completa e auditoria integral de acessibilidade ainda precisam ser desenvolvidos.

O [inventário de prontidão](docs/prontidao.md) mantém as pendências atuais. Não há serviço sem agente, scheduler, instalação global de skills ou sincronização automática com Drive.

## Riscos

Gabaritos preliminares podem mudar; conferir a fonte antes de reutilizar. Dificuldade autoral é estimada. O catálogo não deduplica semanticamente nem pesquisa a web. Perder o banco completo pode perder revisões que não estejam nos manifestos recuperados; arquivar banco e exportação. Verificações automáticas e inspeção visual não substituem revisão de fontes, pedagogia e acessibilidade.

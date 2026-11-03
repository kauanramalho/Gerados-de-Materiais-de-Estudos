# Progresso — Ateliê de Estudos

- **Estado:** active — base operacional 0.5 implementada e publicada, com CI remota aprovada.
- **Prioridade no portfólio:** unassigned.
- **Data do estado:** 2026-11-03.
- **Próxima ação:** produzir o próximo material de concurso/cargo solicitado e registrar a avaliação pedagógica real do leitor.
- **Responsável:** agente para implementação e revisão; titular para avaliação de leitura e escolha de seu concurso.
- **Condição de conclusão desta etapa:** código remoto confirmado, verificações da entrega e 17 skills/documentação relidas no cofre.
- **GitHub:** destino informado pelo titular: https://github.com/kauanramalho/Gerados-de-Materiais-de-Estudos. Código publicado, histórico inicial preservado e SHA remoto confirmado. A CI aprovou verify e artifacts: https://github.com/kauanramalho/Gerados-de-Materiais-de-Estudos/actions/runs/41642703635. O bloqueio anterior está resolvido para esse destino.

## Base operacional

Apostila e caderno por manifesto; pedido por texto/foto/print; leitura de instruções/skills com hashes; pesquisa de concurso/banca/provas/fontes; cobertura completa da seleção em --final; navegação por áreas/destinos do PDF; fontes e questões rastreáveis. Sem recorte, o pedido abrange todo o programa do cargo e não tem teto artificial de páginas. Ver [fluxo completo](docs/do-pedido-a-entrega.md).

A versão 0.5 implementa simulado e pontuação, revisão ativa, comparação de edições/erratas e auditoria de acessibilidade. Há 17 skills locais. A pontuação cobre pesos, erro/branco, anulação com crédito ou exclusão e denominador zero. A edição identifica impacto em fontes, questões e capítulos sem alterar o original. A auditoria mede teclado, contraste, descrições e estrutura; marcação PDF e nomes acessíveis de SVG foram corrigidos. Não é certificação PDF/UA.

## Evidências de produção

- SQL: apostila 24 páginas e caderno 15; 13 casos técnicos, três figuras, oito autorais e três reais por link. O gabarito real de 2026 consultado permanece identificado como preliminar.
- Matemática: apostila 16 e caderno 9, dois diagramas, fórmulas/tabela e seis autorais; simulado de 10 páginas e revisão de 12. Exemplo de pontuação: 3,75/6, com regras autorais explícitas.
- Redes/LGPD: painel genérico detalhado, texto normativo oficial e quatro questões. Não atribuído a concurso/banca; valida impressão de figura e dispositivo legal.
- Curadoria: páginas reais de dois capítulos abertos comparadas, com edição, páginas e licenças em [curadoria editorial](docs/curadoria-editorial-aplicada.md).
- Edições: exemplo editorial altera a explicação de uma autoral, preservando gabarito e IDs; alterações de gabarito nos testes são sintéticas.

Passaram 119 testes locais; a CI em outro host aprovou validações, oito PDFs, navegação, pontuação e auditorias. O acervo preservado cresceu para 21 itens. Os resultados, hashes e evidências ficam no relatório de fechamento. Ver [validação por matéria/formato](docs/validacao-multimateria.md) e [prontidão](docs/prontidao.md). Os testes estruturais não comprovam pesquisa factual ou aprendizagem por si sós.

## Continuidade e limites

O titular aprovou o layout; manter CSS, tipografia e sumário acadêmico. Sua avaliação pedagógica ainda não foi registrada e não será inventada. Uma coleção completa depende do concurso/cargo que for solicitado. O agente deve pesquisar, produzir, revisar e validar cada novo pedido; os demonstradores não são cobertura universal de qualquer edital.

Leitor de tela real, conformidade integral e calibração de dificuldade não foram certificados. Fontes externas e gabaritos preliminares exigem nova consulta ao reutilizar. O acervo cresce por lote; preservar banco e histórico. O projeto opera em sessões do agente com acesso aos arquivos/ferramentas; não há serviço sempre ligado, scheduler ou instalação global presumidos.

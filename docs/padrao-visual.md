# Sistema visual inicial

O titular aprovou o layout em 03/11/2026. Preservar a apresentação atual, inclusive tipografia, cores e sumário acadêmico. Mudanças de navegação devem manter a aparência; conferir por PDF renderizado e comparação de páginas/texto. A aprovação visual não certifica conteúdo ou aprendizagem.

| Elemento | Padrão inicial | Critério de revisão |
|---|---|---|
| Página | A4, coluna única, margens 20 mm | leitura confortável e espaço para anotações |
| Corpo | serifada de sistema, 11,5 pt, entrelinha 1,5 | sem linhas longas e sem texto espremido |
| Títulos | sem serifa, hierarquia H1/H2/H3 | estrutura sem saltos de nível |
| Cores | azul escuro, verde petróleo, cinza; fundo branco | contraste e leitura em tons de cinza |
| Figuras | SVG quando apropriado; raster com resolução suficiente | rótulos legíveis em tamanho final |
| Caixas | borda e título textual | significado compreensível sem cor |
| Questões | ID, origem, enunciado e alternativas | enunciado sem gabarito à vista |
| Referências | links descritivos e origem rastreável | fonte identificável também na impressão |

## Figuras didáticas

Escolher representação de acordo com a tarefa: partes → desenho rotulado; sequência → etapas; relação → diagrama; decisão → fluxo; comparação → tabela; quantidade → gráfico. Não impor quantidade de figuras por página. Investir em figuras que eliminem dúvida, sem decoração excessiva.

Cada figura recebe: ID, título, propósito de aprendizagem, rótulos, legenda, descrição alternativa, fonte/licença e eventual adaptação. Remeter a ela no corpo. Diagramas técnicos exigem validação de conectores, direções, camadas, escalas e relações.

No exemplo de switch, diferenciar portas Ethernet, uplink e console quando existirem. Não presumir que todo equipamento tenha os mesmos conectores, velocidade ou PoE. Identificar um desenho genérico como esquema; usar manual do fabricante para representar um modelo real.

Fotografias podem ser anotadas quando os direitos permitirem. Imagem gerada por IA não comprova uma configuração real; validar a informação e evitar detalhes técnicos inventados. Descrever equipamentos exatos por desenhos apoiados em documentação quando necessário.

## Paginação e navegação

O sumário deve seguir apresentação editorial acadêmica: títulos e subtítulos numerados, recuos consistentes, capítulos com maior peso, linhas pontilhadas discretas e coluna de páginas alinhada à direita. Usar fundo branco e hierarquia tipográfica, sem marcadores de lista visíveis ou caixa de navegação. Os números devem corresponder ao PDF final e aos rodapés, com validação após a exportação. Na amostra, os destinos nomeados do primeiro PDF alimentam os números da segunda passagem; conferir estabilidade antes da entrega.

Manter título com o parágrafo seguinte; evitar órfãs e viúvas; controlar quebras em figuras, tabelas e alternativas. Tabelas longas precisam de cabeçalho repetido. Sumário, glossário e índice de figuras devem navegar por IDs, sem números de página digitados manualmente.

Cada questão aponta para seu gabarito comentado e cada resolução retorna à questão. A resolução pode ligar à seção de teoria. Testar após a exportação: destinos válidos, texto selecionável, fontes incorporadas ou fallback legível, figuras sem corte e nenhuma página vazia acidental. Acessibilidade PDF exige auditoria adicional; o protótipo não declara conformidade PDF/UA.

A regra de navegação é obrigatória em todos os próximos lotes: [contrato, testes e comando de reauditoria](navegacao.md). A mesma página pode conter várias questões; o link precisa apontar à resolução correta, não somente a uma página existente.

No publicador 0.2, SVGs incorporados respeitam a largura da coluna para evitar redução global da impressão. Blocos de questões, comentários e código evitam quebras internas quando cabem. A mediana dos trechos longos do PDF é registrada na auditoria; valor abaixo de 10 pt bloqueia a publicação. Inspecionar também rótulos e legendas: a mediana não comprova sua legibilidade.

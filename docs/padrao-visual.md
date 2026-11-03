# Sistema visual inicial

Proposta v0.1, sujeita à avaliação do piloto. A qualidade visual será confirmada por PDF renderizado; o CSS sozinho não comprova resultado.

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

Manter título com o parágrafo seguinte; evitar órfãs e viúvas; controlar quebras em figuras, tabelas e alternativas. Tabelas longas precisam de cabeçalho repetido. Sumário, glossário e índice de figuras devem navegar por IDs, sem números de página digitados manualmente.

Cada questão aponta para seu gabarito comentado e cada resolução retorna à questão. A resolução pode ligar à seção de teoria. Testar após a exportação: destinos válidos, texto selecionável, fontes incorporadas ou fallback legível, figuras sem corte e nenhuma página vazia acidental. Acessibilidade PDF exige auditoria adicional; o protótipo não declara conformidade PDF/UA.

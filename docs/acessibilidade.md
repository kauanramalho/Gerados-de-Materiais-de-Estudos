# Auditoria de acessibilidade e limites

A exportação solicita marcação estrutural e outline ao Chromium. Tags e marcadores ajudam a navegação, mas não certificam PDF/UA, WCAG integral ou compatibilidade com todo leitor de tela.

```sh
python scripts/acessibilidade.py build/matematica-basica/revisao.html build/matematica-basica/revisao.pdf --report build/acessibilidade.json
```

A ferramenta mede idioma, hierarquia de títulos, imagens informativas com alt, cabeçalhos de tabelas e conteúdo MathML. Calcula contraste de texto/fundo CSS segundo a luminância relativa: 4,5:1 para texto comum e 3:1 para texto grande conforme tamanho/peso. Percorre links com Tab e confere ordem/foco visível. No PDF, verifica presença de estrutura, ordem dos títulos que têm destinos e texto dentro da página.

O agente revisa se a descrição de figura ensina sua informação essencial, se o exercício pode ser resolvido sem depender só de cor e se fórmulas/tabelas têm explicação equivalente. Inspecionar casos representativos e todos os defeitos sinalizados. Fundo complexo, contraste dentro da imagem, ordem semântica fina de tabela e interpretação assistiva de fórmulas não são aprovados por esses checks. A leitura com tecnologia assistiva real continua uma validação específica a registrar quando executada.

No fechamento, a primeira auditoria encontrou PDFs sem árvore estrutural. A exportação foi corrigida com marcação explícita; a revisão de matemática passou em idioma, teclado, contraste, MathML, tags, títulos e limites de página. A correção não redesenha o layout. Os demais relatórios por artefato registram os testes realmente executados e suas ressalvas.

Na validação 0.6, a amostra extensa de SQL revelou números destacados com contraste de 3,01:1 no tema padrão do Pandoc. `styles/code-accessible.theme` ajusta as cores abaixo de 4,7:1 contra o fundo de código existente. CSS, fontes e apresentação do sumário aprovados foram preservados. A ordem de teclado considera links com `tabIndex >= 0`; âncoras de linhas de código com `tabindex=-1` não entram na sequência de Tab. Links ocultos da tecnologia assistiva que sejam focáveis continuam tratados como erro. Regressões verificam esse caso em HTML/PDF real.

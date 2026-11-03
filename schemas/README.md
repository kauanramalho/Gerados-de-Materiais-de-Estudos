# Contratos de dados v0.3

JSON Schema 2020-12 descreve briefing, questões, manifesto, fontes, figuras e cobertura. `scripts/contracts.py` usa jsonschema e FormatChecker para validar tipos, datas, campos obrigatórios e propriedades extras. Instale `requirements-core.txt`. Os contratos apoiam a publicação sem substituir revisão editorial ou consulta aos documentos originais.

`scripts/check.py` verifica os próprios schemas, a amostra e os manifestos presentes. A CLI valida as entradas efetivamente usadas antes de compor o material; um schema de briefing disponível não significa que todo pedido tenha briefing JSON persistido.

Questão REAL exige origem completa e gabarito oficial. AUTORAL não pode receber uma atribuição fictícia de banca. Para ADAPTADA, registrar origem e mudanças. A publicação do texto de terceiros depende de direitos; o registro pode apontar apenas para o item na prova.

- [Pedido](pedido.schema.json): texto/imagem, identidade, programa/seleção, pesquisa e leitura versionada. O agente preenche; scripts/pedido.py inicia e o publicador aplica em --final. Ver [fluxo](../docs/do-pedido-a-entrega.md).
- [Briefing](briefing.schema.json)
- [Questão](questao.schema.json)

- [Manifesto de material](material.schema.json). A CLI build_material.py aplica também verificações de arquivos, cobertura, fontes, figuras e navegação.
- [Fontes](fontes.schema.json)
- [Figuras](figuras.schema.json)
- [Cobertura](cobertura.schema.json)
- [Simulado](simulado.schema.json): matriz, duração e pontuação.
- [Revisão](revisao.schema.json): capítulos curtos e remissões.

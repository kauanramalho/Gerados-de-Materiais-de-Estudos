# Contratos de dados v0.1

JSON Schema 2020-12 descreve os formatos de briefing, questões e manifesto de material. Os contratos apoiam a publicação, sem substituir a revisão editorial. `scripts/check.py` verifica a amostra, a estrutura documental e os manifestos em materials/ usando a biblioteca padrão; validação genérica de todos os schemas é uma tarefa do pipeline futuro.

Questão REAL exige origem completa e gabarito oficial. AUTORAL não pode receber uma atribuição fictícia de banca. Para ADAPTADA, registrar origem e mudanças. A publicação do texto de terceiros depende de direitos; o registro pode apontar apenas para o item na prova.

- [Briefing](briefing.schema.json)
- [Questão](questao.schema.json)

- [Manifesto de material](material.schema.json). A CLI build_material.py aplica também verificações de arquivos, cobertura, fontes, figuras e navegação.

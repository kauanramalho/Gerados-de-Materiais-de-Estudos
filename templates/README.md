# Modelos de trabalho

Copiar os modelos para `work/<id-da-execucao>/` (ignorado pelo Git) e preencher somente fatos verificados. Usar `não localizado`, `não definido` ou uma lacuna explícita em vez de inventar dados.

- [Briefing](briefing.md): identidade do concurso, escopo e fontes oficiais.
- [Matriz de cobertura](matriz-cobertura.csv): edital → objetivos → capítulos → questões.
- [Registro de fontes](fontes.csv): origem, atualização e direitos.
- [Perfil da banca](perfil-banca.md): amostra, padrões observados e limites.
- [Plano e texto de capítulo](capitulo.md): sequência editorial.
- [Manifesto de figuras](figuras.csv): propósito, legenda e origem.
- [Questão e resolução](questao.md): identidade, comentário e navegação.
- [Relatório de entrega](relatorio.md): validação e estado real.
- [Avaliação do piloto](avaliacao-piloto.md): registrar retorno do leitor sem presumir aceite.
- [Checklist de revisão](checklist-revisao.md): evidências e defeitos por dimensão editorial.

Os contratos JSON descrevem o formato futuro de ingestão; os modelos Markdown/CSV já podem ser usados pelo agente. Não são formulários obrigatórios para o usuário.

Para o publicador genérico: use [manifesto-material.json](manifesto-material.json) e [conteudo-capitulo.md](conteudo-capitulo.md). Copie-os para a pasta de trabalho e prepare as quatro listas JSON indicadas no manifesto; não publique os textos de preenchimento.

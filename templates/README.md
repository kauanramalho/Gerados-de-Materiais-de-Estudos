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

Os contratos JSON já são aplicados pelas ferramentas. O agente prepara pedido.json a partir de texto/foto/print e preenche os demais registros; não são formulários obrigatórios para o usuário. Veja [fluxo completo](../docs/do-pedido-a-entrega.md) e [checkpoint de produção](estado-producao.md).

Para o publicador genérico: use [manifesto-material.json](manifesto-material.json) e [conteudo-capitulo.md](conteudo-capitulo.md). Copie-os para a pasta de trabalho e prepare as quatro listas JSON indicadas no manifesto; não publique os textos de preenchimento.

# Ateliê de Estudos

Repositório público: [Gerados-de-Materiais-de-Estudos](https://github.com/kauanramalho/Gerados-de-Materiais-de-Estudos).

Base permanente de instruções, skills e modelos para produzir apostilas e cadernos de questões de concursos, com explicações claras, ilustrações úteis e fontes verificáveis.

**Fase atual:** publicador 0.5, simulado/pontuação, revisão ativa, edições/erratas e acessibilidade; entrada por texto/foto/print, pesquisa e cobertura vinculadas ao pedido, navegação auditada, dois pilotos e acervo local. O projeto é conduzido por um agente com acesso a este repositório. Ainda não existe um serviço autônomo que receba editais ou gere apostilas sem uma sessão de trabalho.

## Como pedir um material

Abra uma tarefa com este repositório como contexto e diga, por exemplo:

> Vou fazer o concurso X e quero a apostila.

> Quero um caderno de questões para este concurso. [Foto ou print anexado.]

O agente lê todas as instruções e skills, identifica o concurso, pesquisa edital, retificações, banca, provas e fontes, e produz o formato pedido. Sem recorte, o escopo é todo o programa do cargo. Não há teto artificial de páginas: explicar e praticar o necessário até concluir. O mesmo fluxo vale para conteúdo e questões; o usuário não precisa fornecer formulário, banca ou edital. Veja o [contrato completo do pedido à entrega](docs/do-pedido-a-entrega.md), incluindo ingestão por imagem, checkpoints e verificação final de cobertura. Em outra conversa, fornecer o repositório novamente: os arquivos não garantem memória automática fora deste contexto.

## O que está disponível

- [Instruções para agentes](AGENTS.md) e [17 skills editoriais](docs/skills.md), com entradas, procedimentos, saídas e critérios de aceite.
- [Planejamento](docs/planejamento.md), [arquitetura](docs/arquitetura.md), [roadmap](docs/roadmap.md) e [backlog](docs/backlog.md).
- [O que falta para ficar pronto](docs/prontidao.md): lacunas verificadas, skills candidatas, documentos previstos e critérios de conclusão.
- [Navegação obrigatória](docs/navegacao.md): sumário clicável, resolução correta, retorno, hashes e bloqueio de exportação com erro. O layout atual foi aprovado pelo titular.
- [Manual editorial](docs/manual-editorial.md), [padrão visual](docs/padrao-visual.md), [política de questões](docs/questoes.md) e [revisão](docs/qualidade.md).
- [Referências pesquisadas](references/catalogo.md), [modelos reutilizáveis](templates/README.md), [contratos de dados](schemas/README.md) e prova mínima de navegação em [examples/redes](examples/redes/README.md).
- [Progresso](Progress.md), [decisões](Decisions.md) e [continuidade no Segundo Cérebro](docs/continuidade.md).

Entregas finais de concurso usam pedido.json vinculado ao manifesto e `--final`. Pilotos sem pedido continuam como referências e não certificam cobertura de um novo pedido. A pesquisa e a leitura de imagens são executadas pelo agente; os scripts validam o registro e os arquivos.

## Produzir novos materiais

O agente já pode montar materiais a partir de um manifesto. O piloto contém teoria, três figuras, exemplos SQL verificados, oito questões autorais e três referências a questões reais com comentário. Veja o [fluxo de produção](docs/producao.md) e o [piloto](materials/dataprev-sql/README.md).

O [piloto de matemática](materials/matematica-basica/README.md) acrescenta seis questões autorais, fórmulas sem JavaScript e tabela com continuação. O [acervo local](docs/acervo.md) permite importar os dois lotes, buscar e deduplicar 21 itens, com histórico de revisões explícitas.

```sh
python scripts/build_material.py materials/dataprev-sql/material.json --check
python scripts/build_material.py materials/dataprev-sql/material.json --pdf
python scripts/build_material.py materials/dataprev-sql/material.json --kind caderno --pdf
```

Também estão implementados [simulado e pontuação](docs/simulados.md), [revisão ativa](docs/revisao-aprendizagem.md), [impacto e erratas](docs/manutencao-edicoes.md), [auditoria de acessibilidade](docs/acessibilidade.md) e o [demonstrador redes/LGPD](materials/redes-lgpd/README.md). O layout aprovado permanece como padrão.

## Verificar e gerar a amostra inicial

Requer Python 3.11+ e `pip install -r requirements-core.txt` para validar os contratos JSON. Para HTML, requer Pandoc. Para PDF, instale `requirements-pdf.txt` e use Chromium/Chrome de sistema ou `python -m playwright install chromium`. Não exige chave de API.

```sh
python scripts/check.py
python -m unittest discover -s tests -v
python scripts/build_sample.py
python scripts/build_sample.py --pdf
```

Saídas em `build/`: HTML autocontido e, com `--pdf`, PDF A4. O sumário apresenta hierarquia numerada, linhas pontilhadas e páginas obtidas dos destinos reais do PDF; a exportação confere a paginação em duas passagens. O HTML recebe esses mesmos números quando gerado com `--pdf`. A amostra demonstra diagramação e links; não é material de um concurso identificado nem certifica equivalência com uma banca. O pipeline editorial completo está no roadmap.

## Escopo e limites

Português do Brasil; rigor técnico proporcional ao edital; texto desenvolvido, prática e revisão. Questões reais conservam identificação da prova e gabarito oficial; autorais são identificadas como tal. Fontes sem direitos claros são referenciadas por link até verificação. Nenhum acervo de terceiros ou dado privado do Drive faz parte desta base pública.

Não há agendamento, sincronização automática com Drive, instalação global de skills ou cobrança de API configurados. Atualizações são executadas em tarefas autorizadas e verificadas.

## Autoria e licença

Projeto de Kauan Ramalho. Documentação inicial e ferramentas produzidas com assistência de IA. [Licença e direitos](LICENSE.md): o repositório público não concede, por si só, licença de redistribuição dos conteúdos; referências externas mantêm seus próprios termos.

# Ateliê de Estudos

Repositório público: [Gerados-de-Materiais-de-Estudos](https://github.com/kauanramalho/Gerados-de-Materiais-de-Estudos).

Base permanente de instruções, skills e modelos para produzir apostilas e cadernos de questões de concursos, com explicações claras, ilustrações úteis e fontes verificáveis.

**Fase atual:** publicador 0.7, quatro formatos, validação de imagens em todas as entradas e acompanhamento de figuras nas edições; entrada por texto/foto/print, pesquisa e cobertura vinculadas ao pedido, navegação auditada e acervo local. O projeto é conduzido por um agente com acesso a este repositório. Ainda não existe um serviço autônomo que receba editais ou gere apostilas sem uma sessão de trabalho.

## Como pedir um material

Abra uma tarefa com este repositório como contexto e diga, por exemplo:

> Vou fazer o concurso X e quero a apostila.

> Quero um caderno de questões para este concurso. [Foto ou print anexado.]

O agente lê todas as instruções e skills, identifica o concurso, pesquisa edital, retificações, banca, provas e fontes, e produz o formato pedido. Sem recorte, o escopo é todo o programa do cargo. Não há teto artificial de páginas: explicar e praticar o necessário até concluir. O mesmo fluxo vale para conteúdo e questões; o usuário não precisa fornecer formulário, banca ou edital. Veja o [contrato completo do pedido à entrega](docs/do-pedido-a-entrega.md), incluindo ingestão por imagem, checkpoints e verificação final de cobertura. Em outra conversa, fornecer o repositório novamente: os arquivos não garantem memória automática fora deste contexto.

## O que está disponível

- [Instruções para agentes](AGENTS.md) e [17 skills editoriais](docs/skills.md), com entradas, procedimentos, saídas e critérios de aceite.
- [Planejamento](docs/planejamento.md), [arquitetura](docs/arquitetura.md), [roadmap](docs/roadmap.md) e [backlog](docs/backlog.md).
- [Estado de prontidão](docs/prontidao.md): desenvolvimento entregue, evidências e avaliação real pelo leitor em acompanhamento.
- [Navegação obrigatória](docs/navegacao.md): sumário clicável, resolução correta, retorno, hashes e bloqueio de exportação com erro. O layout atual foi aprovado pelo titular.
- [Manual editorial](docs/manual-editorial.md), [padrão visual](docs/padrao-visual.md), [política de questões](docs/questoes.md) e [revisão](docs/qualidade.md).
- [Referências pesquisadas](references/catalogo.md), [modelos reutilizáveis](templates/README.md), [contratos de dados](schemas/README.md) e prova mínima de navegação em [examples/redes](examples/redes/README.md).
- [Progresso](Progress.md), [decisões](Decisions.md) e [continuidade no Segundo Cérebro](docs/continuidade.md).

Entregas finais de concurso usam pedido.json vinculado ao manifesto e `--final`. Pilotos sem pedido continuam como referências e não certificam cobertura de um novo pedido. A pesquisa e a leitura de imagens são executadas pelo agente; os scripts validam o registro e os arquivos.

## Produzir novos materiais

**Padrão obrigatório de todas as entregas:** o sumário inteiro é clicável no próprio PDF. Número, título, pontilhado e página levam à seção correspondente, tanto na apostila quanto no caderno de questões, simulado e revisão. O publicador grava destinos diretos de página/posição e recusa exportação com qualquer linha parcialmente clicável, página incorreta ou destino errado. A auditoria pertence ao hash do arquivo entregue; o padrão não depende de solicitar links a cada novo material. Ver [contrato de navegação](docs/navegacao.md).

O agente já pode montar materiais a partir de um manifesto. O piloto contém teoria, três figuras, exemplos SQL verificados, oito questões autorais e três referências a questões reais com comentário. Veja o [fluxo de produção](docs/producao.md) e o [piloto](materials/dataprev-sql/README.md).

O [caso de Banco de Dados Dataprev/FGV](materials/dataprev-bd/README.md) desenvolve os 17 itens da matéria do Perfil 3, com 17 capítulos, 12 figuras e 49 questões. Veja o [protocolo de validação real](docs/validacao-real-dataprev.md) e a [avaliação pedagógica](docs/avaliacao-pedagogica.md), que distingue revisão editorial e retorno do leitor.

O [piloto de matemática](materials/matematica-basica/README.md) acrescenta seis questões autorais, fórmulas sem JavaScript e tabela com continuação. O [acervo local](docs/acervo.md) preserva 67 questões únicas e 70 revisões nos quatro materiais, com busca, deduplicação e histórico explícito.

```sh
python scripts/build_material.py materials/dataprev-sql/material.json --check
python scripts/build_material.py materials/dataprev-sql/material.json --pdf
python scripts/build_material.py materials/dataprev-sql/material.json --kind caderno --pdf
```

Também estão implementados [simulado e pontuação](docs/simulados.md), [revisão ativa](docs/revisao-aprendizagem.md), [impacto e erratas](docs/manutencao-edicoes.md), [auditoria de acessibilidade](docs/acessibilidade.md) e o [demonstrador redes/LGPD](materials/redes-lgpd/README.md). O layout aprovado permanece como padrão.

## Verificar e gerar a amostra inicial

Requer Python 3.11+, `pip install -r requirements-core.txt` e Pandoc para validar os manifestos e o Markdown efetivamente renderizado. Para PDF, instale `requirements-pdf.txt` e use Chromium/Chrome de sistema ou `python -m playwright install chromium`. Não exige chave de API.

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

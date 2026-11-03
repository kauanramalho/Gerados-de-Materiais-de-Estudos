# Ateliê de Estudos

Base permanente de instruções, skills e modelos para produzir apostilas e cadernos de questões de concursos, com explicações claras, ilustrações úteis e fontes verificáveis.

**Fase atual:** fundação editorial e planejamento. O projeto é conduzido por um agente com acesso a este repositório. Ainda não existe um serviço autônomo que receba editais ou gere apostilas sem uma sessão de trabalho.

## Como pedir um material

Abra uma tarefa com este repositório como contexto e diga, por exemplo:

> Leia AGENTS.md e use ae-orquestrar. Quero estudar para [órgão, cargo e ano]. Segue o edital/link. Prepare uma apostila sobre [assunto], com teoria explicada, figuras comentadas, exemplos resolvidos, questões reais verificadas e questões autorais no perfil da banca, com gabarito comentado e navegação clicável.

O agente deve recuperar o estado do projeto, identificar o concurso, buscar edital e retificações, analisar provas relacionadas, escolher as skills e registrar a execução. Em outra conversa, fornecer o repositório novamente: os arquivos não garantem memória automática fora deste contexto.

## O que está disponível

- [Instruções para agentes](AGENTS.md) e [12 skills editoriais](docs/skills.md), com entradas, procedimentos, saídas e critérios de aceite.
- [Planejamento](docs/planejamento.md), [arquitetura](docs/arquitetura.md), [roadmap](docs/roadmap.md) e [backlog](docs/backlog.md).
- [Manual editorial](docs/manual-editorial.md), [padrão visual](docs/padrao-visual.md), [política de questões](docs/questoes.md) e [revisão](docs/qualidade.md).
- [Referências pesquisadas](references/catalogo.md), [modelos reutilizáveis](templates/README.md), [contratos de dados](schemas/README.md) e prova mínima de navegação em [examples/redes](examples/redes/README.md).
- [Progresso](Progress.md), [decisões](Decisions.md) e [continuidade no Segundo Cérebro](docs/continuidade.md).

## Verificar e gerar a amostra

Requer Python 3.11+ e Pandoc para HTML. Para PDF, requer Chromium/Chrome, Playwright e PyMuPDF (`pip install -r requirements-pdf.txt`). A verificação usa apenas a biblioteca padrão do Python; não exige chave de API.

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

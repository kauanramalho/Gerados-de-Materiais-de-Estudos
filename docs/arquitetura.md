# Arquitetura de execução e informação

## Decisão inicial

O produto começa como um repositório editorial operado por um agente. Isso permite melhorar o método antes de construir um serviço de geração. O conteúdo estruturado e as ferramentas de publicação devem permanecer independentes do provedor de IA.

```mermaid
flowchart LR
  A[Texto, foto ou print] --> B[Briefing e matriz de cobertura]
  B --> C[Fontes e perfil da banca]
  C --> D[Plano de capítulo e figuras]
  D --> E[Redação e questões]
  E --> F[Revisão técnica e editorial]
  F --> G[Diagramação HTML e PDF]
  G --> H[Validação e entrega]
  H --> I[Progresso e decisões]
```

O [fluxo do pedido à entrega](do-pedido-a-entrega.md) começa com pesquisa pelo agente. scripts/pedido.py preserva texto/imagem e inventaria instruções; scripts/request.py confere pesquisa registrada, versão lida e cobertura do edital em --final. Esses scripts não substituem visão ou navegação web. Material completo não tem teto artificial de páginas; unidades são checkpoints até terminar.

## Camadas

| Camada | Responsabilidade | Formato |
|---|---|---|
| Instruções | regras permanentes e roteamento | AGENTS.md e .agents/skills/ |
| Planejamento | entregas, dependências e decisões | docs/, Progress.md, Decisions.md |
| Evidências | edital, fontes, prova, gabarito e permissões | registros estruturados e originais privados |
| Conteúdo | texto original, figuras e itens com IDs estáveis | Markdown, SVG, JSON |
| Publicação | conversão e estilos | Pandoc + CSS; Chromium no protótipo |
| Controle | integridade, navegação e revisão humana | Python + relatórios de validação |
| Memória | contexto pessoal e continuidade | Segundo Cérebro; sem cópia pública |

## Contratos e rastreabilidade

Briefing → IDs de itens do edital → objetivos de aprendizagem → capítulos → questões. Toda questão real liga a um registro de prova e gabarito. Toda figura liga a um propósito e registro de direitos. Toda entrega registra versão das instruções e ferramentas, data de conferência e resultado das validações.

IDs persistem entre revisões: `CAP-001`, `FIG-001`, `Q-AUT-001`, `Q-REAL-001`; âncoras de exportação `q-aut-001`, `res-q-aut-001`. Não usar posição na página como identidade. Evitar renumeração automática que quebre links antigos.

## Publicação

Markdown é a fonte editorial. HTML serve à leitura e à revisão; PDF A4 serve à distribuição. A CLI `scripts/build_material.py` 0.4 recebe manifesto, capítulos, figuras, fontes, cobertura e questões, compondo apostila ou caderno com Pandoc e Chromium via Playwright. O sumário usa os destinos do PDF para conferir as páginas; a navegação e os hashes são registrados. `scripts/build_sample.py` preserva a demonstração inicial de redes.

O publicador 0.3 aplica contratos com jsonschema, exporta fórmulas MathML sem JavaScript e foi aplicado a SQL/matemática em apostila/caderno. Uma tabela com continuação e sete fórmulas foram conferidas no novo lote. Ligação entre volumes, texto normativo, outras figuras detalhadas e auditoria completa de acessibilidade permanecem pendentes. HTML com títulos/descrições não certifica PDF acessível. Avaliar outro motor de impressão somente se os testes demonstrarem uma limitação concreta; ver [prontidão](prontidao.md) e [produção](producao.md).

O [catálogo local](acervo.md) guarda questões, revisões imutáveis e ocorrências por edição em SQLite. Busca e exportação usam snapshots consistentes; importação usa transação. Os manifestos são entradas da produção e os bancos completos são arquivados fora do Git. Alterações de resposta não recompõem automaticamente materiais já entregues.

## Integrações

GitHub versiona a base. Drive armazena notas de gestão e entregas quando autorizado. Uma escrita em um sistema não prova sincronização do outro: confirmar cada destino por leitura. Sem espelhamento integral do cofre, upload automático de documentos privados, credenciais no Git ou scheduler neste estágio.

## Evolução para serviço

Somente após o piloto: avaliar CLI de produção, modelo de tarefas, armazenamento de artefatos e adaptador de LLM. Se houver aplicação multiusuário, então definir autenticação, custos, quotas, isolamento de arquivos e recuperação de tarefas. A plataforma e o provedor dependem de uma necessidade demonstrada; não estão escolhidos agora.

# Auditoria completa do Ateliê de Estudos

Data: 03/11/2026, America/Sao_Paulo. Código examinado: `709db22bc0d636721e4ae06d7b0e86a36af714b6`, release v0.5.0. Auditoria documental, de código e de artefatos, com testes existentes e ensaios adicionais em cópias descartáveis. Nenhum defeito foi corrigido nesta auditoria.

## Parecer

**O projeto ainda não está concluído.** A base operada pelo agente existe, está publicada e produz quatro formatos. Duas falhas técnicas foram reproduzidas fora da suíte existente. Também não há evidência de um pedido real novo percorrendo identificação por texto/imagem, pesquisa e entrega integral do edital. O fechamento anterior comprova a entrega da base 0.5 e dos exemplos; não comprova todo o objetivo original.

O projeto foi desenhado para o funcionamento solicitado: o usuário informa o concurso e pede o material; o agente consulta instruções e skills, pesquisa as fontes oficiais e produz até concluir o escopo, sem teto artificial de páginas. Não é necessário instalar um serviço sempre ligado para cumprir esse modelo. A execução completa desse compromisso ainda precisa de aceite real.

## Matriz dos requisitos originais

| Requisito | Verificação | Situação |
|---|---|---|
| Repositório público e versionado | remoto main igual ao código examinado; release v0.5.0 pública e CI aprovada | entregue |
| Gestão e documentação no Segundo Cérebro | 79 arquivos relacionados relidos; bytes/textos iguais à última gravação; hashes de origem dos cartões correspondem ao Git | entregue para a base examinada |
| Skills e instruções reutilizáveis | 17 SKILL.md e 17 cartões independentes; instruções, contratos, modelos e manual disponíveis | escritos; validação prática parcial |
| Pedido simples por texto/foto/print | ingestão preserva imagem/hash; transcrição e pesquisa atribuídas ao agente; testes sintéticos passam | implementado; falta aceite real completo |
| Identificação e pesquisa oficial | fluxo exige edital, retificações, banca, provas-alvo/relacionadas, conteúdo e acervo | instruído e registrado; pesquisa não é provada por metadados |
| Material integral e focado no concurso | --final exige programa/seleção, cobertura e vínculo de questões; sem limite artificial de páginas | contrato entregue; nenhuma coleção final real comprovada |
| Didática, figuras e exemplos resolvidos | SQL, matemática e redes/LGPD demonstram o padrão; referências editoriais consultadas | exemplos entregues; avaliação de aprendizagem pendente |
| Reais e autorais com comentários | catálogo com 21 itens; fontes/direitos/status diferenciados; reais por link quando reprodução não confirmada | mecanismo entregue; revalidar cada novo lote |
| Sumário e questão ↔ resolução clicáveis | oito PDFs, hashes e 341 áreas internas rechecados | passou nos artefatos examinados |
| Simulado, revisão e manutenção | formatos e pontuação existem; ensaios adicionais acharam duas lacunas | correções pendentes |
| Qualidade acessível | checks limitados de teclado, contraste, descrições, MathML e estrutura implementados | evidência parcial; sem certificação assistiva integral |

## Achados que exigem correção

### AE-026 — imagens escapam da validação em revisão e contexto

Severidade técnica alta: impede afirmar que todas as entradas renderizadas obedecem à política de recursos locais. Em `scripts/material.py`, a validação das imagens Markdown percorre somente os capítulos originais; `practice_context` apenas acrescenta o próprio Markdown aos inputs. Em `scripts/formats.py`, a revisão confere o caminho do capítulo, H1 e destinos, sem reaplicar a validação das imagens. O Pandoc incorpora recursos antes de o navegador bloquear a rede.

Reprodução: em cópias do exemplo de matemática, acrescentar uma imagem SVG de teste localizada um nível acima da pasta do material ao capítulo de revisão ou ao contexto do caderno. O capítulo original rejeita a mesma referência; revisão e contexto aceitam. A revisão gerou PDF com o marcador sintético `AUDIT-OUTSIDE-RESOURCE-0526`, navegação aprovada e build `passed`, sem incluir o arquivo externo entre os inputs com hash. Nenhum arquivo privado real foi lido ou publicado.

Efeito: recurso sem manifesto, origem/direitos e hash pode entrar no material; a construção não fica inteiramente rastreável e uma imagem indevida pode ser incorporada. O ensaio não demonstra leitura arbitrária de qualquer tipo de arquivo nem vazamento ocorrido nas apostilas existentes.

Aceite: validar todos os textos e todas as formas de inclusão de imagens efetivamente aceitas pelo renderizador, antes da incorporação. Rejeitar recurso fora da pasta, remoto ou não declarado; registrar os recursos permitidos nos hashes. Testar referências inválidas e imagens válidas nos quatro formatos.

### AE-027 — mudança de figura não sinaliza o capítulo afetado

Severidade técnica média: o relatório de impacto pode deixar de encaminhar revisão necessária. `scripts/edicoes.py` deriva capítulos de objetivos das questões afetadas e dos arquivos Markdown alterados; não acompanha o uso de uma imagem cujo arquivo mudou.

Reprodução: copiar duas edições de matemática, incrementar a versão de uma e mudar apenas um rótulo em `figuras/fatores.svg`. O resultado contém `changed: true` e `changed_files: ["figuras/fatores.svg"]`, mas `chapters_to_review: []`. O capítulo de porcentagens usa essa figura. O relatório detecta a mudança de arquivo; sua lista de capítulos está incompleta.

Aceite: propagar alterações de figuras aos capítulos que as usam ou sinalizar revisão conservadora quando a dependência não puder ser resolvida. Cobrir também inclusão/remoção e mudanças relevantes dos metadados editoriais. Reauditar o PDF da nova edição; preservar os anteriores.

## Validações ainda pendentes

1. **AE-028 — aceite real completo:** confirmar um concurso/cargo e processar pedido textual e foto/print legível, incluindo conferência visual e fontes oficiais. Produzir apostila e caderno até cobrir integralmente a seleção, com pesquisa de provas e revisão separada. Não escolher um concurso pessoal por inferência nem chamar o piloto Dataprev de pedido do titular.
2. **AE-009 — avaliação pedagógica:** o layout foi aprovado; clareza, progressão, aprendizagem e dificuldade precisam de evidência do leitor. Isso não é uma nova permissão de publicação e não impede corrigir defeitos técnicos.
3. **AE-023 — validação das skills:** os 17 procedimentos existem. No Segundo Cérebro, 11 cartões ainda têm status incomplete e seis active-with-caveats. Incomplete aqui indica aplicação/validação insuficiente, não ausência de arquivo. Registrar entradas, execução, resultado, defeitos e limites por procedimento; não promover estados apenas porque a suíte passou.
4. **AE-021 — coleção do edital escolhido:** produzir os capítulos e questões desse pedido. Não exige manter um catálogo pronto de todos os concursos possíveis.

Não falta inventar novas skills para cobrir a função central: os procedimentos já foram escritos. Faltam as correções, suas regressões, a evidência real de execução e a atualização dos registros de validação. Novas skills só se justificam se o uso revelar uma responsabilidade nova.

## Evidências e limites

- `python -m unittest discover -s tests -v`: 119 testes passaram novamente, em 27,696 segundos, sobre o código examinado. Os dois defeitos acima não fazem parte desses testes.
- `scripts/check.py`: valida documentação, contratos, 17 skills e manifestos. Sua aprovação não prova profundidade didática ou leitura das fontes.
- [CI 41648299037](https://github.com/kauanramalho/Gerados-de-Materiais-de-Estudos/actions/runs/41648299037): concluída com sucesso no mesmo SHA examinado. [Release v0.5.0](https://github.com/kauanramalho/Gerados-de-Materiais-de-Estudos/releases/tag/v0.5.0) publicada; sem binários anexados à release. PDFs/pacotes estão no Drive e nos artefatos da CI, que têm retenção de 14 dias.
- Oito PDFs de referência: 103 páginas e 192 entradas de sumário. Rechecagem de navegação sobre os próprios hashes passou: 339 ligações lógicas, distribuídas em 341 áreas clicáveis. Uma ligação quebrada em mais de uma linha pode ocupar duas áreas. Nenhum dos oito tem pedido final vinculado; seus relatórios dizem `draft-or-reference`.
- Cliques nativos no HTML: sete arquivos passaram no lote; o simulado teve timeout de dois segundos ao consultar a posição de um destino. A repetição isolada, sem alterar os hashes, passou com 69 cliques. As verificações concluídas somam 725 cliques; preservar também o lote que falhou. Trata-se de instabilidade observada no teste, sem defeito de destino reproduzido no PDF; melhorar o diagnóstico/robustez é recomendável. Não declarar que o lote único passou.
- Referências externas: 20 URLs responderam HTTP 200 em 03/11/2026 às 11h39, America/Sao_Paulo; PDFs responderam com assinatura PDF. É disponibilidade datada, não garantia permanente nem conferência factual integral do conteúdo.
- 79 documentos do Segundo Cérebro: 69 lidos como texto e dez JSON conferidos por bytes brutos; sem divergência em relação à última gravação. Os 17 cartões têm proveniência de IA e hashes de origem correspondentes. Isso comprova presença e integridade das cópias verificadas, não validação universal das skills.
- Limite semântico demonstrado com metadados sintéticos: trocar o destino teórico de uma questão por outro ID existente não causa erro na validação estrutural de escopo. A navegação pode apontar corretamente para um destino editorialmente inadequado. A revisão deve conferir o significado da remissão e o ensino do objetivo, além dos cliques.
- Não se executou um novo concurso completo, avaliação com alunos, certificação PDF/UA ou calibração psicométrica. Não se promete garantia eterna de URL externa: a disponibilidade precisa ser verificada em cada entrega e registrada com data.

## Critério para encerrar

Corrigir AE-026/027 com regressões; aplicar AE-028 a um alvo confirmado; conferir edital original contra matriz e conteúdo; revisar cada questão e remissão; gerar com --final; auditar sumário, retornos, destinos, fontes e bytes entregues; registrar a avaliação e os limites no projeto e no Segundo Cérebro. Até então, o estado correto é **base publicada e utilizável em sessão do agente, com correções e aceite pendentes**.

## Acompanhamento das pendências

As seis tarefas abertas do backlog foram espelhadas em issues durante a auditoria: [AE-009](https://github.com/kauanramalho/Gerados-de-Materiais-de-Estudos/issues/1), [AE-021](https://github.com/kauanramalho/Gerados-de-Materiais-de-Estudos/issues/2), [AE-023](https://github.com/kauanramalho/Gerados-de-Materiais-de-Estudos/issues/3), [AE-026](https://github.com/kauanramalho/Gerados-de-Materiais-de-Estudos/issues/4), [AE-027](https://github.com/kauanramalho/Gerados-de-Materiais-de-Estudos/issues/5) e [AE-028](https://github.com/kauanramalho/Gerados-de-Materiais-de-Estudos/issues/6). São registros de trabalho pendente, sem atribuição de prioridade humana ou declaração de correção.

## Situação posterior dos achados

Este relatório preserva o diagnóstico anterior às correções. A versão 0.6 corrige AE-026/027 e executa o [caso real de Banco de Dados](validacao-real-dataprev.md), com [evidências das 17 skills](validacao-skills-v06.md). Consulte o [estado atual](prontidao.md). A avaliação real pelo leitor continua distinta da revisão por IA.

# Decisões — Ateliê de Estudos

## D001 — 2026-11-03 — Repositório editorial operado por agente

**Decisão:** começar por instruções, skills, modelos e gestão versionados. **Motivo:** o pedido inicial é uma base de trabalho e planejamento, com produção futura sob demanda. **Consequência:** não é serviço autônomo nem exige contratação de API. **Revisar quando:** piloto demonstrar necessidade de execução persistente.

## D002 — 2026-11-03 — HTML e PDF navegáveis

**Decisão:** ambos são saídas padrão; IDs persistentes ligam sumário, questões e resoluções. **Motivo:** leitura em tela e distribuição de apostilas. **Consequência:** validar navegação após exportação. **Revisar quando:** testes de leitura ou impressão indicarem outro formato.

## D003 — 2026-11-03 — Proveniência explícita de questões

**Decisão:** distinguir REAL, ADAPTADA e AUTORAL, com gabarito oficial separado de comentários próprios. **Motivo:** evitar atribuição falsa e garantir rastreabilidade. **Consequência:** itens sem evidência não são publicados como reais; direitos incertos levam a referência por link. **Revisar quando:** houver novas condições de uso, mantendo a distinção de autoria.

## D004 — 2026-11-03 — Base pública e cofre preservado

**Decisão:** publicação pública autorizada pelo titular; apenas material sanitizado vai ao Git. **Motivo:** compartilhar a base sem expor documentos pessoais. **Consequência:** integração e relatórios privados ficam no Drive. **Revisar quando:** escopo ou destino de uma entrega mudar.

## D005 — 2026-11-03 — Skills locais com validação conservadora

**Decisão:** 12 procedimentos modulares em .agents/skills, com cartões independentes no cofre; sem instalação global automática. **Motivo:** facilitar retomada e evolução do método. **Consequência:** redação e validação estrutural não certificam comportamento no piloto. **Revisar quando:** um concurso real permitir testar cada fluxo.

## D006 — 2026-11-03 — Licença a definir pelo titular

**Decisão:** não atribuir licença aberta por inferência. **Motivo:** tornar público não determina autorização de redistribuição. **Consequência:** LICENSE.md explicita direitos e pendência, sem incorporar obras externas. **Revisar quando:** titular escolher licenças para ferramentas e conteúdo.

## D007 — 2026-11-03 — Sumário com apresentação acadêmica

**Decisão:** usar hierarquia numerada, recuos de subseções, linhas pontilhadas discretas e páginas alinhadas à direita, com fundo branco e links preservados. **Motivo:** o titular pediu uma apresentação semelhante à de livros e apostilas de graduação. **Consequência:** o publicador obtém as páginas dos destinos do PDF e verifica a paginação; rodapés mostram a mesma numeração. O padrão fica registrado em docs/padrao-visual.md. **Revisar quando:** nova avaliação visual do titular ou novos formatos exigirem ajuste.

## D008 — 2026-11-03 — Evolução editorial paralela à publicação

**Decisão:** executar piloto e desenvolver o publicador enquanto a criação no GitHub depende de acesso. **Motivo:** o titular autorizou avançar o desenvolvimento e implementar melhorias; a permissão remota não é requisito para validar materiais. **Consequência:** a pendência GitHub permanece explícita, sem bloquear o trabalho local e no Drive. **Revisar quando:** o repositório estiver acessível.

## D009 — 2026-11-03 — Piloto e publicador por manifesto

**Decisão:** usar um recorte público de modelagem relacional/SQL da Dataprev/FGV como referência e publicar apostila e caderno dos mesmos dados. **Motivo:** havia edital e provas no contexto, permitindo testar proveniência, questões e resultados executáveis. **Consequência:** a seleção não altera prioridade pessoal; itens reais têm status preliminar explícito e acesso por link; o aceite pedagógico depende de leitura e aplicação. **Revisar quando:** houver preferência diferente de concurso ou avaliação do leitor.

## D010 — 2026-11-03 — Contratos verificáveis e catálogo com revisões

**Decisão:** usar JSON Schema com validação de formatos antes da publicação e SQLite local para identidade, revisões e ocorrências de questões por edição. **Motivo:** o titular autorizou continuar as pendências diagnosticadas; tipos/datas incoerentes, duplicatas e alterações silenciosas prejudicam materiais reutilizados. **Consequência:** importar edição modificada exige nova versão; revisões divergentes exigem motivo registrado, preservam o estado anterior e não recompõem PDFs antigos. Fontes oficiais continuam conferidas pelo agente. **Revisar quando:** acervo ou concorrência exigirem outra forma de armazenamento, mantendo rastreabilidade e direitos.

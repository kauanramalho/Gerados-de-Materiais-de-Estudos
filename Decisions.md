# Decisões — Ateliê de Estudos

## D017 — 2026-11-04 — Sumário inteiro clicável como condição de entrega

**Decisão:** todo PDF de apostila, caderno de questões, simulado ou revisão deve permitir clicar em número, título, pontilhado/espaços e página para chegar à seção correspondente. O publicador 0.7 grava destinos diretos de página/posição (/XYZ), audita a área contínua de cada linha e bloqueia falhas. **Motivo:** requisito permanente reafirmado pelo titular e maior portabilidade entre leitores PDF; contagem de links ou clique somente no título não bastam. **Consequência:** manifesto de navegação versão 2 por hash, regressões de áreas parciais e verificação adicional em visualizador PDF quando o motor mudar. Dígitos de página não podem quebrar; o restante da apresentação aprovada é preservado. **Revisar quando:** o motor de exportação ou novos formatos exigirem atualização comprovada por testes, mantendo o requisito de navegação.

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

## D011 — 2026-11-03 — Layout aprovado e navegação obrigatória

**Decisão:** preservar o layout que o titular declarou ter gostado e conferir cada rota de navegação nos arquivos exportados. **Motivo:** pedido explícito de sumário clicável e links corretos em todas as futuras apostilas/cadernos. **Consequência:** exportação com destino, área clicável ou pareamento incorreto falha; relatórios são associados ao hash do arquivo. Referências externas têm verificação datada e não garantia permanente de disponibilidade. O aceite visual não encerra a avaliação didática. **Revisar quando:** titular pedir mudança visual ou um novo formato exigir contrato e testes próprios, mantendo o requisito de navegação.

## D012 — 2026-11-03 — Pedido simples, escopo integral e extensão necessária

**Decisão:** aceitar texto, foto ou print; o agente carrega todo o método e pesquisa concurso, edital/retificações, banca, provas anteriores/relacionadas, conteúdo e acervo. Pedido sem recorte abrange todo o programa do cargo, em apostila ou caderno, sem teto artificial de páginas. **Motivo:** o titular reiterou esse funcionamento e pediu correção de lacunas. **Consequência:** lotes são checkpoints internos até concluir o pedido; pedido.json e --final vinculam pesquisa/contexto e todos os itens selecionados ao material, detectando omissões e questões fora do escopo. Visão, pesquisa factual e revisão didática permanecem ações do agente e precisam de evidência real, além dos testes estruturais. **Revisar quando:** formato, ferramenta ou novo caso real exigir ajuste, preservando foco no pedido e transparência de lacunas.

## D013 — 2026-11-03 — Fechamento funcional e publicação

**Decisão:** usar o repositório público Gerados-de-Materiais-de-Estudos fornecido pelo titular, preservando seu primeiro commit. Implementar simulado/pontuação, revisão, edições/erratas e auditoria com quatro skills próprias. **Motivo:** pedido de resolver pendências e confirmar os destinos. **Consequência:** envio e CI foram conferidos; avaliação pedagógica e novas coleções exigem execução real. Gabarito do simulado fica em seção posterior no mesmo PDF. Marcação PDF/SVG melhora a semântica sem presumir PDF/UA. **Revisar quando:** novo pedido ou requisito exigir expansão.

## D014 — 2026-11-03 — Recursos e impacto de figuras pela AST

**Decisão:** conferir o Markdown composto com o mesmo leitor do Pandoc antes da incorporação e rastrear usos de figuras nessa AST. **Motivo:** imagens de revisão/contexto escapavam da checagem, e a comparação de edições ignorava alterações de figuras. **Consequência:** caminhos resolvidos precisam permanecer no material e no inventário; SVG não pode buscar recursos externos. Uso sem capítulo definido exige revisão conservadora explícita. **Revisar quando:** novos formatos ou sintaxes exigirem ajuste, mantendo validação antes de leitura e hashes completos.

## D015 — 2026-11-03 — Caso real escolhido e aceite honesto

**Decisão:** validar a matéria inteira Banco de Dados do Dataprev/FGV, Perfil 3, nos 17 itens do edital 001/2026. **Motivo:** escolha expressa do titular. **Consequência:** pedidos por texto e print de teste, pesquisa oficial, 17 capítulos e 49 questões; o print é renderização do edital pelo agente, não foto recebida do usuário. Aplicação das 17 skills e revisão editorial por IA são documentadas; AE-009 exige retorno real do leitor. **Revisar quando:** o retorno indicar falha ou uma nova seleção mudar o escopo.

## D016 — 2026-11-04 — Arquivos de provas, sumário extenso e prova futura

**Decisão:** identificar arquivos oficiais ZIP como download, mantendo PDF com salto de página; omitir itens individuais do sumário, preservando destinos de questões/resoluções e agrupamento por disciplina; admitir prova-alvo ainda não publicada apenas com consulta documentada e limitação. **Motivo:** a produção integral CRECI-ES revelou navegação enganosa de ZIP, excesso de entradas e rejeição indevida do estado previsto no esquema. **Consequência:** 143 testes locais, exportação dos dois materiais e auditorias dos arquivos finais; links externos seguem como observação datada. Itens reais continuam somente por acesso ao original sem permissão de reprodução confirmada. **Revisar quando:** nova banca usar outro tipo de arquivo ou o formato exigir outra organização, mantendo rotas e proveniência verificadas.

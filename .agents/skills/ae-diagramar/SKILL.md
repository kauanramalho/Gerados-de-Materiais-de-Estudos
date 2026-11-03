---
name: ae-diagramar
description: Montar apostilas e cadernos navegáveis em HTML e PDF.
version: 0.1.0
---

# Montar apostilas e cadernos navegáveis em HTML e PDF

## Quando usar

Após revisão de conteúdo ou para testar uma proposta visual.

## Entradas

Capítulos, questões, figuras, metadados e padrões visuais. Consulte AGENTS.md e as políticas em docs/ antes de executar.

## Procedimento

1. Organize capa, orientações, sumário, capítulos/questões, resoluções, glossário e referências conforme o tipo de material.
2. Atribua IDs persistentes, gere sumário clicável e todos os links questão → resolução → questão; inclua remissões à teoria.
3. Aplique hierarquia, margens, tipografia e quebras; evite separar dados essenciais, figuras e legendas. Em simulados, mantenha respostas separadas.
4. Exporte HTML e PDF com a ferramenta validada. O protótipo atual só gera examples/redes; para outros materiais, documente o comando usado e suas limitações.
5. Inspecione PDF, confira destinos e legibilidade, corrija falhas e gere manifesto de arquivos/versões.

## Saídas

HTML, PDF, manifesto e validação de navegação.

## Validação

Todos os links internos obrigatórios funcionam no arquivo final; páginas e figuras foram inspecionadas.

## Limites

Não inventar evidência, fontes, capacidades ou aprovação humana. Ausência de acesso deve ser registrada com seu efeito na entrega. Esta skill é uma instrução de projeto, não um serviço ou instalação global. Validação pedagógica em concurso real permanece pendente do piloto.

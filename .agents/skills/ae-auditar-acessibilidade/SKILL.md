---
name: ae-auditar-acessibilidade
description: Auditar teclado, descrições, contraste e estrutura dos artefatos, com limites explícitos.
version: 0.1.0
---

# Auditar teclado, descrições, contraste e estrutura dos artefatos, com limites explícitos.

## Quando usar

Em uma tarefa deste procedimento no Ateliê de Estudos, após ler o contexto e as políticas do projeto.

## Entradas

HTML/PDF final, figuras, descrições, fórmulas, tabelas e relatório de navegação.

## Procedimento

1. Leia AGENTS e docs/acessibilidade.md. Execute scripts/acessibilidade.py com HTML, PDF e --report; o resultado não é certificação WCAG ou PDF/UA.
2. Confira idioma, hierarquia, descrições de imagens e cabeçalhos de tabelas. Revise manualmente se as alternativas textuais transmitem a informação necessária à resolução.
3. Exercite teclado/foco, confira contrastes medidos e todas as rotas com audit_links.py. Fundos complexos e figuras exigem inspeção própria.
4. Confirme marcação estrutural do PDF, sequência de títulos e ausência de texto fora da página. Confira visualmente fórmulas, gráficos e a ordem de leitura em casos representativos.
5. Registre o que foi efetivamente testado e os limites de leitor de tela/semântica ainda não verificados. Corrija falhas detectadas e não declare conformidade integral a partir de tags ou aprovação estrutural.

## Saídas

Relatório com medidas, testes, correções e limitações por formato.

## Validação

Nenhuma informação essencial fica sem equivalente e as verificações executadas são reproduzíveis; limites não são ocultados.

## Limites

Procedimento local operado pelo agente, sem instalação global ou serviço permanente. Não inventar fontes, aprovação humana, equivalência de dificuldade, conformidade ou evidência. Conteúdo privado e originais ficam fora do Git público; preservar autoria por IA no Segundo Cérebro.

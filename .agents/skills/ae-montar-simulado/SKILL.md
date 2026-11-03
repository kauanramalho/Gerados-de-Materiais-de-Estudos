---
name: ae-montar-simulado
description: Montar, aplicar e pontuar um simulado com matriz e regras rastreáveis.
version: 0.1.0
---

# Montar, aplicar e pontuar um simulado com matriz e regras rastreáveis.

## Quando usar

Em uma tarefa deste procedimento no Ateliê de Estudos, após ler o contexto e as políticas do projeto.

## Entradas

Plano do simulado, manifesto, questões revisadas, perfil de banca e regras oficiais quando houver.

## Procedimento

1. Leia AGENTS e docs/simulados.md. Identifique objetivos e formato do pedido; use o mesmo fluxo de pesquisa do concurso.
2. Prepare simulado.json com ordem exata, distribuição por objetivo, duração, pesos e regras de acerto/erro/branco/anulação. Regra oficial exige fonte/hash e localizador; sem isso identificar treino autoral.
3. Execute build_material.py com --kind simulado --check e depois --pdf. Em pedido final, vincular pedido.json e acrescentar --final. O bloco de questões precede o gabarito em seção separada no mesmo PDF; não revelar respostas antes dele.
4. Confira folha de respostas, questões e comentários. Execute audit_links.py com --browser --external e acessibilidade.py; não presumir suporte a ligações entre PDFs separados.
5. Pontue respostas por IDs com scripts/simulado.py. Confira casos de erro, branco, pesos e anulação. Gabarito preliminar não sustenta pontuação oficial definitiva. Arquive plano, respostas, resultado e edição.

## Saídas

Simulado navegável, plano, folha de respostas, comentários e resultado de pontuação.

## Validação

Matriz e ordem correspondem às questões, cálculo reproduzível e respostas aparecem depois da prova.

## Limites

Procedimento local operado pelo agente, sem instalação global ou serviço permanente. Não inventar fontes, aprovação humana, equivalência de dificuldade, conformidade ou evidência. Conteúdo privado e originais ficam fora do Git público; preservar autoria por IA no Segundo Cérebro.

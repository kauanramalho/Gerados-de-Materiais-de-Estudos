---
name: ae-produzir-revisao
description: Produzir revisão curta com recuperação ativa e retorno às explicações.
version: 0.1.0
---

# Produzir revisão curta com recuperação ativa e retorno às explicações.

## Quando usar

Em uma tarefa deste procedimento no Ateliê de Estudos, após ler o contexto e as políticas do projeto.

## Entradas

Material já ensinado, objetivos, dificuldades do leitor e capítulos de revisão.

## Procedimento

1. Leia AGENTS e docs/revisao-aprendizagem.md. Escolha os objetivos já trabalhados; revisão pressupõe aprendizagem inicial e não substitui apostila completa.
2. Escreva perguntas de recuperação antes da síntese, relações essenciais, erros frequentes e exemplos breves. Condense sem remover condições que tornam o conceito correto.
3. Mapeie cada capítulo a arquivo curto em revisao.json, preservando os IDs de destino usados pelas questões. As remissões apontam para explicações dentro do PDF de revisão.
4. Gere com --kind revisao, valide cobertura do pedido com --final quando aplicável e audite todos os links. Compare extensão e legibilidade com a apostila.
5. Registre o que o leitor tentou recuperar e onde precisou voltar à explicação. Intervalos de retomada são sugestões ajustáveis; não prometer eficácia ou aprendizagem comprovada sem avaliação.

## Saídas

Revisão com perguntas, sínteses, prática comentada e remissões locais.

## Validação

Cada objetivo selecionado tem retomada e prática; o texto é mais breve sem criar falsas simplificações.

## Limites

Procedimento local operado pelo agente, sem instalação global ou serviço permanente. Não inventar fontes, aprovação humana, equivalência de dificuldade, conformidade ou evidência. Conteúdo privado e originais ficam fora do Git público; preservar autoria por IA no Segundo Cérebro.

# Revisão curta e recuperação ativa

`--kind revisao` usa o plano `revisao` do manifesto. Cada capítulo tem um arquivo de síntese próprio, preservando os IDs que as questões usam para retornar à explicação. A revisão pode ser lida no mesmo PDF: não há dependência de um link para volume separado.

A sequência é tentar recuperar uma resposta antes de consultar, conferir conceito e condições, resolver prática e interpretar o comentário. Resumo não substitui explicação inicial. A síntese deve conservar bases, hipóteses e limites, inclusive em fórmulas; concisão não autoriza generalização falsa. Retomadas em dias diferentes são sugestões ajustáveis ao desempenho, sem promessa de aprendizagem comprovada.

```sh
python scripts/build_material.py materials/matematica-basica/material.json --kind revisao --pdf
```

O exemplar de matemática mantém porcentagens, médias e probabilidade, com perguntas de recuperação, seis questões e comentários. Sua extensão é conferida frente à apostila; não existe cota fixa de páginas. O plano exige mapear todos os capítulos e preservar os destinos teóricos necessários. Antes de entregar, auditar links, teclado/descrições e conteúdo. Em pedido final, aplicar também `--final`.

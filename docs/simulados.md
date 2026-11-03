# Simulados e pontuação

O publicador aceita `--kind simulado`. O manifesto aponta `simulado` para um JSON com tempo, ordem dos IDs, distribuição por objetivo, pesos e regras. A ordem deve incluir cada questão exatamente uma vez e a matriz deve coincidir com os objetivos dos itens. O exemplo em [matemática](../materials/matematica-basica/simulado.json) é treino autoral, sem atribuição de banca.

O PDF contém aplicação/folha de respostas, prova e gabarito comentado em seção posterior, começando em outra página. Não há respostas do projeto no bloco da prova. Os links de questão ao comentário continuam disponíveis para consulta depois do treino; o sumário não revela a alternativa correta. O formato mantém tudo no mesmo arquivo e não presume ligações entre PDFs separados.

```sh
python scripts/build_material.py materials/matematica-basica/material.json --kind simulado --pdf
python scripts/simulado.py materials/matematica-basica/material.json --respostas materials/matematica-basica/respostas-exemplo.json --report build/pontuacao.json
```

Usar `--final` na publicação de um pedido de concurso com todas as condições de [cobertura](do-pedido-a-entrega.md). Plano com regra oficial exige fonte identificada, hash e localizador; conferir o edital/regulamento real. Gabarito preliminar não permite apresentar a pontuação como oficial definitiva. Um treino com itens autorais não é a prova oficial, ainda que use regras dela.

Respostas são um objeto JSON de ID para alternativa; ID ausente, null ou string vazia significa branco. IDs/alternativas desconhecidos são recusados. Acertos, erros e brancos recebem o valor do plano multiplicado pelo peso. Anulação pode creditar a todos ou excluir do máximo; registrar a regra pertinente. Se todas as questões forem excluídas, a porcentagem fica nula. O cálculo usa Decimal para acumulação, sem arredondar silenciosamente cada item.

O exemplo tem seis questões e tempo sugerido de 30 minutos: acerto 1, erro −0,25, branco 0, pesos unitários. As respostas de demonstração resultam em 3,75 de 6. Testes cobrem pesos, frações, branco, anulações, denominador zero e matriz/ordem inválidas. Essas regras são escolhas de treinamento e não caracterizam uma banca ou eficácia psicométrica.

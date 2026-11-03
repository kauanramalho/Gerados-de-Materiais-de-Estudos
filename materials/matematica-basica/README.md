# Piloto autoral de matemática

Três unidades de porcentagens, médias e probabilidade, seis questões autorais e dois diagramas originais. Demonstra fórmulas em MathML nativo e tabela com continuação, sem atribuição a edital ou banca. A seleção não altera prioridade de estudos do titular.

```sh
python scripts/build_material.py materials/matematica-basica/material.json --pdf
python scripts/build_material.py materials/matematica-basica/material.json --kind caderno --pdf
```

Resultados iniciais: apostila de 16 páginas, caderno de 9, seis pares questão/resolução por arquivo. Foram conferidos 41 links internos e 23 entradas de sumário na apostila, 30 links e 18 entradas no caderno. Sete fórmulas da apostila usam MathML sem JavaScript ou servidor remoto. A tabela tem trinta observações e cabeçalho repetido na continuação.

Os seis cálculos das respostas foram comparados em `tests/test_math_pilot.py`, incluindo enumeração de pares para a probabilidade. As páginas foram renderizadas e inspecionadas; isso não certifica aprendizagem ou PDF/UA. Fontes conceituais consultadas constam em `fontes.json`; redação, dados e figuras são próprios. A avaliação do leitor permanece pendente.

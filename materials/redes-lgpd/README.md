# Casos de impressão: equipamento e texto normativo

Demonstrador sem concurso/banca atribuídos. Dois capítulos, um esquema original detalhado e quatro questões autorais verificam rótulos de interfaces, explicação técnica, referência normativa, data de corte, exemplo resolvido e navegação. Não é prioridade pessoal escolhida pelo titular nem cobertura integral de redes ou LGPD.

Fontes consultadas em 03/11/2026: RFC 4188 (objeto dot1dTpFdbPort) e texto atualizado da Lei 13.709/2018 na Câmara dos Deputados (art.46 caput e §2º). Hashes, URLs e localizadores estão em fontes.json. A figura é genérica; modelos reais exigem manual correspondente. A explicação e as questões são originais.

```sh
python scripts/build_material.py materials/redes-lgpd/material.json --pdf
python scripts/build_material.py materials/redes-lgpd/material.json --kind caderno --pdf
```

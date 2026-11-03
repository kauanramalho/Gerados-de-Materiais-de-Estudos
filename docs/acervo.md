# Acervo de questões v0.3

O catálogo local usa SQLite, com importação de manifestos previamente validados. Não pesquisa a internet sozinho. O agente continua responsável por localizar provas oficiais, conferir status e direitos e preparar os registros. O primeiro catálogo contém 17 itens: 14 autorais e três reais por link, provenientes dos pilotos SQL e matemática.

## Uso

Instale `requirements-core.txt`. A partir da raiz:

```sh
python scripts/acervo.py --db build/acervo.sqlite importar materials/dataprev-sql/material.json
python scripts/acervo.py --db build/acervo.sqlite importar materials/matematica-basica/material.json
python scripts/acervo.py --db build/acervo.sqlite buscar --banca FGV --ano 2026 --assunto integridade --origem REAL
python scripts/acervo.py --db build/acervo.sqlite buscar --assunto probabilidade --origem AUTORAL
python scripts/acervo.py --db build/acervo.sqlite exportar --output build/acervo.json
```

Os filtros são combinados. Banca é comparada de forma exata após normalização de caixa/acentos; assunto é busca textual literal nos registros e contextos de cobertura, sem classificador automático. Autorais mantêm banca vazia, mesmo quando a referência editorial é FGV. Uma pesquisa sem resultado não prova ausência de questão relevante fora do catálogo.

## Identidade e deduplicação

Cada questão tem chave estável além do ID local `Q-AUT-001` ou `Q-REAL-001`, que pode se repetir em outros materiais. A ocorrência registra material, edição, ID local e revisão usada.

- **REAL:** banca, órgão, cargo, ano, caderno e número normalizados compõem a identidade. URLs alternativas e nova versão do gabarito não criam outra questão.
- **AUTORAL:** texto e alternativas geram a identidade; espaços e representação Unicode são normalizados, preservando caixa, números e operadores. Trocar `>` por `>=` cria outro item.
- **ADAPTADA:** origem mais o conteúdo adaptado compõem a identidade; evidência de permissão continua obrigatória.

Não há deduplicação semântica ou reconhecimento automático de cadernos equivalentes. Grafias diferentes de cargo podem exigir reconciliação editorial. Uma duplicata exata pode aparecer em vários materiais sem multiplicar o registro global.

## Edições e revisões

Material e versão identificam um conjunto de entradas com hash. Reimportar as mesmas entradas não duplica itens. Alterar arquivos de uma edição já registrada exige incrementar `version` no manifesto.

Se a identidade da questão permanecer e seus metadados, comentário ou resposta mudarem, a importação exige revisão explícita:

```sh
python scripts/acervo.py --db build/acervo.sqlite importar work/lote/material.json --aceitar-revisoes --motivo 'Fonte oficial novamente conferida e alteração documentada'
python scripts/acervo.py --db build/acervo.sqlite historico <id-estavel-retornado-na-busca>
```

O agente só usa essa opção após conferir a mudança. É uma proteção da ferramenta contra substituição silenciosa, não uma nova exigência de autorização humana para toda correção. A revisão anterior é preservada; ocorrências antigas continuam indicando qual revisão foi usada. Uma falha na importação desfaz as alterações daquele lote.

Evidência mais antiga não substitui a atual. Gabarito definitivo/retificado/anulado não regride para preliminar. Mudar resposta oficial exige hash de gabarito diferente e consistente com o registro de fontes. Esses controles não conseguem verificar, sem pesquisa, se um hash informado corresponde a um documento autêntico.

O histórico do catálogo não atualiza PDFs antigos automaticamente. Avaliar o impacto nos materiais e emitir nova edição/errata continua sendo uma entrega distinta, AE-020. Os testes de retificação usam fixtures identificadas, sem afirmar que a banca alterou suas respostas reais.

## Direitos, exportação e recuperação

Registros `somente-link` conservam metadados, resposta e comentário próprio, suprimindo enunciado e alternativas originais antes da gravação. O publicador mantém a mesma política. A exportação JSON contém questões atuais, materiais, ocorrências e histórico de revisões. Ela é uma saída de consulta/intercâmbio; importação reversa genérica de JSON não foi implementada.

O banco completo deve ser arquivado fora do Git e fora do cofre Obsidian. Para retomar, recupere esse arquivo SQLite. É possível reconstruir os itens dos manifestos disponíveis, mas reconstruir apenas as edições atuais não recupera revisões históricas perdidas. Confirme hashes e faça cópia de segurança antes de migrar bancos de outra versão. A versão de estrutura atual é 1; arquivos desconhecidos não são migrados nem sobrescritos silenciosamente.

O código não guarda caminhos absolutos privados no catálogo. Ainda assim, revise campos e conteúdo antes de compartilhar um banco ou JSON de trabalhos pessoais. A base pública do projeto contém os manifestos e ferramentas, não um acervo comercial de terceiros.

## Fechamento 0.5

O banco anterior foi preservado e ampliado para 21 itens ao importar redes/LGPD: 18 autorais e três reais por link. A edição 0.5 de matemática reutiliza as seis questões existentes. Novos formatos não atribuem banca às autorais. Arquivar banco/exportação fora do cofre e do Git público.

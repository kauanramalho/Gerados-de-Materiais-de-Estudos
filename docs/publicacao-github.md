# Publicar o pacote inicial

A conta foi identificada, mas a conexão atual devolveu 403 `Resource not accessible by integration` tanto para `createRepository` quanto para `POST /user/repos`. Isso é uma limitação de permissão da integração, não uma falha dos arquivos locais. Nenhum repositório remoto foi confirmado nesta tarefa.

## Quando houver permissão para criar

Na raiz do checkout, em um terminal autenticado com permissão de criação:

```sh
gh repo create kauanramalho/atelie-de-estudos --public --source=. --remote=origin --push
gh repo view kauanramalho/atelie-de-estudos --json url,visibility,defaultBranchRef
git rev-parse HEAD
git ls-remote origin refs/heads/main
```

## Quando o titular criar o repositório vazio

Criar `atelie-de-estudos` público, sem README/licença/.gitignore automáticos, e conceder à integração acesso ao novo repositório se sua seleção for restrita. Depois, na raiz do checkout:

```sh
git remote add origin https://github.com/kauanramalho/atelie-de-estudos.git
git push -u origin main
```

Os comandos pressupõem que não exista `origin`; conferir `git remote -v` antes. Se o repositório remoto já contiver arquivos, buscar e reconciliar os históricos, sem force push.

## Recuperar o histórico do pacote

O ZIP contém os arquivos públicos. O arquivo `.bundle`, entregue separadamente, preserva o histórico Git:

```sh
git clone atelie-de-estudos.bundle atelie-de-estudos
cd atelie-de-estudos
python scripts/check.py
python -m unittest discover -s tests -v
```

Antes do push: revisar diff, arquivos rastreados, histórico, `.gitignore` e direitos. Depois: confirmar visibilidade pública, branch e SHA remoto; conferir a execução da CI antes de declará-la aprovada. Atualizar Progress e o cofre somente com os resultados observados. O destino nos comandos é pretendido; este documento não prova que ele exista.

# Dessik — loja fictícia

Projeto acadêmico completo com cadastro, login, autenticação JWT, catálogo vindo do MySQL, CRUD administrativo, pedidos com atualização transacional de estoque e integração com ViaCEP. Compras são simulações: não há pagamento nem entrega.

O front-end usa somente HTML5, CSS3 e JavaScript puro com `fetch()`. O back-end é Python com FastAPI e `mysql-connector-python`. Não há React, Node obrigatório, SQLite ou Docker obrigatório.

**Comece pela etapa 11 para executar.** O documento [PROJETO_COMPLETO.md](docs/PROJETO_COMPLETO.md) reúne estas 14 etapas e o conteúdo integral dos arquivos para copiar ou apresentar.

## ETAPA 1 — Visão geral

```text
Navegador (HTML + CSS + JavaScript)
             | fetch, JSON e Authorization: Bearer JWT
             v
Vercel: arquivos públicos + FastAPI em /api/*
             | consultas parametrizadas e transações
             v
MySQL remoto (usuários, produtos, pedidos e itens)

GET /api/cep/{cep} -> FastAPI -> ViaCEP -> endereço em JSON
```

Localmente, o Uvicorn serve a API e os mesmos arquivos públicos em uma única origem. Senhas recebem hash bcrypt com salt; tokens expiram; a permissão administrativa é lida no banco a cada operação protegida.

## ETAPA 2 — Estrutura de pastas

```text
Dessik/
├── api/
│   ├── __init__.py
│   └── index.py
├── backend/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── auth.py
│   ├── schemas.py
│   ├── security.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── usuarios.py
│   │   ├── produtos.py
│   │   ├── pedidos.py
│   │   └── cep.py
│   └── services/
│       ├── __init__.py
│       └── password_generator.py
├── public/
│   ├── index.html
│   ├── loja.html
│   ├── cadastro.html
│   ├── login.html
│   ├── admin.html
│   ├── css/style.css
│   ├── js/
│   │   ├── api.js
│   │   ├── cadastro.js
│   │   ├── login.js
│   │   ├── loja.js
│   │   └── admin.js
│   └── images/placeholder.svg
├── database/
│   ├── schema.sql
│   └── dados.sql
├── scripts/
│   ├── __init__.py
│   ├── init_db.py
│   ├── admin.py
│   └── export_guide.py
├── tests/
│   ├── conftest.py
│   ├── test_security.py
│   ├── test_cep.py
│   ├── test_frontend.py
│   └── test_mysql.py
├── docs/
│   ├── PROJETO_COMPLETO.md
│   └── VALIDACAO.md
├── .env.example
├── .gitignore
├── .vercelignore
├── requirements.txt
├── requirements-dev.txt
├── requirements-lock.txt
├── pyproject.toml
├── vercel.json
└── README.md
```

`public/` substitui a pasta `frontend/` sugerida no enunciado para que a Vercel sirva os arquivos estáticos diretamente. Não existe duplicação de builds nem etapa JavaScript. `schemas.py` representa e valida a entrada; usamos SQL parametrizado, então não precisamos de modelos ORM. Cadastro e login ficam juntos em `usuarios.py`.

## ETAPA 3 — Banco de dados

O DDL completo está em [database/schema.sql](database/schema.sql). As oito amostras fictícias estão em [database/dados.sql](database/dados.sql): notebook, mouse, teclado, monitor, headset, webcam, SSD e RAM. A webcam começa sem estoque para demonstrar o botão indisponível.

Use MySQL 8.0.16+ com InnoDB ou serviço compatível com transações, bloqueio `FOR UPDATE` e chaves estrangeiras. Os valores monetários são `DECIMAL`, não `FLOAT`. O pedido armazena o preço unitário vigente, preservando o valor histórico mesmo que o administrador altere o preço depois.

Crie o banco no painel do provedor ou, em um servidor próprio, no Workbench:

```sql
CREATE DATABASE loja_ficticia CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE loja_ficticia;
```

Depois abra e execute `schema.sql`, seguido de `dados.sql`, com o banco selecionado. Alternativamente, configure `.env` e execute `python -m scripts.init_db`: ele executa ambos no banco informado em `DB_NAME`. Não precisa conceder `CREATE DATABASE` à aplicação na nuvem.

O script não apaga tabelas e a carga de demonstração não redefine produtos já existentes com os mesmos IDs. Execute a massa em banco novo; não é uma ferramenta de migração para schemas anteriores. DDL MySQL pode provocar commit implícito. Não há criação de tabela automática em cada requisição ou deploy.

Não há senha padrão ou usuário administrador embutido. Um usuário com pedidos não pode ser excluído por causa da FK. Produtos com pedidos retornam HTTP 409 na exclusão: zere o estoque se quiser interromper as vendas sem perder o histórico.

As imagens iniciais são placeholders locais identificados como ilustrativos, sem dependência de serviço externo. Para usar fotos próprias, coloque os arquivos em `public/images/` e altere `imagem_url` para `/images/nome.webp` no administrador. Também é aceita URL HTTPS. Use imagens com autorização de uso.

## ETAPA 4 — Back-End

- `config.py`: lê `.env`, exige segredo JWT forte e exige banco remoto com TLS em produção.
- `database.py`: única fábrica de conexões e contexto de transação. Commita ao concluir, desfaz em caso de erro e sempre fecha os recursos.
- `schemas.py`: valida e-mail, nomes, senhas coincidentes, CEP, UF, preço, estoque e quantidades. Campos extras são rejeitados, inclusive `is_admin` no cadastro.
- `security.py`: bcrypt com salt e JWT HS256 com expiração, emissor e audiência.
- `auth.py`: valida Bearer, assinatura e prazo do token; consulta a conta e suas permissões.
- `services/password_generator.py`: gera senha de 16 caracteres com `secrets`, contendo minúsculas, maiúsculas, números e símbolos.

O bcrypt tem limite de 72 **bytes**; a API rejeita senhas acima disso em vez de truncá-las. O mínimo no cadastro é de 8 caracteres. Não se registra senha ou token nos logs. Erros de validação omitem a entrada enviada.

As consultas usam parâmetros `%s` e tuplas separadas. O driver transmite o dado como valor, impedindo que um e-mail ou nome seja interpretado como comando SQL. Consultas nunca concatenam a entrada do usuário.

## ETAPA 5 — API REST

| Método | Endpoint | Função | Acesso |
|---|---|---|---|
| GET | `/api/health` | Verificar API (não consulta o banco) | Público |
| POST | `/api/cadastro` | Cadastrar cliente | Público |
| POST | `/api/login` | Emitir JWT | Público |
| GET | `/api/me` | Consultar conta autenticada | Cliente/Admin |
| GET | `/api/gerar-senha` | Sugerir senha forte | Público |
| GET | `/api/produtos` | Listar catálogo | Público |
| GET | `/api/produtos/{id}` | Consultar um produto | Público |
| POST | `/api/produtos` | Criar produto | Admin |
| PUT | `/api/produtos/{id}` | Substituir dados do produto | Admin |
| DELETE | `/api/produtos/{id}` | Excluir produto sem pedidos | Admin |
| POST | `/api/pedidos` | Simular compra | Cliente/Admin |
| GET | `/api/pedidos` | Últimos 100 pedidos da própria conta | Cliente/Admin |
| GET | `/api/cep/{cep}` | Consultar ViaCEP | Público |
| GET | `/api/docs` | Swagger interativo | Público |
| GET | `/api/openapi.json` | Contrato OpenAPI | Público |

Produtos aceitam `?limite=12&offset=0` (limite de 1 a 100). O front-end pagina o catálogo e a tabela administrativa. O preço na resposta é uma string decimal como `"129.90"`. O JavaScript a formata como moeda; o cálculo oficial sempre é feito no servidor.

Pedidos aceitam até 50 produtos diferentes e quantidades inteiras de 1 a 1.000 por item. Produtos duplicados devem ser agrupados. A interface simula um produto por vez; a API também suporta vários produtos. O cliente não envia o valor a pagar nem o ID do usuário. Esses dados vêm do banco e do JWT.

O servidor bloqueia os produtos por ordem de ID com `SELECT ... FOR UPDATE`, valida todas as disponibilidades, grava pedido e itens e reduz o estoque na mesma transação. Se qualquer etapa falhar, ocorre rollback. Há também atualização condicional e restrição de estoque não negativo. Deadlock ou timeout de bloqueio retorna 409 para uma nova tentativa consciente do usuário.

Respostas usam 200/201 no sucesso, 401 para autenticação inválida, 403 para permissão insuficiente, 404 para recursos inexistentes, 409 para conflitos, 422 para dados inválidos, 502 para erro no ViaCEP, 503 para falha de banco e 500 para falha inesperada. Mensagens não expõem credenciais nem SQL.

## ETAPA 6 — Front-End

Abra `http://127.0.0.1:8000/` com o servidor iniciado; não dê duplo clique no HTML. Os scripts são módulos JavaScript separados e usam caminhos da mesma origem. O catálogo é montado a partir de `GET /api/produtos`, sem produtos fixos no HTML.

O navegador mantém o JWT em `sessionStorage` durante a sessão da aba. `api.js` inclui `Authorization: Bearer ...` nas operações protegidas. Sair remove o token local. Se ele vencer, a API retorna 401 e a sessão é removida; entre novamente. Fechar a aba normalmente encerra esse armazenamento, sujeito ao recurso de restauração de sessão do navegador.

Esse armazenamento pode ser acessado por JavaScript: uma falha XSS pode expor o token. Aqui os textos são inseridos por `textContent`, as imagens são validadas e há CSP. Em um sistema profissional, cookies `HttpOnly`, `Secure`, `SameSite` com proteção CSRF e revogação/renovação de sessão merecem consideração. Logout local não revoga um JWT já copiado, que permanece válido até expirar. O projeto não implementa rate limiting distribuído; para publicação aberta, configure regras de limitação no provedor para login e cadastro.

Na loja, escolha uma quantidade, clique em Comprar e confirme a simulação. O total devolvido pelo servidor é o definitivo. Após a compra, os cards são recarregados. Em indisponibilidade do banco, aparece um erro real; não há catálogo falso de fallback. Botões desativados evitam cliques repetidos durante uma requisição, mas a API não oferece idempotência: se houver perda da resposta, consulte `GET /api/pedidos` antes de repetir a compra.

Os campos de endereço são opcionais. O botão Consultar CEP chama nossa API, que consulta ViaCEP com timeout de 5 segundos. Erros permitem preenchimento manual. Conforme o [contrato do ViaCEP](https://viacep.com.br/), CEP inexistente é identificado por `erro` na resposta. Evite consultas em massa.

## ETAPA 7 — Variáveis de ambiente

Copie `.env.example` para `.env`. Nunca publique o arquivo real.

| Variável | Conteúdo |
|---|---|
| `APP_ENV` | `development` local, `production` na Vercel |
| `DB_HOST` | Host fornecido pelo provedor |
| `DB_PORT` | Porta do provedor, normalmente 3306 ou 4000 |
| `DB_USER` | Usuário do banco |
| `DB_PASSWORD` | Senha do banco |
| `DB_NAME` | Nome do banco previamente criado |
| `DB_SSL` | `true` remoto; `false` somente em desenvolvimento local |
| `DB_SSL_CA` | Caminho opcional do certificado CA PEM |
| `JWT_SECRET` | Chave aleatória, no mínimo 32 bytes |
| `JWT_ALGORITHM` | `HS256`, único algoritmo aceito |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 60 por padrão; de 1 a 1.440 |
| `CORS_ORIGINS` | Vazio para mesma origem; origens extras separadas por vírgula |

Gere a chave, copie a saída para `JWT_SECRET` e guarde-a somente no `.env` e na Vercel:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Coloque entre aspas valores que contenham caracteres especiais para o formato `.env`, por exemplo `DB_PASSWORD="valor fornecido pelo provedor"`. A aplicação passa os campos separadamente ao driver, sem montar uma URL que exija escapar a senha.

Na mesma origem, deixe `CORS_ORIGINS` vazio. Se usar um servidor estático separado, informe a origem exata, como `http://127.0.0.1:5500`, e adapte o endereço base de `api.js` e o `connect-src` da CSP desse servidor. `localhost` e `127.0.0.1` são origens diferentes. CORS não substitui autenticação. `*` é rejeitado pela configuração.

## ETAPA 8 — Dependências

`requirements.txt` fixa as bibliotecas diretas usadas na aplicação. `requirements-dev.txt` acrescenta pytest. `requirements-lock.txt` registra todas as versões do ambiente validado, inclusive transitivas; pode ser usado para reproduzir esse ambiente com `pip install -r requirements-lock.txt`. Python 3.13 foi usado na validação.

```bash
python -m pip install -r requirements.txt
```

Não é necessário instalar Node, framework de CSS ou compilador front-end.

## ETAPA 9 — Configuração Vercel

`api/index.py` exporta `app`. `pyproject.toml` declara explicitamente `entrypoint = "api.index:app"`. `vercel.json` seleciona FastAPI, define duração de 30 segundos e cabeçalhos. `public/` é servido como arquivos estáticos. Localmente esse diretório é montado apenas quando `VERCEL` não é `1`.

A configuração segue o [suporte atual de FastAPI da Vercel](https://vercel.com/docs/frameworks/backend/fastapi), consultado em 08/09/2026. Não usa builders legados `@vercel/python`, runtimes inventados ou reescrita geral que converta endpoints em HTML. A raiz do projeto na Vercel deve ser a pasta que contém `pyproject.toml` e `vercel.json`.

## ETAPA 10 — Testes

Inicie o servidor e acesse `/api/docs`. Execute o login, copie `access_token`, clique em **Authorize** e cole somente o token. O Swagger envia o cabeçalho Bearer automaticamente.

### Cadastro — POST /api/cadastro

```json
{
  "nome": "João Silva",
  "email": "joao@example.com",
  "senha": "Senha123!",
  "confirmar_senha": "Senha123!",
  "cep": "01001000",
  "logradouro": "Praça da Sé",
  "bairro": "Sé",
  "cidade": "São Paulo",
  "estado": "SP"
}
```

As senhas acima são exemplos de teste. Em uma conta de uso real, use o gerador. Repetir o e-mail deve retornar 409; senha divergente, campo faltando ou tentativa de enviar `is_admin` deve retornar 422.

### Login — POST /api/login

```json
{"email": "joao@example.com", "senha": "Senha123!"}
```

Espera-se `access_token` e `token_type: "bearer"`. Senha incorreta deve retornar 401. `GET /api/me` com o token deve mostrar `is_admin: false` inicialmente.

### Criar produto — POST /api/produtos

Após promover a conta pelo comando da etapa 11:

```json
{
  "nome": "Mouse de teste",
  "descricao": "Mouse para testar o CRUD.",
  "categoria": "Periféricos",
  "preco": "99.90",
  "quantidade_estoque": 10,
  "imagem_url": "/images/placeholder.svg"
}
```

Anote o `id_produto` retornado. Use `GET /api/produtos/{id}` para consultar. Use `PUT /api/produtos/{id}` com o mesmo JSON e preço `"89.90"` para alterar. PUT exige todos os campos. Para excluir, use DELETE no ID antes de fazer pedidos. Um cliente comum recebe 403 em todas as mutações.

### Fazer pedido — POST /api/pedidos

```json
{"itens": [{"id_produto": 2, "quantidade": 3}]}
```

Troque `2` pelo ID desejado. A resposta 201 traz `id_pedido`, `valor_total` e mensagem de simulação. Se havia 10 unidades, ficam 7. Verifique em `GET /api/produtos/{id}`. Quantidade 0, negativa, fracionária ou item duplicado gera 422. Acima do estoque gera 409. Sem token gera 401. `GET /api/pedidos` lista somente os pedidos da conta autenticada.

### Testes automatizados

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Testes unitários e HTTP não precisam de banco. Os testes de integração são pulados se não houver autorização explícita pela variável abaixo. Para executá-los, crie **outro banco**, chamado `dessik_test`, configure as variáveis DB para ele e inicialize suas tabelas:

```powershell
$env:DB_NAME = "dessik_test"
# Configure também DB_HOST, DB_PORT, DB_USER, DB_PASSWORD e DB_SSL para o banco de teste.
python -m scripts.init_db
$env:RUN_MYSQL_TESTS = "1"
python -m pytest -q
Remove-Item Env:RUN_MYSQL_TESTS
Remove-Item Env:DB_NAME
```

O banco de teste deve terminar em `_test`. Os testes criam contas e produtos exclusivos e preservam os dados para inspeção; não use o banco real da loja. A integração verifica cadastro, duplicidade, login, hash, CRUD, FK, SQL injection como dado, rollback de pedido inválido e disputa de duas compras pela última unidade.

## ETAPA 11 — Executar localmente, do início

1. Instale Python 3.13 em [python.org](https://www.python.org/downloads/) e habilite o acesso pelo terminal. Verifique `python --version`.
2. Instale MySQL Server 8.0.16+ ou use banco remoto compatível. **Workbench é um cliente e não substitui o servidor.** Crie o banco conforme a etapa 3. Reserve um usuário da aplicação, evitando usar root na produção.
3. Baixe/clône este repositório ou abra esta pasta no VS Code. Abra o terminal **na raiz do projeto**, onde está `requirements.txt`.
4. Crie e ative o ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Se a política do PowerShell impedir ativar, não precisa alterá-la: substitua `python` por `.\.venv\Scripts\python.exe` nos comandos seguintes. No Prompt de Comando, use `.venv\Scripts\activate.bat`. No Linux/macOS, use `source .venv/bin/activate`.

5. Instale as dependências e crie `.env`:

```powershell
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

No Linux/macOS: `cp .env.example .env`. Se `.env` já existe, edite-o; não sobrescreva suas credenciais.

6. Preencha `.env` com o banco. Localmente, `DB_HOST=127.0.0.1`, porta configurada e `DB_SSL=false` são permitidos com `APP_ENV=development`. No banco remoto use o host real, a porta do provedor e `DB_SSL=true`. Gere `JWT_SECRET` com o comando da etapa 7.
7. Execute o SQL no Workbench, com o banco selecionado, ou use:

```bash
python -m scripts.init_db
```

8. Inicie a aplicação:

```bash
python -m uvicorn api.index:app --reload
```

9. Abra [a loja local](http://127.0.0.1:8000/loja.html). A documentação interativa está em [Swagger](http://127.0.0.1:8000/api/docs).
10. Clique em Criar conta. Teste Sugerir senha e Consultar CEP. Guarde a senha e conclua o cadastro.
11. Faça login. Consulte produtos, escolha quantidade e confirme uma compra. Confira a redução do estoque.
12. Para administrar, abra outro terminal com o mesmo ambiente, na raiz, e promova **a conta que você acabou de cadastrar**:

```bash
python -m scripts.admin joao@example.com
```

13. Atualize a loja e abra Administração no menu. Cadastre, edite e exclua um produto de teste. Não há endpoint público de promoção: o comando depende de acesso autorizado ao banco.
14. Confira os testes da etapa 10. Para encerrar o servidor, use `Ctrl+C`.

## ETAPA 12 — Banco na nuvem e serverless

Escolha um serviço **MySQL compatível**, por exemplo TiDB Cloud Starter. A [página oficial de preços](https://www.pingcap.com/pricing/) e a [página do Starter](https://www.pingcap.com/tidb-cloud-starter/) apresentavam uma opção gratuita em 08/09/2026. Verifique os limites, regiões e exigências de conta no momento da contratação; não se promete gratuidade permanente. Não foram presumidos planos atuais de Clever Cloud, FreeDB ou db4free.

No painel do serviço, crie uma instância e copie host, porta, usuário, senha e nome do banco para o `.env` e, depois, para a Vercel. Utilize o endereço público ou a conectividade suportada pelo provedor e autorize somente o acesso necessário. A Vercel não consegue acessar o MySQL do seu computador por `localhost`.

No TiDB, use as instruções de conexão geradas pelo próprio painel e mantenha TLS ativo. Veja a [documentação de TLS do TiDB Cloud](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters/). A aplicação verifica tanto a cadeia de certificados quanto o hostname. Se a CA estiver na confiança do sistema, `DB_SSL_CA` pode ficar vazio; se o provedor exigir uma CA própria, configure seu arquivo PEM. Não desative a verificação para contornar erros.

Se precisar de CA própria na Vercel, inclua **somente o certificado público CA** em uma pasta versionada, como `database/ca.pem`, e configure `DB_SSL_CA=database/ca.pem`. Nunca inclua chaves privadas. A pasta `certs/` é ignorada por padrão e serve apenas para uso local.

O DDL foi direcionado a InnoDB/MySQL. Serviços compatíveis podem ter diferenças de versão no suporte/enforcement de CHECK e FKs; habilite o suporte quando necessário, confira a documentação da versão e execute os testes de integração antes de usar o serviço. A validação e a atualização condicional no servidor protegem o estoque além das restrições do schema.

Serverless significa que várias execuções podem começar simultaneamente. Cada transação abre uma conexão curta e a fecha ao terminar; não existe conexão global permanente. Ainda assim, muitas requisições simultâneas podem atingir o limite de conexões do plano. Ajuste concorrência e limites no provedor, monitore os erros e considere proxy/pool gerenciado se o projeto crescer.

O cold start pode aumentar a latência da primeira chamada. As funções têm limites de duração, memória e tamanho; não mantenha tarefas longas, estado importante ou arquivos mutáveis no disco da função. O MySQL remoto é a fonte persistente dos dados.

## ETAPA 13 — Deploy na Vercel

1. Crie um repositório no GitHub e envie estes arquivos. Use GitHub Desktop ou Git. `.env`, `.venv` e `.local` devem ficar fora do commit. Se já publicou um segredo, removê-lo do arquivo não basta: troque a credencial.
2. Crie/configure o banco remoto e execute `schema.sql` e `dados.sql` nele. Não execute seed automático em todo deploy.
3. Na Vercel, escolha **Add New → Project** e importe o repositório. Selecione a raiz do projeto e o preset FastAPI, se não for detectado.
4. Deixe instalação/build/output nos padrões do preset, respeitando os arquivos deste repositório. Não selecione `public` como raiz do projeto, pois isso excluiria o backend.
5. Em **Settings → Environment Variables**, adicione **individualmente** `APP_ENV=production`, `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_SSL=true`, `JWT_SECRET`, `JWT_ALGORITHM=HS256`, `ACCESS_TOKEN_EXPIRE_MINUTES=60`. Adicione `DB_SSL_CA` apenas se necessário. Deixe `CORS_ORIGINS` vazio para a mesma origem.
6. Selecione os ambientes desejados (Production e, se for testar previews, Preview). Prefira bancos separados para produção e preview. Não copie o `.env` para `public/`.
7. Clique em **Deploy**. Se mudar variáveis depois, faça um novo deploy para aplicá-las.
8. Abra `/api/health`, `/api/produtos`, `/loja.html`, `/cadastro.html` e `/login.html`. O health valida que a função respondeu; produtos confirma a conexão real com o banco.
9. Cadastre uma conta de teste e faça uma compra. Promova a conta necessária via `python -m scripts.admin seu@email.com` em um ambiente autorizado conectado ao banco remoto. Teste CRUD e restrições com outra conta comum.
10. Em falhas, consulte Build Logs e Runtime Logs no painel. Não cole senhas ou tokens em capturas públicas.

| Sintoma | Verificação |
|---|---|
| Configuração JWT inválida | Chave preenchida, algoritmo HS256 e novo deploy |
| HTTP 503 em produtos | Host, porta, usuário, senha, DB_NAME, rede e TLS |
| Tabela inexistente | Execute os dois scripts SQL no banco correto |
| Erro de certificado | CA correta e hostname do certificado; não desative TLS |
| HTTP 401 | Faça login novamente e envie Bearer válido |
| HTTP 403 | Confira `is_admin` pelo comando de promoção |
| HTTP 409 ao excluir | Produto já aparece em pedido; mantenha o histórico |
| 404 na raiz | Confira preset FastAPI, raiz do repositório e pasta public |
| CEP não preenche | Verifique formato e conectividade com ViaCEP; preencha manualmente |

O projeto entrega a configuração e o tutorial de deploy. A publicação real exige a sua conta Vercel e credenciais de um banco remoto; esses recursos não são criados nem inventados pelo código.

## ETAPA 14 — Explicação para apresentação

“Este projeto é uma loja fictícia de tecnologia. A interface é feita com HTML e CSS, e o JavaScript usa `fetch` para enviar requisições à API em Python.

API REST é um conjunto de endereços que permite trabalhar com recursos. GET consulta, POST cria, PUT atualiza e DELETE exclui. JSON é o formato usado para transportar os campos, como nome e quantidade.

O FastAPI recebe esses dados e valida o conteúdo antes de executar a regra. Depois, o conector MySQL executa consultas parametrizadas. Assim, a entrada do usuário é tratada como dado e não como comando SQL.

No cadastro, a senha passa pelo bcrypt, que gera um hash com salt. O banco guarda esse hash, não a senha. No login, o bcrypt verifica se a senha digitada corresponde ao hash. Se corresponder, a API emite um JWT assinado e com prazo de validade.

O navegador guarda esse token temporariamente e o envia no cabeçalho Authorization. A API valida o token e consulta a conta. Para cadastrar, editar ou excluir produtos, ela também verifica se a conta é administradora.

O catálogo vem do banco. Na compra simulada, o servidor verifica e bloqueia os produtos, registra o pedido e seus itens e reduz o estoque numa transação. Se uma parte falhar, tudo é desfeito. Isso impede pedido pela metade e evita vender a mesma última unidade duas vezes.

O CEP demonstra a integração entre sistemas: o navegador chama nossa API, nossa API consulta o ViaCEP e o endereço volta em JSON para preencher o formulário.

Na publicação, a Vercel entrega as páginas e executa o Python. O banco fica em outro serviço acessível com TLS. Assim, a aplicação pode reiniciar sem perder os dados. Não há cobrança real: o objetivo é demonstrar a comunicação completa entre interface, API e banco.”

# Dessik — loja virtual acadêmica

Esta é a entrega correspondente ao pedido: HTML, CSS e JavaScript puro, FastAPI e MySQL, com carrinho, estoque, pedidos, cadastro, login, ViaCEP e CRUD administrativo. Compras são simulações, sem pagamento ou entrega.

Os arquivos anteriores na raiz do repositório foram preservados. **Para estudar e executar esta versão, use somente `workspace/`.** Não misture seu schema com o banco da versão anterior: esta entrega usa `tipo_usuario` (`cliente` ou `admin`).

```text
workspace/
├── publico/                 # Páginas, CSS, JavaScript e imagens
│   ├── index.html
│   ├── cadastro.html
│   ├── login.html
│   ├── loja.html
│   ├── carrinho.html
│   ├── admin.html
│   ├── pedidos.html         # Histórico do próprio usuário
│   ├── css/
│   ├── js/
│   ├── imagens/
│   └── README.md
├── privada/
│   ├── api/index.py         # Entrada da Vercel
│   ├── backend/
│   │   ├── main.py          # Rotas da API
│   │   ├── database.py      # Configuração, conexão e transação
│   │   ├── auth.py          # bcrypt, JWT e permissão de admin
│   │   ├── models.py        # Converte preço para JSON, sem ORM
│   │   └── schemas.py       # Valida os dados recebidos
│   ├── database/schema.sql
│   ├── database/dados.sql
│   ├── tests/
│   ├── .env.example
│   ├── requirements.txt
│   ├── vercel.json
│   └── README.md
└── CODIGO_COMPLETO.md       # Código textual integral, arquivo por arquivo
```

Comece pelo [guia do back-end](privada/README.md) para configurar o MySQL e executar a loja. Depois leia o [guia do front-end](publico/README.md).

## Como as partes conversam

1. O navegador abre um HTML e executa JavaScript.
2. `fetch()` pede os produtos à API.
3. FastAPI executa um SELECT parametrizado no MySQL.
4. O banco devolve os dados e a API os envia como JSON.
5. JavaScript cria os cards usando `textContent`.

JSON é um formato de texto para transportar informações. Exemplo: `{"id_produto":2,"quantidade":1}`. Ele não protege dados sozinho; autenticação, validação e HTTPS têm esse papel.

No carrinho, o navegador guarda somente IDs e quantidades em `sessionStorage`. Os itens sobrevivem à navegação na mesma aba. Fechar a aba encerra esse armazenamento. O carrinho não reserva estoque.

Ao finalizar, a API identifica o usuário pelo JWT, consulta os preços e bloqueia as linhas dos produtos com `FOR UPDATE`. Ela cria o pedido, insere os itens e reduz o estoque na mesma transação. Se faltar um produto ou estoque, ocorre `rollback`: nenhuma parte da compra fica registrada. Valores monetários usam `Decimal`, evitando erros de centavos no Python.

## COMO APRESENTAR O PROJETO

“Criei a Dessik como uma loja fictícia para estudar desenvolvimento web.”

“O front-end usa HTML para estruturar, CSS para estilizar e JavaScript para interagir. Não usei frameworks no navegador.”

“O JavaScript usa fetch para conversar com minha API FastAPI. Os produtos vêm do MySQL em JSON; não estão escritos no HTML.”

“Minha API tem funções pequenas e SQL visível. O schema mostra as quatro tabelas e suas relações.”

“O carrinho junta produtos. Na compra, o servidor consulta os preços verdadeiros e verifica o estoque antes de salvar tudo.”

“Usei bcrypt para proteger senhas, JWT com expiração, variáveis de ambiente e queries parametrizadas. Esconder um botão de admin não basta: o servidor também verifica a permissão.”

“A transação impede que uma compra fique pela metade. Os bloqueios também impedem duas pessoas de comprar a mesma última unidade.”

## Roteiro de demonstração e testes funcionais

| Passo | Ação | Resultado esperado |
| --- | --- | --- |
| 1 | Abrir a página inicial | Marca Dessik, apresentação, destaques e benefícios |
| 2 | Abrir cadastro, informar nome e e-mail válidos | Formulário organizado |
| 3 | Informar CEP `01001000` e sair do campo | Endereço preenchido pelo ViaCEP; pode corrigir manualmente |
| 4 | Sugerir senha, guardar e cadastrar | Conta criada; redirecionamento para login |
| 5 | Fazer login | Sessão iniciada, saudação e botão Sair |
| 6 | Abrir loja e buscar Mouse | Produtos da API; categoria e preço visíveis |
| 7 | Filtrar Acessórios | Apenas produtos da categoria |
| 8 | Ver Hub e Webcam | Aviso de estoque baixo e botão desabilitado no esgotado |
| 9 | Comprar Mouse (2) e Teclado (1) | Mensagem de item adicionado; nenhuma compra registrada ainda |
| 10 | Abrir carrinho, mudar quantidade e remover um item | Subtotal e total atualizados |
| 11 | Finalizar pedido | Número do pedido, total do servidor e carrinho vazio |
| 12 | Voltar à loja e atualizar | Estoque reduzido pela quantidade comprada |
| 13 | Abrir Meus pedidos | Somente pedidos do usuário atual |
| 14 | Promover sua conta conforme o README privado | Papel admin no banco |
| 15 | Entrar em Administração e criar produto temporário | Novo produto aparece no catálogo |
| 16 | Editar preço/estoque e excluir esse produto | CRUD completo; exclusão pede confirmação |
| 17 | Mostrar as tabelas no MySQL Workbench | Relacionamento entre usuários, pedidos e itens |
| 18 | Mostrar auth.py, SQL parametrizado e .gitignore | Explicar as proteções de segurança |

Produto que já pertence a um pedido não pode ser excluído: a API retorna 409 para preservar o histórico. Para retirá-lo de venda, ajuste seu estoque para zero.

## Testes seguros de Cybersecurity

Faça estes testes apenas nesta aplicação local, com dados fictícios.

| Teste | Resultado esperado |
| --- | --- |
| POST/PUT/DELETE de produto sem JWT | 401 |
| DELETE com JWT de cliente | 403 |
| Produto com estoque `-1`, autenticado como admin | 422 |
| Cadastro com e-mail `invalido` | 422 sem ecoar a senha |
| Cadastro incluindo `tipo_usuario: "admin"` | 422; cadastro público não escolhe papel |
| JWT adulterado ou expirado | 401 |
| Pedido com quantidade negativa ou produto repetido | 422 |
| Pedido contendo um campo `preco` | 422; cliente só envia IDs e quantidades |
| Dois pedidos para uma última unidade | Um sucesso e um conflito; estoque termina em zero |
| Conferir `senha_hash` no banco de teste | Hash bcrypt, nunca senha legível |
| GET `/.env` ou `/privada/.env` | 404 |
| Parar banco de teste e consultar produtos | 503 com mensagem genérica |
| `git check-ignore privada/.env` a partir de workspace | Caminho listado como ignorado |
| `git ls-files -- privada/.env` | Nenhuma saída; arquivo não rastreado |

Os testes automatizados ficam em `privada/tests/`. Leia as instruções antes de habilitar testes de integração; eles criam dados e exigem banco isolado terminado em `_test`.

## Limites e validação da entrega

API: 43 testes passaram, incluindo integração com banco, compra de vários itens, rejeição de preço adulterado e concorrência. O teste de navegador foi executado separadamente: fluxo real de cadastro, login, criação administrativa, carrinho e compra passou em Edge headless. As seis páginas principais foram verificadas sem rolagem horizontal em larguras de 390 e 768 pixels. A página inicial também foi inspecionada por captura em 1440 pixels.

O ambiente local fornecia **MariaDB 11.4**, usado nos testes via `mysql-connector-python`. O SQL é destinado a **MySQL 8.0.16+**; ainda é necessário repetir os testes no MySQL escolhido para publicação. O ViaCEP tem testes de sucesso, CEP inexistente, resposta inválida e timeout usando respostas controladas. A consulta real do CEP `01001000` também retornou HTTP 200 e o endereço de São Paulo nesta revisão. A disponibilidade do serviço externo depende da rede.

A configuração de Vercel foi preparada, mas não publicada nesta tarefa. O projeto demonstra proteção básica; não inclui recuperação de senha, verificação de e-mail ou limite distribuído de tentativas de login. O JWT é guardado na sessão da aba e ainda seria acessível a um script malicioso; por isso, evitar XSS continua essencial. JWT assinado não é criptografado: não coloque segredos dentro dele.

## Tabela de segurança

| Risco | Proteção |
| --- | --- |
| SQL Injection | Queries parametrizadas |
| Vazamento de senha | bcrypt com salt |
| Credenciais no código | `.env` ignorado pelo Git |
| Acesso administrativo indevido | JWT + `tipo_usuario` consultado no banco |
| Alteração de preço pelo navegador | Valor calculado no back-end |
| Estoque negativo | Validação, bloqueio e atualização na transação |
| XSS | `textContent`, validação de imagens e CSP local |
| Token inválido | Validação da assinatura e expiração JWT |
| Dados interceptados | HTTPS na publicação e TLS no MySQL remoto |
| Erros expondo informações | Mensagens genéricas, sem senha nem SQL |

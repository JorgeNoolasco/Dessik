# Dessik — front-end

HTML organiza as páginas, CSS define a aparência e JavaScript busca dados e responde aos cliques. Não há React, Bootstrap ou outra biblioteca de interface.

## Como abrir

Primeiro execute o back-end conforme [privada/README.md](../privada/README.md). Abra **http://127.0.0.1:8000**. FastAPI serve esta pasta e a API no mesmo endereço. Não abra por duplo clique (`file://`): módulos JavaScript e requisições precisam de um servidor HTTP.

Opcionalmente, para hospedar o front-end separado, execute nesta pasta:

```powershell
python -m http.server 5500 --bind 127.0.0.1
```

Nesse caso, mude somente a constante em `js/api.js`:

```javascript
export const API_URL = "http://127.0.0.1:8000/api";
```

Abra http://127.0.0.1:5500. A API deve permitir essa origem em `CORS_ORIGINS`. O padrão da entrega é `API_URL = "/api"`, pois tudo roda na mesma origem. Na publicação separada, coloque a URL **HTTPS** do seu back-end nessa constante.

## O que cada arquivo faz

| Arquivo | Função |
| --- | --- |
| `index.html` | Apresentação da loja, quatro destaques vindos da API e benefícios |
| `loja.html` | Catálogo com busca, categorias, paginação e estoque |
| `cadastro.html` | Nome, e-mail, senha, confirmação e endereço |
| `login.html` | Entrada com e-mail e senha |
| `carrinho.html` | Itens, quantidades, subtotais e finalização |
| `admin.html` | Formulário e tabela para criar, editar e excluir produtos |
| `pedidos.html` | Histórico de pedidos da conta logada |
| `css/style.css` | Estrutura: grids, formulários, cards e responsividade |
| `css/storefront.css` | Identidade Dessik e detalhes visuais compartilhados |
| `js/api.js` | Centraliza `API_URL`, `fetch`, mensagens, sessão e criação segura de elementos |
| `js/loja.js` | Busca produtos, desenha cards e adiciona itens ao carrinho; também carrega os destaques |
| `js/carrinho.js` | Guarda IDs/quantidades na aba, consulta preços e envia o pedido |
| `js/cadastro.js` | Sugere senha, consulta CEP pela API e envia cadastro |
| `js/login.js` | Recebe o JWT e guarda na sessão da aba |
| `js/admin.js` | CRUD; a API verifica novamente se o usuário é admin |
| `js/pedidos.js` | Exibe os pedidos do próprio usuário |
| `imagens/` | Ilustrações locais de produtos e imagem de substituição |

`fetch()` faz uma requisição HTTP. `await response.json()` transforma o texto JSON em dados que o JavaScript consegue usar. `element()` cria elementos e preenche `textContent`: nomes e descrições recebidos não são interpretados como HTML.

Os oito primeiros produtos usam uma imagem com oito ilustrações. O CSS seleciona a região apropriada para cada card. Os quatro acessórios adicionais usam SVGs locais editáveis. Os arquivos de imagem fazem parte da entrega; não dependem de um serviço externo para abrir.

## Segurança no navegador

Tudo enviado ao navegador deve ser considerado público. Não coloque `.env`, senha do MySQL, `JWT_SECRET` ou chave secreta nesta pasta. A URL da API pode ser pública; suas credenciais não.

O token retornado após login é uma credencial temporária do usuário e não faz parte dos arquivos do repositório. Ele fica em `sessionStorage`. Sair remove o token. O carrinho usa o mesmo armazenamento, mas contém somente IDs e quantidades, sem dados de pagamento.

Esconder Administração melhora a interface; não protege a API. O servidor valida o JWT e o papel do usuário em cada operação. Preço, estoque e total vistos no carrinho são uma estimativa até o servidor confirmar a compra. Se o estoque mudar, a API recusa a compra e o carrinho consulta os dados atualizados.

Para modificar a aparência, comece pelas variáveis e pelas seções comentadas em `storefront.css`. Para mudar produtos, use o administrador ou o banco: não escreva cards fixos no HTML.

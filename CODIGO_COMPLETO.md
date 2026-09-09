# Dessik — código completo

Esta cópia reúne os arquivos textuais da entrega. Consulte README.md para executar, estudar, testar e apresentar. Nenhum segredo do `.env` é incluído. As imagens PNG são entregues como arquivos em `publico/imagens/`.


## ARQUIVO: publico/.gitignore

```text
.env
.env.*
!.env.example
venv/
.venv/
__pycache__/
*.pyc
.pytest_cache/
.vercel/
```

O que este arquivo faz:

- Mantém arquivos privados e temporários fora do Git.


## ARQUIVO: publico/admin.html

```html
<!DOCTYPE html>
<html lang="pt-BR">
 <head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1" name="viewport"/>
  <meta content="Dessik: loja fictícia de tecnologia para um projeto acadêmico." name="description"/>
  <title>
   Administração | Dessik
  </title>
  <link href="/imagens/placeholder.svg" rel="icon" type="image/svg+xml"/>
  <link href="/css/style.css" rel="stylesheet"/>
  <link href="/css/storefront.css?v=3" rel="stylesheet"/>
  <script src="/js/admin.js" type="module">
  </script>
 </head>
 <body class="account-page">
  <a class="skip" href="#main">
   Pular para o conteúdo
  </a>
  <div class="topnote">
   SEU SETUP, SUAS REGRAS.
   <span>
    Loja fictícia · Sem cobranças reais
   </span>
  </div>
  <header class="navbar">
   <div class="nav-inner">
    <a aria-label="Dessik início" class="brand" href="/index.html">
     dessik
     <span>
      .
     </span>
    </a>
    <nav aria-label="Navegação principal">
     <a href="/index.html">
      Início
     </a>
     <a href="/carrinho.html">
      Carrinho
     </a>
     <a href="/loja.html">
      Produtos
     </a>
     <a data-session="" hidden="" href="/pedidos.html">
      Meus pedidos
     </a>
     <a data-admin="" hidden="" href="/admin.html">
      Administração
     </a>
     <a data-guest="" href="/login.html">
      Entrar
     </a>
     <a class="button secondary" data-guest="" href="/cadastro.html">
      Criar conta
     </a>
     <span class="nav-session" data-session="" hidden="">
      <span data-user="">
      </span>
      <button class="secondary" data-logout="">
       Sair
      </button>
     </span>
    </nav>
   </div>
  </header>
  <main id="main">
   <section class="intro">
    <div>
     <p class="eyebrow">
      Administração
     </p>
     <h1>
      Seu catálogo, em dia.
     </h1>
     <p>
      Cadastre produtos, ajuste preços e acompanhe o estoque.
     </p>
    </div>
   </section>
   <div aria-live="polite" class="message" hidden="" id="message" role="status">
   </div>
   <div class="admin-layout" hidden="" id="admin-content">
    <section class="form-panel">
     <h2 id="form-title">
      Novo produto
     </h2>
     <form id="product-form">
      <div class="fields">
       <label>
        Nome
        <input maxlength="120" minlength="2" name="nome" required=""/>
       </label>
       <label>
        Descrição
        <textarea maxlength="2000" name="descricao" required=""></textarea>
       </label>
       <label>
        Categoria
        <input maxlength="60" name="categoria" required=""/>
       </label>
       <div class="two-cols">
        <label>
         Preço (R$)
         <input max="99999999.99" min="0.01" name="preco" required="" step="0.01" type="number"/>
        </label>
        <label>
         Estoque
         <input max="1000000" min="0" name="quantidade_estoque" required="" step="1" type="number"/>
        </label>
       </div>
       <label>
        Imagem
        <input maxlength="1000" name="imagem_url" required="" value="/imagens/placeholder.svg"/>
        <span class="hint">
         URL HTTPS ou caminho em /imagens/.
        </span>
       </label>
      </div>
      <div class="actions">
       <button id="save-product" type="submit">
        Cadastrar produto
       </button>
       <button class="secondary" id="cancel-edit" type="button">
        Limpar
       </button>
      </div>
     </form>
    </section>
    <section aria-label="Produtos cadastrados">
     <div class="table-wrap">
      <table>
       <thead>
        <tr>
         <th scope="col">
          Produto
         </th>
         <th scope="col">
          Preço
         </th>
         <th scope="col">
          Estoque
         </th>
         <th scope="col">
          Ações
         </th>
        </tr>
       </thead>
       <tbody id="product-rows">
       </tbody>
      </table>
     </div>
     <div class="pagination">
      <button class="secondary" disabled="" id="previous">
       Anterior
      </button>
      <span id="page-number">
       Página 1
      </span>
      <button class="secondary" disabled="" id="next">
       Próxima
      </button>
     </div>
    </section>
   </div>
  </main>
  <dialog aria-labelledby="dialog-title" id="confirm-dialog">
   <h2 id="dialog-title">
   </h2>
   <p>
   </p>
   <form class="actions" method="dialog">
    <button autofocus="" class="secondary" value="cancel">
     Cancelar
    </button>
    <button value="confirm">
     Confirmar
    </button>
   </form>
  </dialog>
  <footer>
   <div class="footer-main">
    <div>
     <a class="brand" href="/index.html">
      dessik
      <span>
       .
      </span>
     </a>
     <p>
      Tecnologia para quem faz
      <br/>
      do próprio jeito.
     </p>
    </div>
    <div class="footer-links">
     <a href="/loja.html">
      Explorar produtos
     </a>
     <a href="/login.html">
      Minha conta
     </a>
     <a href="/cadastro.html">
      Criar conta
     </a>
    </div>
   </div>
   <div class="footer-bottom">
    <span>
     © 2026 Dessik. Projeto acadêmico.
    </span>
    <span>
     Produtos fictícios. Compras simuladas. Nenhuma cobrança.
    </span>
   </div>
  </footer>
 </body>
</html>
```

O que este arquivo faz:

- Organiza o formulário de produto e a tabela administrativa.


## ARQUIVO: publico/cadastro.html

```html
<!DOCTYPE html>
<html lang="pt-BR">
 <head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1" name="viewport"/>
  <meta content="Dessik: loja fictícia de tecnologia para um projeto acadêmico." name="description"/>
  <title>
   Criar conta | Dessik
  </title>
  <link href="/imagens/placeholder.svg" rel="icon" type="image/svg+xml"/>
  <link href="/css/style.css" rel="stylesheet"/>
  <link href="/css/storefront.css?v=3" rel="stylesheet"/>
  <script src="/js/cadastro.js" type="module">
  </script>
 </head>
 <body class="account-page">
  <a class="skip" href="#main">
   Pular para o conteúdo
  </a>
  <div class="topnote">
   SEU SETUP, SUAS REGRAS.
   <span>
    Loja fictícia · Sem cobranças reais
   </span>
  </div>
  <header class="navbar">
   <div class="nav-inner">
    <a aria-label="Dessik início" class="brand" href="/index.html">
     dessik
     <span>
      .
     </span>
    </a>
    <nav aria-label="Navegação principal">
     <a href="/index.html">
      Início
     </a>
     <a href="/carrinho.html">
      Carrinho
     </a>
     <a href="/loja.html">
      Produtos
     </a>
     <a data-session="" hidden="" href="/pedidos.html">
      Meus pedidos
     </a>
     <a data-admin="" hidden="" href="/admin.html">
      Administração
     </a>
     <a data-guest="" href="/login.html">
      Entrar
     </a>
     <a class="button secondary" data-guest="" href="/cadastro.html">
      Criar conta
     </a>
     <span class="nav-session" data-session="" hidden="">
      <span data-user="">
      </span>
      <button class="secondary" data-logout="">
       Sair
      </button>
     </span>
    </nav>
   </div>
  </header>
  <main id="main">
   <div class="form-layout">
    <section class="form-intro">
     <p class="eyebrow">
      Vamos começar
     </p>
     <h1>
      Suas ideias.
      <br/>
      Seu próximo setup.
     </h1>
     <p>
      Crie sua conta para experimentar a loja. Todas as compras são simulações, sem pagamento.
     </p>
     <a href="/loja.html">
      ← Conhecer os produtos
     </a>
    </section>
    <section class="form-panel">
     <h2>
      Crie sua conta
     </h2>
     <div aria-live="polite" class="message" hidden="" id="message" role="status">
     </div>
     <form id="register-form">
      <div class="fields">
       <label>
        Nome
        <input autocomplete="name" maxlength="100" minlength="2" name="nome" required=""/>
       </label>
       <label>
        E-mail
        <input autocomplete="email" maxlength="254" name="email" required="" type="email"/>
       </label>
       <label>
        Senha
        <input aria-describedby="password-hint" autocomplete="new-password" maxlength="72" minlength="8" name="senha" required="" type="password"/>
        <span class="hint" id="password-hint">
         Pelo menos 8 caracteres. Use uma senha exclusiva.
        </span>
       </label>
       <button class="secondary" id="generate-password" type="button">
        Sugerir senha segura
       </button>
       <label>
        Confirmar senha
        <input autocomplete="new-password" maxlength="72" minlength="8" name="confirmar_senha" required="" type="password"/>
       </label>
      </div>
      <div class="form-section">
       <h3>
        Endereço
       </h3>
       <p class="hint">
        Opcional. Consulte o CEP ou preencha manualmente.
       </p>
      </div>
      <div class="fields">
       <label>
        CEP
        <input autocomplete="postal-code" inputmode="numeric" maxlength="9" name="cep" pattern="[0-9]{5}-?[0-9]{3}" placeholder="00000-000"/>
       </label>
       <button class="secondary" id="lookup-cep" type="button">
        Consultar CEP
       </button>
       <div class="message" hidden="" id="cep-message" role="status">
       </div>
       <label>
        Logradouro
        <input autocomplete="address-line1" maxlength="150" name="logradouro"/>
       </label>
       <label>
        Bairro
        <input maxlength="100" name="bairro"/>
       </label>
       <div class="two-cols">
        <label>
         Cidade
         <input autocomplete="address-level2" maxlength="100" name="cidade"/>
        </label>
        <label>
         Estado (UF)
         <input autocomplete="address-level1" maxlength="2" name="estado" pattern="[A-Za-z]{2}" placeholder="SP"/>
        </label>
       </div>
      </div>
      <div class="actions">
       <button class="full" type="submit">
        Cadastrar
       </button>
      </div>
     </form>
     <p class="form-foot">
      Já tem uma conta?
      <a href="/login.html">
       Entrar
      </a>
     </p>
    </section>
   </div>
  </main>
  <dialog aria-labelledby="dialog-title" id="confirm-dialog">
   <h2 id="dialog-title">
   </h2>
   <p>
   </p>
   <form class="actions" method="dialog">
    <button autofocus="" class="secondary" value="cancel">
     Cancelar
    </button>
    <button value="confirm">
     Confirmar
    </button>
   </form>
  </dialog>
  <footer>
   <div class="footer-main">
    <div>
     <a class="brand" href="/index.html">
      dessik
      <span>
       .
      </span>
     </a>
     <p>
      Tecnologia para quem faz
      <br/>
      do próprio jeito.
     </p>
    </div>
    <div class="footer-links">
     <a href="/loja.html">
      Explorar produtos
     </a>
     <a href="/login.html">
      Minha conta
     </a>
     <a href="/cadastro.html">
      Criar conta
     </a>
    </div>
   </div>
   <div class="footer-bottom">
    <span>
     © 2026 Dessik. Projeto acadêmico.
    </span>
    <span>
     Produtos fictícios. Compras simuladas. Nenhuma cobrança.
    </span>
   </div>
  </footer>
 </body>
</html>
```

O que este arquivo faz:

- Mostra o formulário de conta e endereço.


## ARQUIVO: publico/carrinho.html

```html
<!DOCTYPE html>
<html lang="pt-BR">
 <head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1" name="viewport"/>
  <meta content="Dessik: loja fictícia de tecnologia para um projeto acadêmico." name="description"/>
  <title>
   Carrinho | Dessik
  </title>
  <link href="/imagens/placeholder.svg" rel="icon" type="image/svg+xml"/>
  <link href="/css/style.css" rel="stylesheet"/>
  <link href="/css/storefront.css?v=3" rel="stylesheet"/>
  <script src="/js/carrinho.js" type="module">
  </script>
 </head>
 <body class="store-page">
  <a class="skip" href="#main">
   Pular para o conteúdo
  </a>
  <div class="topnote">
   SEU SETUP, SUAS REGRAS.
   <span>
    Loja fictícia · Sem cobranças reais
   </span>
  </div>
  <header class="navbar">
   <div class="nav-inner">
    <a aria-label="Dessik início" class="brand" href="/index.html">
     dessik
     <span>
      .
     </span>
    </a>
    <nav aria-label="Navegação principal">
     <a href="/index.html">
      Início
     </a>
     <a aria-current="page" href="/carrinho.html">
      Carrinho
     </a>
     <a href="/loja.html">
      Explorar produtos
     </a>
     <a data-session="" hidden="" href="/pedidos.html">
      Meus pedidos
     </a>
     <a data-admin="" hidden="" href="/admin.html">
      Administração
     </a>
     <a data-guest="" href="/login.html">
      Entrar
     </a>
     <a class="button secondary" data-guest="" href="/cadastro.html">
      Criar conta
     </a>
     <span class="nav-session" data-session="" hidden="">
      <span data-user="">
      </span>
      <button class="secondary" data-logout="">
       Sair
      </button>
     </span>
    </nav>
   </div>
  </header>
  <main id="main">
   <section class="intro">
    <div>
     <p class="eyebrow">
      SEU PRÓXIMO UPGRADE
     </p>
     <h1>
      Meu carrinho
      <span>
       .
      </span>
     </h1>
     <p>
      Confira seus produtos e finalize a compra simulada.
     </p>
    </div>
    <a class="button secondary" href="/loja.html">
     Continuar comprando ↗
    </a>
   </section>
   <div aria-live="polite" class="message" hidden="" id="message" role="status">
   </div>
   <div class="cart-layout">
    <section aria-label="Itens do carrinho" id="cart-items">
    </section>
    <aside class="form-panel">
     <h2>
      Resumo do pedido
     </h2>
     <p>
      Total estimado
     </p>
     <strong class="price" id="cart-total">
      R$ 0,00
     </strong>
     <p class="hint">
      Compra simulada. Sem pagamento nem entrega.
     </p>
     <div class="fields">
      <button disabled="" id="checkout">
       Finalizar pedido
      </button>
      <button class="secondary" id="refresh-cart">
       Atualizar carrinho
      </button>
      <a hidden="" href="/login.html" id="cart-login">
       Entrar na minha conta
      </a>
      <a href="/pedidos.html">
       Meus pedidos
      </a>
     </div>
    </aside>
   </div>
  </main>
  <footer>
   <div class="footer-main">
    <div>
     <a class="brand" href="/index.html">
      dessik
      <span>
       .
      </span>
     </a>
     <p>
      Tecnologia para quem faz
      <br/>
      do próprio jeito.
     </p>
    </div>
    <div class="footer-links">
     <a href="/loja.html">
      Explorar produtos
     </a>
     <a href="/login.html">
      Minha conta
     </a>
     <a href="/cadastro.html">
      Criar conta
     </a>
    </div>
   </div>
   <div class="footer-bottom">
    <span>
     © 2026 Dessik. Projeto acadêmico.
    </span>
    <span>
     Produtos fictícios. Compras simuladas. Nenhuma cobrança.
    </span>
   </div>
  </footer>
 </body>
</html>
```

O que este arquivo faz:

- Mostra itens selecionados, resumo e botão de finalizar pedido.


## ARQUIVO: publico/css/storefront.css

```css
/* Identidade Dessik. style.css contém os componentes básicos. */
:root {
    --ink: #252932;
    --muted: #59616e;
    --green: #984120;
    --line: #dce0e6;
    --bg: #f4f5f7;
    --red: #a12535;
    font-family: "Segoe UI", Arial, sans-serif;
}

button,
.button {
    background: #ff855a;
    color: #291a12;
    font-size: .9rem;
}

.secondary {
    background: #e9ecf0;
    color: #29303b;
    border: 1px solid #c9ced6;
}

.danger {
    background: #fff0f2;
    color: #a12535;
}

button:disabled {
    background: #e4e7ec;
    color: #69717d;
}

input,
textarea,
select {
    border-color: #bdc5d0;
}

button:focus-visible,
a:focus-visible,
input:focus-visible,
select:focus-visible,
textarea:focus-visible {
    outline-color: #984120;
}

.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}

.topnote {
    background: #2b2521;
    color: #ffa67f;
    display: flex;
    justify-content: space-between;
    padding: 9px 36px;
    font-size: .7rem;
    letter-spacing: 1px;
}

.topnote span {
    color: #b5a99e;
    letter-spacing: 0;
}

.nav-inner {
    max-width: 1344px;
    padding: 24px 36px;
    flex-wrap: wrap;
}

.brand {
    font-size: 2.6rem;
    line-height: 1;
    letter-spacing: -2.5px;
    font-weight: 800;
}

.brand span {
    color: #ff855a;
}

nav {
    gap: 24px;
}

nav a {
    font-size: .85rem;
}

nav a.button {
    background: #252932;
    color: white;
}

main {
    max-width: 1344px;
    padding: 22px 36px 72px;
}

/* Apresentação da loja */
.hero {
    display: grid;
    grid-template-columns: 1.2fr 1fr;
    min-height: 450px;
    background: #26272c;
    color: white;
    border: 1px solid #3b3d44;
    border-radius: 16px;
    overflow: hidden;
}

.hero-copy {
    padding: 38px 40px;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.collection-label {
    width: 100%;
    display: flex;
    justify-content: space-between;
    gap: 12px;
    font-size: .65rem;
    letter-spacing: 1.6px;
    color: #c6c8d0;
}

.hero h1 {
    font-size: clamp(2.5rem, 4.5vw, 4rem);
    font-weight: 800;
    line-height: 1.04;
    letter-spacing: -2.6px;
    margin: 28px 0 20px;
}

.hero h1 em {
    font-style: normal;
    color: #ff855a;
}

.hero-copy>p:not(.collection-label) {
    max-width: 355px;
    color: #b6bbc8;
    line-height: 1.65;
    font-size: .94rem;
}

.hero-button {
    margin-top: 12px;
    gap: 30px;
}

.home-register {
    color: #ffb394;
    margin-top: 16px;
    font-size: .9rem;
}

.hero-caption {
    margin-top: auto;
    padding-top: 28px;
    color: #b6bbc8;
    font-size: .62rem;
    letter-spacing: 2px;
}

.hero-showcase {
    position: relative;
    min-height: 350px;
    background: #e9edf2;
    color: #202530;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 28px;
    overflow: hidden;
}

.showcase-kicker {
    position: relative;
    z-index: 1;
    font-size: .62rem;
    letter-spacing: 2px;
    color: #626d7c;
}

.hero-product {
    position: absolute;
    width: 405px;
    aspect-ratio: 1;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -52%);
}

.showcase-bottom {
    position: relative;
    z-index: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: auto;
}

.showcase-bottom>div {
    display: flex;
    flex-direction: column;
    gap: 3px;
}

.showcase-bottom span {
    font-size: .61rem;
    letter-spacing: 1.7px;
    color: #626c7b;
}

.showcase-bottom strong {
    font-size: 1.45rem;
}

.showcase-bottom>a {
    width: 40px;
    height: 40px;
    display: grid;
    place-items: center;
    background: #fafbfc;
    color: #252b35;
    border: 1px solid #a6acb6;
    border-radius: 50%;
    text-decoration: none;
    font-size: 1.5rem;
}

.collection-strip {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    border-bottom: 1px solid var(--line);
    padding: 23px 2px;
    margin-bottom: 31px;
    color: var(--muted);
    font-size: .66rem;
    letter-spacing: 1.7px;
}

.collection-strip b {
    color: #984120;
    margin: 0 16px;
}

/* Busca, filtros e cards */
.catalog-bar {
    border: 0;
    margin-bottom: 26px;
}

.catalog-bar h2 {
    font-size: 2rem;
}

.catalog-bar h2 span {
    color: #984120;
}

.catalog-bar .eyebrow {
    font-size: .65rem;
}

#product-count {
    font-size: .8rem;
}

.catalog-tools {
    display: flex;
    justify-content: space-between;
    gap: 24px;
    margin-bottom: 20px;
}

.search-box {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 12px;
    background: white;
    border: 1px solid #bdc5d0;
    border-radius: 7px;
    padding: 0 14px;
    flex: 1;
    max-width: 550px;
}

.search-box input {
    border: 0;
    background: transparent;
}

.sort-box {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 12px;
    font-size: .8rem;
}

.sort-box select {
    width: 165px;
}

.category-tabs {
    display: flex;
    flex-wrap: wrap;
    gap: 9px;
    margin-bottom: 26px;
}

.category-tabs button {
    background: white;
    color: #4d5562;
    border: 1px solid #cbd0d8;
    min-height: 36px;
    padding: 8px 16px;
    font-size: .77rem;
}

.category-tabs button[aria-pressed=true] {
    background: #252932;
    color: white;
    border-color: #252932;
}

.card {
    box-shadow: 0 4px 16px #27314208;
}

.card:hover {
    border-color: #adb5c2;
}

.product-visual {
    position: relative;
    aspect-ratio: 1.16;
    background: #eff2f6;
    overflow: hidden;
}

.product-visual .product-art {
    position: absolute;
    width: 100%;
    aspect-ratio: 1;
    top: 50%;
    transform: translateY(-50%);
}

.product-visual img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    background: #eff2f6;
}

.product-tag {
    position: absolute;
    left: 12px;
    top: 12px;
    border-radius: 4px;
    background: #ffffffed;
    padding: 5px 7px;
    color: #596878;
    font-size: .55rem;
    letter-spacing: .7px;
}

.card .category {
    font-size: .65rem;
}

.card h3 {
    font-size: 1rem;
}

.description {
    font-size: .85rem;
}

.stock {
    color: #246743;
    font-size: .75rem;
}

.stock.out {
    color: #a12535;
}

.buy-row button {
    background: #303641;
    color: white;
    font-size: .8rem;
}

.buy-row input {
    color: #252932;
    background: white;
}

/* A imagem reúne 4 colunas e 2 linhas. Cada posição mostra um produto. */
.product-art {
    background-image: url('/imagens/catalogo-dessik.png');
    background-size: 400% 200%;
    background-repeat: no-repeat;
}

.art-notebook {
    background-position: 0% 0%;
}

.art-mouse {
    background-position: 33.333333% 0%;
}

.art-teclado {
    background-position: 66.666667% 0%;
}

.art-monitor {
    background-position: 100% 0%;
}

.art-headset {
    background-position: 0% 100%;
}

.art-webcam {
    background-position: 33.333333% 100%;
}

.art-ssd {
    background-position: 66.666667% 100%;
}

.art-ram {
    background-position: 100% 100%;
}

/* Conta, carrinho e rodapé */
.account-page main {
    padding-top: 52px;
}

.form-panel {
    box-shadow: 0 4px 16px #27314208;
}

.form-intro h1 {
    font-size: clamp(2.5rem, 4vw, 3.6rem);
}

.form-layout {
    max-width: 1100px;
}

.cart-layout {
    display: grid;
    grid-template-columns: 1fr 340px;
    gap: 28px;
    align-items: start;
}

.cart-item {
    background: white;
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
}

.cart-item h2 {
    font-size: 1.2rem;
    margin-bottom: 8px;
}

.cart-item input {
    max-width: 110px;
}

.cart-item p {
    color: var(--muted);
}

.cart-item strong {
    white-space: nowrap;
}

.benefits {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 26px;
    margin-top: 65px;
}

.benefits article {
    border-top: 2px solid var(--line);
    padding-top: 22px;
}

.benefits span {
    font-size: .7rem;
    letter-spacing: 1px;
    color: #984120;
}

.benefits h2 {
    font-size: 1.25rem;
    margin-top: 15px;
}

.benefits p {
    color: var(--muted);
}

.home-page .catalog-tools,
.home-page .category-tabs,
.home-page .pagination {
    display: none;
}

.order-card {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    background: white;
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 25px;
    margin-bottom: 15px;
}

.order-status {
    color: #246743;
}

footer {
    display: block;
    max-width: 1272px;
    padding: 0;
}

.footer-main {
    display: flex;
    justify-content: space-between;
    gap: 30px;
    padding: 37px 0;
}

.footer-main p {
    margin: 14px 0 0;
}

.footer-links {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 30px;
}

.footer-links a {
    color: var(--muted);
    text-decoration: none;
    font-size: .8rem;
}

.footer-bottom {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    padding: 20px 0;
    border-top: 1px solid var(--line);
    font-size: .7rem;
}

/* Três pontos de ajuste; a estrutura básica usa grid e flex. */
@media(max-width:1100px) {
    .hero h1 {
        font-size: 3.3rem;
    }

    .hero-copy {
        padding: 32px 28px;
    }

    .hero-product {
        width: 350px;
    }

    .footer-main,
    .footer-bottom {
        margin: 0 36px;
    }
}

@media(max-width:850px) {
    .hero {
        grid-template-columns: 1fr 1fr;
    }

    .hero h1 {
        font-size: 2.5rem;
        letter-spacing: -1.5px;
    }

    .hero-product {
        width: 300px;
    }

    .collection-label span {
        display: none;
    }

    .cart-layout {
        grid-template-columns: 1fr;
    }

    .cart-item {
        flex-wrap: wrap;
    }

    .collection-strip {
        justify-content: center;
    }

    .collection-strip>span:first-child {
        display: none;
    }

    .benefits {
        grid-template-columns: 1fr;
    }
}

@media(max-width:520px) {
    main {
        padding: 20px 22px 45px;
    }

    .nav-inner {
        padding: 20px 22px;
        flex-direction: column;
        align-items: flex-start;
    }

    nav {
        justify-content: flex-start;
        gap: 14px;
    }

    .brand {
        font-size: 2.2rem;
    }

    .topnote {
        justify-content: center;
        padding: 9px 22px;
    }

    .topnote span {
        display: none;
    }

    .hero {
        grid-template-columns: 1fr;
    }

    .hero h1 {
        font-size: 2.8rem;
    }

    .hero-showcase {
        min-height: 310px;
    }

    .catalog-tools {
        flex-direction: column;
    }

    .search-box {
        max-width: none;
    }

    .sort-box {
        justify-content: space-between;
    }

    .catalog-bar h2 {
        font-size: 1.6rem;
    }

    .catalog-bar {
        align-items: flex-start;
        gap: 12px;
    }

    .collection-strip {
        font-size: .55rem;
        letter-spacing: 1px;
    }

    .collection-strip b {
        margin: 0 8px;
    }

    .product-visual {
        aspect-ratio: 1.35;
    }

    .cart-item {
        padding: 18px;
    }

    .footer-main,
    .footer-bottom {
        flex-direction: column;
        margin: 0 22px;
    }

    .footer-links {
        gap: 20px;
    }

    .order-card {
        flex-direction: column;
    }
}
```

O que este arquivo faz:

- Define a identidade visual Dessik e adapta as superfícies para o fundo claro.


## ARQUIVO: publico/css/style.css

```css
:root {
    color-scheme: light;
    --ink: #182622;
    --muted: #56665f;
    --green: #156c48;
    --lime: #d9f46b;
    --line: #dce3de;
    --bg: #f5f7f5;
    --white: #fff;
    --red: #aa2533;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 16px
}

* {
    box-sizing: border-box
}

body {
    margin: 0;
    background: var(--bg);
    color: var(--ink);
    line-height: 1.5
}

a {
    color: var(--green);
    text-underline-offset: 4px
}

button,
input,
textarea,
select {
    font: inherit
}

button,
.button {
    cursor: pointer;
    border: 0;
    border-radius: 8px;
    background: var(--green);
    color: white;
    padding: 12px 18px;
    font-weight: 700;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    min-height: 46px
}

button:hover,
.button:hover {
    filter: brightness(.92)
}

button:disabled {
    cursor: not-allowed;
    opacity: .55
}

.secondary {
    background: #eaf0eb;
    color: var(--ink)
}

.danger {
    background: #fff0f0;
    color: var(--red)
}

button:focus-visible,
a:focus-visible,
input:focus-visible,
select:focus-visible,
textarea:focus-visible {
    outline: 3px solid #88700c;
    outline-offset: 3px
}

[hidden] {
    display: none !important
}

.skip {
    position: absolute;
    top: -80px;
    left: 10px;
    background: white;
    padding: 15px;
    z-index: 10
}

.skip:focus {
    top: 5px
}

.topnote {
    background: var(--ink);
    color: #eef5ef;
    text-align: center;
    padding: 8px;
    font-size: .875rem
}

.navbar {
    background: white;
    border-bottom: 1px solid var(--line)
}

.nav-inner {
    max-width: 1200px;
    margin: auto;
    min-height: 88px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
    padding: 16px 28px
}

.brand {
    color: var(--ink);
    font-weight: 900;
    font-size: 2rem;
    letter-spacing: -1.8px;
    text-decoration: none
}

.brand span {
    color: var(--green)
}

nav {
    display: flex;
    align-items: center;
    gap: 24px;
    flex-wrap: wrap
}

nav a {
    color: var(--ink);
    text-decoration: none;
    font-size: .9375rem
}

nav a[aria-current=page] {
    color: var(--green);
    font-weight: bold
}

.nav-session {
    display: flex;
    align-items: center;
    gap: 12px
}

.nav-session button {
    padding: 8px 14px;
    min-height: 40px
}

main {
    max-width: 1200px;
    margin: 0 auto;
    padding: 38px 28px 64px
}

.eyebrow {
    color: var(--green);
    font-size: .875rem;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    font-weight: 700
}

h1,
h2,
h3,
p {
    margin-top: 0
}

h1 {
    font-size: clamp(2rem, 4vw, 3.3rem);
    line-height: 1.12;
    letter-spacing: -1.5px;
    margin-bottom: 18px
}

h2 {
    font-size: 1.6rem;
    letter-spacing: -.6px
}

h3 {
    font-size: 1.125rem
}

.intro {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
    margin-bottom: 30px
}

.intro p {
    color: var(--muted);
    margin-bottom: 0
}

.pill {
    background: var(--lime);
    padding: 8px 14px;
    border-radius: 50px;
    font-size: .875rem;
    white-space: nowrap
}

.catalog-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 18px;
    padding-top: 20px;
    border-top: 1px solid var(--line)
}

.catalog-bar h2 {
    margin: 0
}

.muted {
    color: var(--muted)
}

.grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 20px
}

.card {
    background: white;
    border: 1px solid var(--line);
    border-radius: 12px;
    overflow: hidden;
    display: flex;
    flex-direction: column
}

.card img {
    width: 100%;
    height: 185px;
    object-fit: contain;
    background: #e9eeea
}

.card-body {
    padding: 20px;
    display: flex;
    flex-direction: column;
    flex: 1;
    gap: 8px
}

.card .category {
    color: var(--green);
    font-size: .8125rem;
    text-transform: uppercase;
    letter-spacing: .8px;
    margin: 0
}

.card h3 {
    margin: 0
}

.description {
    color: var(--muted);
    font-size: .9375rem;
    flex: 1;
    margin: 0 0 4px
}

.price {
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0
}

.stock {
    font-size: .875rem;
    color: var(--green);
    margin: 0 0 10px
}

.stock.out {
    color: var(--red)
}

.buy-row {
    display: flex;
    gap: 8px
}

.buy-row input {
    width: 65px;
    padding: 10px
}

.buy-row button {
    flex: 1;
    padding: 10px
}

.message {
    padding: 14px 18px;
    border-radius: 8px;
    background: #edf2ef;
    border: 1px solid var(--line);
    margin-bottom: 20px;
    overflow-wrap: anywhere
}

.message.error {
    background: #fff0f0;
    border-color: #e8bac0;
    color: #86212d
}

.message.success {
    background: #e5f2e9;
    border-color: #9dceb1;
    color: #15552e
}

.empty {
    padding: 48px;
    text-align: center;
    background: white;
    border: 1px dashed var(--line);
    border-radius: 12px;
    grid-column: 1/-1
}

.form-layout {
    display: grid;
    grid-template-columns: .85fr 1.15fr;
    gap: 70px;
    align-items: start;
    max-width: 1000px
}

.form-intro {
    padding-top: 32px
}

.form-intro p {
    color: var(--muted);
    max-width: 330px
}

.form-panel {
    background: white;
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 30px
}

.form-panel h2 {
    margin-bottom: 22px
}

label {
    display: flex;
    flex-direction: column;
    gap: 6px;
    font-size: .9375rem;
    font-weight: 600
}

input,
textarea,
select {
    width: 100%;
    border: 1px solid #b8c7bd;
    border-radius: 7px;
    padding: 11px 12px;
    background: white;
    color: var(--ink);
    min-height: 46px
}

textarea {
    resize: vertical;
    min-height: 100px
}

.fields {
    display: grid;
    gap: 18px
}

.two-cols {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px
}

.actions {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 20px
}

.full {
    width: 100%
}

.form-foot {
    font-size: .9375rem;
    color: var(--muted);
    margin: 22px 0 0
}

.hint {
    font-size: .875rem;
    color: var(--muted);
    font-weight: 400
}

.form-section {
    margin: 24px 0 16px;
    border-top: 1px solid var(--line);
    padding-top: 22px
}

.form-section h3 {
    margin-bottom: 4px
}

.admin-layout {
    display: grid;
    grid-template-columns: 360px 1fr;
    gap: 28px;
    align-items: start
}

.table-wrap {
    overflow: auto;
    background: white;
    border: 1px solid var(--line);
    border-radius: 12px
}

table {
    width: 100%;
    border-collapse: collapse;
    text-align: left;
    font-size: .9375rem
}

th,
td {
    padding: 16px;
    border-bottom: 1px solid var(--line)
}

th {
    background: #ecf1ed;
    font-size: .875rem
}

td button {
    font-size: .875rem;
    min-height: 36px;
    padding: 6px 10px;
    margin: 3px
}

.pagination {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    gap: 14px;
    margin-top: 24px
}

footer {
    max-width: 1200px;
    margin: auto;
    padding: 24px 28px;
    border-top: 1px solid var(--line);
    display: flex;
    justify-content: space-between;
    gap: 15px;
    font-size: .875rem;
    color: var(--muted)
}

dialog {
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 28px;
    max-width: 460px;
    width: calc(100% - 32px)
}

dialog::backdrop {
    background: #10251eb3
}

dialog h2 {
    font-size: 1.5rem
}

dialog .actions {
    justify-content: flex-end
}

@media(max-width:1000px) {
    .grid {
        grid-template-columns: repeat(3, minmax(0, 1fr))
    }

    .admin-layout {
        grid-template-columns: 300px 1fr
    }

    .form-layout {
        gap: 32px
    }
}

@media(max-width:760px) {
    .grid {
        grid-template-columns: repeat(2, minmax(0, 1fr))
    }

    .form-layout,
    .admin-layout {
        grid-template-columns: 1fr
    }

    .form-intro {
        padding-top: 0
    }

    .form-intro p {
        max-width: none
    }

    .nav-inner {
        align-items: flex-start;
        gap: 16px;
        padding: 16px 20px
    }

    nav {
        gap: 14px;
        justify-content: flex-end
    }

    .intro {
        align-items: flex-start
    }

    .pill {
        white-space: normal
    }

    main {
        padding: 28px 20px 44px
    }

    .form-panel {
        padding: 24px
    }

    .nav-session {
        flex-wrap: wrap;
        justify-content: flex-end
    }
}

@media(max-width:460px) {

    .grid,
    .two-cols {
        grid-template-columns: 1fr
    }

    .card img {
        height: 210px
    }

    .intro {
        display: block
    }

    .intro .pill {
        display: inline-block;
        margin-top: 18px
    }

    .nav-inner {
        flex-direction: column
    }

    nav {
        justify-content: flex-start;
        gap: 18px
    }

    .brand {
        font-size: 1.8rem
    }

    .catalog-bar {
        gap: 12px;
        align-items: flex-start
    }

    footer {
        flex-direction: column
    }

    .form-panel {
        padding: 20px
    }
}
```

O que este arquivo faz:

- Define a estrutura responsiva e os componentes básicos.


## ARQUIVO: publico/imagens/controle.svg

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="#e9edf2"/><path d="M135 105h130c35 0 65 115 35 125-25 8-50-45-65-45h-60c-15 0-40 53-65 45-30-10 0-125 25-125z" fill="#343b47"/><path d="M140 130v42m-21-21h42" stroke="#94a0b1" stroke-width="10"/><circle cx="258" cy="142" r="10" fill="#ff855a"/><circle cx="280" cy="163" r="10" fill="#ff855a"/></svg>
```

O que este arquivo faz:

- Fornece uma imagem local editável.


## ARQUIVO: publico/imagens/hub.svg

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="#e9edf2"/><rect x="90" y="110" width="220" height="90" rx="20" fill="#414854"/><path d="M310 150h30v-60" fill="none" stroke="#414854" stroke-width="12"/><g fill="#ff855a"><rect x="115" y="145" width="35" height="20"/><rect x="180" y="145" width="35" height="20"/><rect x="245" y="145" width="35" height="20"/></g></svg>
```

O que este arquivo faz:

- Fornece uma imagem local editável.


## ARQUIVO: publico/imagens/mousepad.svg

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="#e9edf2"/><path d="M80 100h220l40 120H40z" fill="#343b47" stroke="#ff855a" stroke-width="5"/><path d="M115 135h90m-65 25h90m-60 25h90" stroke="#596576" stroke-width="4"/></svg>
```

O que este arquivo faz:

- Fornece uma imagem local editável.


## ARQUIVO: publico/imagens/placeholder.svg

```xml
<svg xmlns="http://www.w3.org/2000/svg" width="640" height="420" viewBox="0 0 640 420"><rect width="640" height="420" fill="#e9eeea"/><text x="320" y="205" text-anchor="middle" font-family="Arial,sans-serif" font-size="60" font-weight="bold" letter-spacing="-3" fill="#156c48">dessik.</text><text x="320" y="250" text-anchor="middle" font-family="Arial,sans-serif" font-size="18" letter-spacing="3" fill="#56665f">IMAGEM ILUSTRATIVA</text></svg>
```

O que este arquivo faz:

- Fornece uma imagem local editável.


## ARQUIVO: publico/imagens/suporte.svg

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="#e9edf2"/><path d="M130 95l-40 120h210L260 95" fill="none" stroke="#687789" stroke-width="15"/><path d="M100 155h190" stroke="#ff855a" stroke-width="14"/></svg>
```

O que este arquivo faz:

- Fornece uma imagem local editável.


## ARQUIVO: publico/index.html

```html
<!DOCTYPE html>
<html lang="pt-BR">
 <head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1" name="viewport"/>
  <meta content="Dessik: loja fictícia de tecnologia para um projeto acadêmico." name="description"/>
  <title>
   Dessik | Tecnologia para o seu dia a dia
  </title>
  <link href="/imagens/placeholder.svg" rel="icon" type="image/svg+xml"/>
  <link href="/css/style.css" rel="stylesheet"/>
  <link href="/css/storefront.css?v=3" rel="stylesheet"/>
  <script src="/js/loja.js?v=3" type="module">
  </script>
 </head>
 <body class="store-page home-page">
  <a class="skip" href="#main">
   Pular para o conteúdo
  </a>
  <div class="topnote">
   SEU SETUP, SUAS REGRAS.
   <span>
    Loja fictícia · Sem cobranças reais
   </span>
  </div>
  <header class="navbar">
   <div class="nav-inner">
    <a aria-label="Dessik início" class="brand" href="/index.html">
     dessik
     <span>
      .
     </span>
    </a>
    <nav aria-label="Navegação principal">
     <a aria-current="page" href="/index.html">
      Início
     </a>
     <a href="/carrinho.html">
      Carrinho
     </a>
     <a href="/loja.html">
      Explorar produtos
     </a>
     <a data-session="" hidden="" href="/pedidos.html">
      Meus pedidos
     </a>
     <a data-admin="" hidden="" href="/admin.html">
      Administração
     </a>
     <a data-guest="" href="/login.html">
      Entrar
     </a>
     <a class="button secondary" data-guest="" href="/cadastro.html">
      Criar conta
     </a>
     <span class="nav-session" data-session="" hidden="">
      <span data-user="">
      </span>
      <button class="secondary" data-logout="">
       Sair
      </button>
     </span>
    </nav>
   </div>
  </header>
  <main id="main">
   <section aria-labelledby="hero-title" class="hero">
    <div class="hero-copy">
     <p class="collection-label">
      TECNOLOGIA COM A SUA IDENTIDADE
      <span>
       DESSIK / 2026
      </span>
     </p>
     <h1 id="hero-title">
      MENOS LIMITES.
      <br/>
      <em>
       MAIS VOCÊ.
      </em>
     </h1>
     <p>
      Do play ao próximo projeto. Encontre o que falta no seu setup e faça do seu jeito.
     </p>
     <a class="button hero-button" href="/loja.html">
      Ver Produtos
      <span aria-hidden="true">
       ↗
      </span>
     </a>
     <a class="home-register" href="/cadastro.html">
      Criar Conta ↗
     </a>
     <span class="hero-caption">
      ESSENTIALS COLLECTION — 2026
     </span>
    </div>
    <div class="hero-showcase">
     <span class="showcase-kicker">
      EM DESTAQUE / ÁUDIO
     </span>
     <div aria-label="Ilustração do headset Wave preto com detalhes azuis" class="hero-product product-art art-headset" role="img">
     </div>
     <div class="showcase-bottom">
      <div>
       <span>
        OUÇA CADA DETALHE.
       </span>
       <strong>
        Headset Wave
       </strong>
      </div>
      <a aria-label="Explorar produtos" href="#catalogo">
       ↗
      </a>
     </div>
    </div>
   </section>
   <div class="collection-strip">
    <span>
     FEITO PARA O SEU DIA A DIA
    </span>
    <span>
     CRIAR
     <b>
      ✳
     </b>
     TRABALHAR
     <b>
      ✳
     </b>
     JOGAR
     <b>
      ✳
     </b>
     EXPLORAR
    </span>
   </div>
   <div aria-live="polite" class="message" hidden="" id="message" role="status">
   </div>
   <section aria-labelledby="catalog-title" id="catalogo">
    <div class="catalog-bar">
     <div>
      <p class="eyebrow">
       O PRÓXIMO UPGRADE É SEU
      </p>
      <h2 id="catalog-title">
       Produtos em destaque
       <span>
        .
       </span>
      </h2>
      <span aria-live="polite" class="muted" id="product-count">
       Carregando produtos…
      </span>
     </div>
     <button class="secondary" id="reload">
      Atualizar ↻
     </button>
    </div>
    <div class="catalog-tools">
     <label class="search-box">
      <span aria-hidden="true">
       ⌕
      </span>
      <span class="sr-only">
       Buscar produtos
      </span>
      <input autocomplete="off" id="search" maxlength="100" placeholder="O que falta no seu setup?" type="search"/>
     </label>
     <label class="sort-box">
      <span>
       Ordenar por
      </span>
      <select id="sort">
       <option value="recentes">
        Seleção Dessik
       </option>
       <option value="menor-preco">
        Menor preço
       </option>
       <option value="maior-preco">
        Maior preço
       </option>
      </select>
     </label>
    </div>
    <div aria-label="Filtrar por categoria" class="category-tabs" role="group">
     <button aria-pressed="true" data-category="">
      Todos os produtos
     </button>
     <button aria-pressed="false" data-category="Computadores">
      Computadores
     </button>
     <button aria-pressed="false" data-category="Periféricos">
      Periféricos
     </button>
     <button aria-pressed="false" data-category="Monitores">
      Monitores
     </button>
     <button aria-pressed="false" data-category="Áudio">
      Áudio
     </button>
     <button aria-pressed="false" data-category="Acessórios">
      Acessórios
     </button>
     <button aria-pressed="false" data-category="Componentes">
      Componentes
     </button>
    </div>
    <div aria-busy="true" class="grid" id="products">
    </div>
    <div class="pagination">
     <button class="secondary" disabled="" id="previous">
      Anterior
     </button>
     <span id="page-number">
      Página 1
     </span>
     <button class="secondary" disabled="" id="next">
      Próxima
     </button>
    </div>
   </section>
   <section aria-label="Benefícios da loja" class="benefits">
    <article>
     <span>
      01 / ESCOLHA
     </span>
     <h2>
      Seu próximo upgrade.
     </h2>
     <p>
      Tecnologia para estudar, criar e jogar, em um só lugar.
     </p>
    </article>
    <article>
     <span>
      02 / CONFIANÇA
     </span>
     <h2>
      Conta protegida.
     </h2>
     <p>
      Senhas protegidas e acesso exclusivo aos seus pedidos.
     </p>
    </article>
    <article>
     <span>
      03 / TRANQUILIDADE
     </span>
     <h2>
      Experimente à vontade.
     </h2>
     <p>
      Uma loja acadêmica com compras simuladas, sem cobrança.
     </p>
    </article>
   </section>
  </main>
  <dialog aria-labelledby="dialog-title" id="confirm-dialog">
   <h2 id="dialog-title">
   </h2>
   <p>
   </p>
   <form class="actions" method="dialog">
    <button autofocus="" class="secondary" value="cancel">
     Cancelar
    </button>
    <button value="confirm">
     Confirmar
    </button>
   </form>
  </dialog>
  <footer>
   <div class="footer-main">
    <div>
     <a class="brand" href="/index.html">
      dessik
      <span>
       .
      </span>
     </a>
     <p>
      Tecnologia para quem faz
      <br/>
      do próprio jeito.
     </p>
    </div>
    <div class="footer-links">
     <a href="/loja.html">
      Explorar produtos
     </a>
     <a href="/login.html">
      Minha conta
     </a>
     <a href="/cadastro.html">
      Criar conta
     </a>
    </div>
   </div>
   <div class="footer-bottom">
    <span>
     © 2026 Dessik. Projeto acadêmico.
    </span>
    <span>
     Produtos fictícios. Compras simuladas. Nenhuma cobrança.
    </span>
   </div>
  </footer>
 </body>
</html>
```

O que este arquivo faz:

- Apresenta a loja, carrega quatro produtos da API e mostra os benefícios.


## ARQUIVO: publico/js/admin.js

```javascript
import {
    apiRequest,
    message,
    money,
    element,
    setupSession,
    confirmAction
} from './api.js';
const form = document.querySelector('#product-form');
const table = document.querySelector('#product-rows');
let editing = null;
let offset = 0;
const limit = 20;

function resetForm() {
    form.reset();
    editing = null;
    document.querySelector('#form-title').textContent = 'Novo produto';
    document.querySelector('#save-product').textContent = 'Cadastrar produto';
}
async function loadProducts() {
    const products = await apiRequest(`/produtos?limite=${limit}&offset=${offset}`);
    table.replaceChildren();
    for (const product of products) {
        const row = element('tr');
        row.append(element('td', `#${product.id_produto} ${product.nome}`), element('td', money(product.preco)),
            element('td', String(product.quantidade_estoque)));
        const actions = element('td');
        const edit = element('button', 'Editar', 'secondary');
        edit.setAttribute('aria-label', `Editar ${product.nome}`);
        edit.onclick = () => {
            editing = product.id_produto;
            for (const key of ['nome', 'descricao', 'categoria', 'preco', 'quantidade_estoque', 'imagem_url']) form.elements[key].value = product[key];
            document.querySelector('#form-title').textContent = `Editar produto #${editing}`;
            document.querySelector('#save-product').textContent = 'Salvar alterações';
            form.elements.nome.focus();
        };
        const remove = element('button', 'Excluir', 'danger');
        remove.setAttribute('aria-label', `Excluir ${product.nome}`);
        remove.onclick = async () => {
            if (!await confirmAction('Excluir produto?', `O produto ${product.nome} será removido do catálogo.`, 'Excluir')) return;
            remove.disabled = true;
            try {
                await apiRequest(`/produtos/${product.id_produto}`, {
                    method: 'DELETE',
                    auth: true
                });
                if (editing === product.id_produto) resetForm();
                message('Produto excluído.', 'success');
                await loadProducts();
            } catch (error) {
                message(error.message);
            } finally {
                remove.disabled = false;
            }
        };
        actions.append(edit, remove);
        row.append(actions);
        table.append(row);
    }
    if (!products.length) {
        const row = element('tr');
        const cell = element('td', 'Nenhum produto nesta página.');
        cell.colSpan = 4;
        row.append(cell);
        table.append(row);
    }
    document.querySelector('#previous').disabled = offset === 0;
    document.querySelector('#next').disabled = products.length < limit;
    document.querySelector('#page-number').textContent = `Página ${offset / limit + 1}`;
}
async function refresh() {
    try {
        await loadProducts();
    } catch (error) {
        message(error.message);
    }
}
form.addEventListener('submit', async event => {
    event.preventDefault();
    const button = document.querySelector('#save-product');
    button.disabled = true;
    try {
        const body = Object.fromEntries(new FormData(form));
        body.quantidade_estoque = Number(body.quantidade_estoque);
        const data = await apiRequest(editing ? `/produtos/${editing}` : '/produtos', {
            method: editing ? 'PUT' : 'POST',
            auth: true,
            body
        });
        resetForm();
        message(data.mensagem, 'success');
        await refresh();
    } catch (error) {
        message(error.message);
    } finally {
        button.disabled = false;
    }
});
document.querySelector('#cancel-edit').onclick = resetForm;
document.querySelector('#previous').onclick = () => {
    offset = Math.max(0, offset - limit);
    refresh();
};
document.querySelector('#next').onclick = () => {
    offset += limit;
    refresh();
};
const user = await setupSession(true, true);
if (user) {
    document.querySelector('#admin-content').hidden = false;
    await refresh();
}
```

O que este arquivo faz:

- Envia requisições para criar, atualizar e excluir produtos.


## ARQUIVO: publico/js/api.js

```javascript
export const API_URL = "/api"; // Mesma origem. Em hospedagens separadas, use a URL HTTPS da API.
export const money = value => Number(value).toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL'
});

export async function apiRequest(path, {
    method = 'GET',
    body,
    auth = false
} = {}) {
    const headers = {};
    if (body !== undefined) headers['Content-Type'] = 'application/json';
    if (auth) {
        const token = sessionStorage.getItem('dessik_token');
        if (!token) throw new Error('Entre na sua conta para continuar.');
        headers.Authorization = `Bearer ${token}`;
    }
    let response;
    try {
        response = await fetch(`${API_URL}${path}`, {
            method,
            headers,
            cache: 'no-store',
            body: body === undefined ? undefined : JSON.stringify(body)
        });
    } catch {
        throw new Error('Sem conexão com a loja. Verifique sua internet e tente novamente.');
    }
    let data;
    try {
        data = await response.json();
    } catch {
        throw new Error('O servidor não respondeu corretamente. Tente novamente.');
    }
    if (!response.ok) {
        if (response.status === 401 && auth) sessionStorage.removeItem('dessik_token');
        const detail = data.erros?.map(item => `${item.campo || 'Dados'}: ${item.mensagem}`).join(' ');
        const error = new Error(detail || data.mensagem || 'Não foi possível concluir a operação.');
        error.status = response.status;
        throw error;
    }
    return data;
}

export function message(text = '', kind = 'error', target = document.querySelector('#message')) {
    target.textContent = text;
    target.className = `message ${kind}`;
    target.hidden = !text;
}

export function element(tag, text, className) {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = text; // Dados do banco nunca viram HTML executável.
    if (className) node.className = className;
    return node;
}

export async function setupSession(required = false, admin = false) {
    if (sessionStorage.getItem('dessik_login_ok')) {
        sessionStorage.removeItem('dessik_login_ok');
        message('Login realizado com sucesso.', 'success');
    }
    const token = sessionStorage.getItem('dessik_token');
    if (!token) {
        if (required) location.replace('/login.html');
        return null;
    }
    try {
        const user = await apiRequest('/me', {
            auth: true
        });
        document.querySelectorAll('[data-guest]').forEach(el => el.hidden = true);
        document.querySelectorAll('[data-session]').forEach(el => el.hidden = false);
        document.querySelectorAll('[data-admin]').forEach(el => el.hidden = !user.is_admin);
        document.querySelectorAll('[data-user]').forEach(el => el.textContent = user.nome.split(' ')[0]);
        document.querySelectorAll('[data-logout]').forEach(el => el.onclick = () => {
            sessionStorage.removeItem('dessik_token');
            location.assign('/login.html');
        });
        if (admin && !user.is_admin) throw new Error('Esta área está disponível apenas para administradores.');
        return user;
    } catch (error) {
        if (error.status === 401) {
            sessionStorage.removeItem('dessik_token');
            if (required) location.replace('/login.html');
        }
        if (required) message(error.message);
        return null;
    }
}

export function confirmAction(title, description, action = 'Confirmar') {
    return new Promise(resolve => {
        const dialog = document.querySelector('#confirm-dialog');
        dialog.querySelector('h2').textContent = title;
        dialog.querySelector('p').textContent = description;
        dialog.querySelector('[value="confirm"]').textContent = action;
        dialog.returnValue = 'cancel';
        dialog.addEventListener('close', () => resolve(dialog.returnValue === 'confirm'), {
            once: true
        });
        dialog.showModal();
    });
}
```

O que este arquivo faz:

- Centraliza a URL da API, fetch, mensagens, sessão e elementos com textContent.


## ARQUIVO: publico/js/cadastro.js

```javascript
import {
    apiRequest,
    message,
    setupSession
} from './api.js';
setupSession();
const form = document.querySelector('#register-form');
const cepMessage = document.querySelector('#cep-message');
const senha = form.elements.senha;
const confirmation = form.elements.confirmar_senha;

function validatePasswords() {
    confirmation.setCustomValidity(confirmation.value && confirmation.value !== senha.value ? 'As senhas não coincidem.' : '');
    senha.setCustomValidity(new TextEncoder().encode(senha.value).length > 72 ? 'Use no máximo 72 bytes na senha.' : '');
}
senha.addEventListener('input', validatePasswords);
confirmation.addEventListener('input', validatePasswords);
document.querySelector('#generate-password').addEventListener('click', async event => {
    const button = event.currentTarget;
    button.disabled = true;
    try {
        const data = await apiRequest('/gerar-senha');
        senha.value = confirmation.value = data.senha;
        senha.type = 'text';
        validatePasswords();
        message('Senha sugerida preenchida. Guarde-a antes de cadastrar.', 'success');
    } catch (error) {
        message(error.message);
    } finally {
        button.disabled = false;
    }
});
document.querySelector('#lookup-cep').addEventListener('click', async event => {
    const value = form.elements.cep.value.replace(/\D/g, '');
    if (value.length !== 8) return message('Informe os 8 números do CEP.', 'error', cepMessage);
    const button = event.currentTarget;
    button.disabled = true;
    message('Consultando CEP…', '', cepMessage);
    try {
        const address = await apiRequest(`/cep/${value}`);
        // Não substitui um endereço caso o usuário tenha alterado o CEP durante a consulta.
        if (form.elements.cep.value.replace(/\D/g, '') !== value) return;
        for (const key of ['logradouro', 'bairro', 'cidade', 'estado']) form.elements[key].value = address[key];
        message('Endereço encontrado. Confira os dados abaixo.', 'success', cepMessage);
    } catch (error) {
        message(error.message, 'error', cepMessage);
    } finally {
        button.disabled = false;
    }
});
form.addEventListener('submit', async event => {
    event.preventDefault();
    validatePasswords();
    if (!form.reportValidity()) return;
    const button = form.querySelector('[type="submit"]');
    button.disabled = true;
    message();
    try {
        const body = Object.fromEntries(new FormData(form));
        body.cep = body.cep.replace(/\D/g, '');
        await apiRequest('/cadastro', {
            method: 'POST',
            body
        });
        location.assign('/login.html?cadastro=ok');
    } catch (error) {
        message(error.message);
    } finally {
        button.disabled = false;
    }
});

// Ao sair do campo, consulta automaticamente um CEP completo.
form.elements.cep.addEventListener('blur', () => {
    if (form.elements.cep.value.replace(/\D/g, '').length === 8) document.querySelector('#lookup-cep').click();
});
```

O que este arquivo faz:

- Valida o formulário, sugere senha e consulta ViaCEP por meio da API.


## ARQUIVO: publico/js/carrinho.js

```javascript
import {
    apiRequest,
    element,
    message,
    money,
    setupSession
} from './api.js';

// Apenas IDs e quantidades: o preço verdadeiro será consultado na API.
export function lerCarrinho() {
    try {
        const itens = JSON.parse(sessionStorage.getItem('dessik_carrinho') || '[]');
        if (!Array.isArray(itens)) return [];
        const validos = [];
        for (const item of itens) {
            if (Number.isInteger(item.id_produto) && item.id_produto > 0 &&
                Number.isInteger(item.quantidade) && item.quantidade > 0 && item.quantidade <= 1000 &&
                !validos.some(outro => outro.id_produto === item.id_produto)) validos.push(item);
        }
        return validos.slice(0, 50);
    } catch {
        return [];
    }
}

function salvarCarrinho(itens) {
    sessionStorage.setItem('dessik_carrinho', JSON.stringify(itens));
}
export function adicionarProduto(produto, quantidade) {
    const itens = lerCarrinho();
    const existente = itens.find(item => item.id_produto === produto.id_produto);
    const total = (existente?.quantidade || 0) + quantidade;
    if (!Number.isInteger(quantidade) || quantidade < 1 || total > Math.min(produto.quantidade_estoque, 1000)) {
        throw new Error('Estoque insuficiente para essa quantidade no carrinho.');
    }
    if (existente) existente.quantidade = total;
    else {
        if (itens.length >= 50) throw new Error('O carrinho aceita até 50 produtos diferentes.');
        itens.push({
            id_produto: produto.id_produto,
            quantidade
        });
    }
    salvarCarrinho(itens);
}

async function iniciarCarrinho() {
    await setupSession();
    const lista = document.querySelector('#cart-items');
    const finalizar = document.querySelector('#checkout');
    let enviando = false;
    let atualizando = false;
    async function mostrarCarrinho() {
        if (atualizando || enviando) return;
        atualizando = true;
        document.querySelector('#refresh-cart').disabled = true;
        finalizar.disabled = true;
        lista.replaceChildren();
        const itens = lerCarrinho();
        let totalCentavos = 0;
        let valido = itens.length > 0;
        for (const item of itens) {
            const linha = element('article', undefined, 'cart-item');
            const detalhes = element('div');
            try {
                const produto = await apiRequest(`/produtos/${item.id_produto}`);
                const subtotal = Math.round(Number(produto.preco) * 100) * item.quantidade;
                totalCentavos += subtotal;
                detalhes.append(element('h2', produto.nome), element('p', `${money(produto.preco)} por unidade`));
                const label = element('label', 'Quantidade');
                const quantidade = element('input');
                quantidade.type = 'number';
                quantidade.min = '1';
                quantidade.max = String(Math.min(produto.quantidade_estoque, 1000));
                quantidade.value = String(item.quantidade);
                quantidade.addEventListener('change', async () => {
                    const valor = Number(quantidade.value);
                    if (!Number.isInteger(valor) || !quantidade.reportValidity()) return;
                    const atuais = lerCarrinho();
                    const atual = atuais.find(p => p.id_produto === item.id_produto);
                    if (atual) atual.quantidade = valor;
                    salvarCarrinho(atuais);
                    await mostrarCarrinho();
                });
                label.append(quantidade);
                detalhes.append(label);
                if (item.quantidade > produto.quantidade_estoque) {
                    valido = false;
                    detalhes.append(element('p', `Estoque insuficiente. Disponível: ${produto.quantidade_estoque}. Ajuste a quantidade ou remova o item.`, 'stock out'));
                }
                linha.append(detalhes, element('strong', money(subtotal / 100)));
            } catch (erro) {
                valido = false;
                linha.append(element('p', `Produto #${item.id_produto}: ${erro.message}`));
            }
            const remover = element('button', 'Remover', 'secondary');
            remover.addEventListener('click', async () => {
                salvarCarrinho(lerCarrinho().filter(p => p.id_produto !== item.id_produto));
                await mostrarCarrinho();
            });
            linha.append(remover);
            linha.querySelectorAll('button, input').forEach(campo => campo.disabled = true);
            lista.append(linha);
        }
        if (!itens.length) lista.append(element('p', 'Seu carrinho está vazio. Explore a loja para começar.', 'empty'));
        document.querySelector('#cart-total').textContent = money(totalCentavos / 100);
        finalizar.disabled = !valido || enviando;
        atualizando = false;
        lista.querySelectorAll('button, input').forEach(campo => campo.disabled = false);
        document.querySelector('#refresh-cart').disabled = false;
    }
    finalizar.addEventListener('click', async () => {
        if (enviando) return;
        if (!sessionStorage.getItem('dessik_token')) {
            message('Entre na sua conta para finalizar. Seus itens ficam guardados nesta aba.');
            document.querySelector('#cart-login').hidden = false;
            return;
        }
        enviando = true;
        finalizar.disabled = true;
        finalizar.textContent = 'Finalizando...';
        lista.querySelectorAll('button, input').forEach(campo => campo.disabled = true);
        try {
            const pedido = await apiRequest('/pedidos', {
                method: 'POST',
                auth: true,
                body: {
                    itens: lerCarrinho()
                }
            });
            salvarCarrinho([]);
            message(`Pedido #${pedido.id_pedido} realizado! Total: ${money(pedido.valor_total)}. Nenhuma cobrança.`, 'success');
        } catch (erro) {
            message(erro.message + ' Se houve perda de conexão, confira Meus pedidos antes de tentar novamente.');
        } finally {
            enviando = false;
            finalizar.textContent = 'Finalizar pedido';
            await mostrarCarrinho();
        }
    });
    document.querySelector('#refresh-cart').onclick = mostrarCarrinho;
    await mostrarCarrinho();
}
if (document.querySelector('#cart-items')) iniciarCarrinho().catch(erro => message(erro.message));
```

O que este arquivo faz:

- Guarda IDs e quantidades na aba, consulta preços e envia todos os itens do pedido.


## ARQUIVO: publico/js/login.js

```javascript
import {
    apiRequest,
    message,
    setupSession
} from './api.js';
setupSession();
if (new URLSearchParams(location.search).get('cadastro') === 'ok') {
    message('Conta criada com sucesso. Entre para começar.', 'success');
}
document.querySelector('#login-form').addEventListener('submit', async event => {
    event.preventDefault();
    const form = event.currentTarget;
    const button = form.querySelector('[type="submit"]');
    button.disabled = true;
    message();
    try {
        const data = await apiRequest('/login', {
            method: 'POST',
            body: Object.fromEntries(new FormData(form))
        });
        sessionStorage.setItem('dessik_token', data.access_token);
        sessionStorage.setItem('dessik_login_ok', '1');
        location.assign(sessionStorage.getItem('dessik_carrinho') ? '/carrinho.html' : '/loja.html');
    } catch (error) {
        message(error.message);
    } finally {
        button.disabled = false;
    }
});
```

O que este arquivo faz:

- Autentica e guarda o JWT temporário na sessão da aba.


## ARQUIVO: publico/js/loja.js

```javascript
import {
    adicionarProduto
} from './carrinho.js';
import {
    apiRequest,
    message,
    money,
    element,
    setupSession
} from './api.js';
setupSession();
const grid = document.querySelector('#products');
let offset = 0;
const limit = document.body.classList.contains('home-page') ? 4 : 12;
let category = '';
let requestVersion = 0;
const search = document.querySelector('#search');
const sort = document.querySelector('#sort');
const productArt = new Map([
    ['Notebook Horizon 14', 'notebook'],
    ['Mouse Pulse', 'mouse'],
    ['Teclado mecânico Type', 'teclado'],
    ['Monitor View 24', 'monitor'],
    ['Headset Wave', 'headset'],
    ['Webcam Focus', 'webcam'],
    ['SSD Sprint 1 TB', 'ssd'],
    ['Memória RAM Flux 16 GB', 'ram'],
]);

function card(product) {
    const article = element('article', undefined, 'card');
    const visual = element('div', undefined, 'product-visual');
    const image = element('img');
    image.src = product.imagem_url;
    image.alt = product.nome;
    image.loading = 'lazy';
    image.addEventListener('error', () => image.src = '/imagens/placeholder.svg', {
        once: true
    });
    const art = productArt.get(product.nome);
    if (art && ['/imagens/placeholder.svg', '/imagens/catalogo-dessik.png'].includes(product.imagem_url)) {
        const sprite = element('div', undefined, `product-art art-${art}`);
        sprite.setAttribute('role', 'img');
        sprite.setAttribute('aria-label', `Ilustração de ${product.nome}`);
        visual.append(sprite);
    } else visual.append(image);
    visual.append(element('span', product.quantidade_estoque ? 'DESSIK / ESSENTIALS' : 'ESGOTADO', 'product-tag'));
    const body = element('div', undefined, 'card-body');
    body.append(element('p', product.categoria, 'category'),
        element('h3', product.nome), element('p', product.descricao, 'description'),
        element('p', money(product.preco), 'price'),
        element('p', product.quantidade_estoque ? (product.quantidade_estoque <= 3 ? `Últimas ${product.quantidade_estoque} unidades` : `Estoque: ${product.quantidade_estoque} unidades`) : 'Produto indisponível',
            product.quantidade_estoque ? 'stock' : 'stock out'));
    const row = element('div', undefined, 'buy-row');
    const quantity = element('input');
    quantity.type = 'number';
    quantity.min = '1';
    quantity.max = String(Math.min(product.quantidade_estoque, 1000));
    quantity.value = '1';
    quantity.setAttribute('aria-label', `Quantidade de ${product.nome}`);
    quantity.disabled = product.quantidade_estoque === 0;
    const button = element('button', product.quantidade_estoque ? 'Comprar ↗' : 'Indisponível');
    button.disabled = product.quantidade_estoque === 0;
    button.addEventListener('click', async () => {
        try {
            if (!quantity.reportValidity()) return;
            adicionarProduto(product, Number(quantity.value));
            message('Produto adicionado ao carrinho.', 'success');
            document.querySelector('#message').scrollIntoView({
                block: 'nearest'
            });
        } catch (error) {
            message(error.message);
        }
    });
    row.append(quantity, button);
    body.append(row);
    article.append(visual, body);
    return article;
}
async function loadProducts(clear = true) {
    const version = ++requestVersion;
    if (clear) message();
    grid.setAttribute('aria-busy', 'true');
    try {
        let products;
        const filters = new URLSearchParams({
            busca: search.value.trim(),
            categoria: category,
            ordem: sort.value
        });
        products = await apiRequest(`/produtos?limite=${limit}&offset=${offset}&${filters}`);
        if (version !== requestVersion) return;
        grid.replaceChildren(...products.map(card));
        if (!products.length) grid.append(element('p', 'Nenhum produto encontrado. Experimente outra busca ou categoria.', 'empty'));
        document.querySelector('#product-count').textContent = `${products.length} produtos nesta seleção`;
        document.querySelector('#previous').disabled = offset === 0;
        document.querySelector('#next').disabled = products.length < limit;
        document.querySelector('#page-number').textContent = `Página ${offset / limit + 1}`;
    } catch (error) {
        if (version !== requestVersion) return;
        grid.replaceChildren(element('p', 'Não foi possível carregar o catálogo.', 'empty'));
        message(error.message);
    } finally {
        if (version === requestVersion) grid.setAttribute('aria-busy', 'false');
    }
}
let searchTimer;
search.addEventListener('input', () => {
    clearTimeout(searchTimer);
    // Invalida resultados anteriores ainda em trânsito antes da próxima busca.
    requestVersion++;
    searchTimer = setTimeout(() => {
        offset = 0;
        loadProducts();
    }, 250);
});
sort.addEventListener('change', () => {
    offset = 0;
    loadProducts();
});
document.querySelectorAll('[data-category]').forEach(button => button.addEventListener('click', () => {
    category = button.dataset.category;
    document.querySelectorAll('[data-category]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    offset = 0;
    loadProducts();
}));
document.querySelector('#previous').onclick = () => {
    offset = Math.max(0, offset - limit);
    loadProducts();
};
document.querySelector('#next').onclick = () => {
    offset += limit;
    loadProducts();
};
document.querySelector('#reload').onclick = () => {
    offset = 0;
    loadProducts();
};
loadProducts();
```

O que este arquivo faz:

- Consulta produtos, cria cards, mostra estoque e adiciona ao carrinho.


## ARQUIVO: publico/js/pedidos.js

```javascript
import {
    apiRequest,
    setupSession,
    element,
    money,
    message
} from './api.js';

const content = document.querySelector('#orders-content');
const list = document.querySelector('#orders-list');
const reload = document.querySelector('#reload-orders');

async function loadOrders() {
    reload.disabled = true;
    list.setAttribute('aria-busy', 'true');
    message();
    try {
        const orders = await apiRequest('/pedidos', {
            auth: true
        });
        list.replaceChildren();
        if (!orders.length) {
            const empty = element('div', undefined, 'empty');
            const link = element('a', 'Explorar produtos ↗', 'button');
            link.href = '/loja.html';
            empty.append(element('h2', 'Seu primeiro upgrade começa aqui.'),
                element('p', 'Você ainda não fez nenhuma compra simulada.'), link);
            list.append(empty);
        }
        for (const order of orders) {
            const card = element('article', undefined, 'order-card');
            const date = new Date(order.data_pedido);
            const heading = element('div');
            heading.append(element('p', `PEDIDO #${order.id_pedido}`, 'eyebrow'),
                element('h2', money(order.valor_total)));
            const details = element('div');
            details.append(element('p', Number.isNaN(date.getTime()) ? 'Data não disponível' : date.toLocaleString('pt-BR')),
                element('span', 'Compra simulada • Sem cobrança', 'order-status'));
            card.append(heading, details);
            list.append(card);
        }
        document.querySelector('#order-count').textContent = `${orders.length} pedidos • até os 100 mais recentes`;
    } catch (error) {
        message(error.message);
    } finally {
        reload.disabled = false;
        list.setAttribute('aria-busy', 'false');
    }
}

reload.addEventListener('click', loadOrders);
if (await setupSession(true)) {
    content.hidden = false;
    await loadOrders();
}
```

O que este arquivo faz:

- Consulta e exibe os próprios pedidos.


## ARQUIVO: publico/login.html

```html
<!DOCTYPE html>
<html lang="pt-BR">
 <head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1" name="viewport"/>
  <meta content="Dessik: loja fictícia de tecnologia para um projeto acadêmico." name="description"/>
  <title>
   Entrar | Dessik
  </title>
  <link href="/imagens/placeholder.svg" rel="icon" type="image/svg+xml"/>
  <link href="/css/style.css" rel="stylesheet"/>
  <link href="/css/storefront.css?v=3" rel="stylesheet"/>
  <script src="/js/login.js" type="module">
  </script>
 </head>
 <body class="account-page">
  <a class="skip" href="#main">
   Pular para o conteúdo
  </a>
  <div class="topnote">
   SEU SETUP, SUAS REGRAS.
   <span>
    Loja fictícia · Sem cobranças reais
   </span>
  </div>
  <header class="navbar">
   <div class="nav-inner">
    <a aria-label="Dessik início" class="brand" href="/index.html">
     dessik
     <span>
      .
     </span>
    </a>
    <nav aria-label="Navegação principal">
     <a href="/index.html">
      Início
     </a>
     <a href="/carrinho.html">
      Carrinho
     </a>
     <a href="/loja.html">
      Produtos
     </a>
     <a data-session="" hidden="" href="/pedidos.html">
      Meus pedidos
     </a>
     <a data-admin="" hidden="" href="/admin.html">
      Administração
     </a>
     <a data-guest="" href="/login.html">
      Entrar
     </a>
     <a class="button secondary" data-guest="" href="/cadastro.html">
      Criar conta
     </a>
     <span class="nav-session" data-session="" hidden="">
      <span data-user="">
      </span>
      <button class="secondary" data-logout="">
       Sair
      </button>
     </span>
    </nav>
   </div>
  </header>
  <main id="main">
   <div class="form-layout">
    <section class="form-intro">
     <p class="eyebrow">
      Bom ter você de volta
     </p>
     <h1>
      Seu setup começa
      <br/>
      por aqui.
     </h1>
     <p>
      Entre na sua conta para explorar os produtos e simular sua próxima compra.
     </p>
     <a href="/loja.html">
      ← Continuar explorando
     </a>
    </section>
    <section class="form-panel">
     <h2>
      Entrar na conta
     </h2>
     <div aria-live="polite" class="message" hidden="" id="message" role="status">
     </div>
     <form id="login-form">
      <div class="fields">
       <label>
        E-mail
        <input autocomplete="email" maxlength="254" name="email" required="" type="email"/>
       </label>
       <label>
        Senha
        <input autocomplete="current-password" maxlength="72" name="senha" required="" type="password"/>
       </label>
      </div>
      <div class="actions">
       <button class="full" type="submit">
        Entrar
       </button>
      </div>
     </form>
     <p class="form-foot">
      Ainda não tem conta?
      <a href="/cadastro.html">
       Cadastre-se
      </a>
     </p>
    </section>
   </div>
  </main>
  <dialog aria-labelledby="dialog-title" id="confirm-dialog">
   <h2 id="dialog-title">
   </h2>
   <p>
   </p>
   <form class="actions" method="dialog">
    <button autofocus="" class="secondary" value="cancel">
     Cancelar
    </button>
    <button value="confirm">
     Confirmar
    </button>
   </form>
  </dialog>
  <footer>
   <div class="footer-main">
    <div>
     <a class="brand" href="/index.html">
      dessik
      <span>
       .
      </span>
     </a>
     <p>
      Tecnologia para quem faz
      <br/>
      do próprio jeito.
     </p>
    </div>
    <div class="footer-links">
     <a href="/loja.html">
      Explorar produtos
     </a>
     <a href="/login.html">
      Minha conta
     </a>
     <a href="/cadastro.html">
      Criar conta
     </a>
    </div>
   </div>
   <div class="footer-bottom">
    <span>
     © 2026 Dessik. Projeto acadêmico.
    </span>
    <span>
     Produtos fictícios. Compras simuladas. Nenhuma cobrança.
    </span>
   </div>
  </footer>
 </body>
</html>
```

O que este arquivo faz:

- Mostra os campos de e-mail e senha.


## ARQUIVO: publico/loja.html

```html
<!DOCTYPE html>
<html lang="pt-BR">
 <head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1" name="viewport"/>
  <meta content="Dessik: loja fictícia de tecnologia para um projeto acadêmico." name="description"/>
  <title>
   Loja | Dessik
  </title>
  <link href="/imagens/placeholder.svg" rel="icon" type="image/svg+xml"/>
  <link href="/css/style.css" rel="stylesheet"/>
  <link href="/css/storefront.css?v=3" rel="stylesheet"/>
  <script src="/js/loja.js?v=3" type="module">
  </script>
 </head>
 <body class="store-page">
  <a class="skip" href="#main">
   Pular para o conteúdo
  </a>
  <div class="topnote">
   SEU SETUP, SUAS REGRAS.
   <span>
    Loja fictícia · Sem cobranças reais
   </span>
  </div>
  <header class="navbar">
   <div class="nav-inner">
    <a aria-label="Dessik início" class="brand" href="/index.html">
     dessik
     <span>
      .
     </span>
    </a>
    <nav aria-label="Navegação principal">
     <a href="/index.html">
      Início
     </a>
     <a href="/carrinho.html">
      Carrinho
     </a>
     <a aria-current="page" href="/loja.html">
      Explorar produtos
     </a>
     <a data-session="" hidden="" href="/pedidos.html">
      Meus pedidos
     </a>
     <a data-admin="" hidden="" href="/admin.html">
      Administração
     </a>
     <a data-guest="" href="/login.html">
      Entrar
     </a>
     <a class="button secondary" data-guest="" href="/cadastro.html">
      Criar conta
     </a>
     <span class="nav-session" data-session="" hidden="">
      <span data-user="">
      </span>
      <button class="secondary" data-logout="">
       Sair
      </button>
     </span>
    </nav>
   </div>
  </header>
  <main id="main">
   <section aria-labelledby="hero-title" class="hero">
    <div class="hero-copy">
     <p class="collection-label">
      TECNOLOGIA COM A SUA IDENTIDADE
      <span>
       DESSIK / 2026
      </span>
     </p>
     <h1 id="hero-title">
      MENOS LIMITES.
      <br/>
      <em>
       MAIS VOCÊ.
      </em>
     </h1>
     <p>
      Do play ao próximo projeto. Encontre o que falta no seu setup e faça do seu jeito.
     </p>
     <a class="button hero-button" href="#catalogo">
      Explorar coleção
      <span aria-hidden="true">
       ↗
      </span>
     </a>
     <span class="hero-caption">
      ESSENTIALS COLLECTION — 2026
     </span>
    </div>
    <div class="hero-showcase">
     <span class="showcase-kicker">
      EM DESTAQUE / ÁUDIO
     </span>
     <div aria-label="Ilustração do headset Wave preto com detalhes azuis" class="hero-product product-art art-headset" role="img">
     </div>
     <div class="showcase-bottom">
      <div>
       <span>
        OUÇA CADA DETALHE.
       </span>
       <strong>
        Headset Wave
       </strong>
      </div>
      <a aria-label="Explorar produtos" href="#catalogo">
       ↗
      </a>
     </div>
    </div>
   </section>
   <div class="collection-strip">
    <span>
     FEITO PARA O SEU DIA A DIA
    </span>
    <span>
     CRIAR
     <b>
      ✳
     </b>
     TRABALHAR
     <b>
      ✳
     </b>
     JOGAR
     <b>
      ✳
     </b>
     EXPLORAR
    </span>
   </div>
   <div aria-live="polite" class="message" hidden="" id="message" role="status">
   </div>
   <section aria-labelledby="catalog-title" id="catalogo">
    <div class="catalog-bar">
     <div>
      <p class="eyebrow">
       O PRÓXIMO UPGRADE É SEU
      </p>
      <h2 id="catalog-title">
       Encontre seu essencial
       <span>
        .
       </span>
      </h2>
      <span aria-live="polite" class="muted" id="product-count">
       Carregando produtos…
      </span>
     </div>
     <button class="secondary" id="reload">
      Atualizar ↻
     </button>
    </div>
    <div class="catalog-tools">
     <label class="search-box">
      <span aria-hidden="true">
       ⌕
      </span>
      <span class="sr-only">
       Buscar produtos
      </span>
      <input autocomplete="off" id="search" maxlength="100" placeholder="O que falta no seu setup?" type="search"/>
     </label>
     <label class="sort-box">
      <span>
       Ordenar por
      </span>
      <select id="sort">
       <option value="recentes">
        Seleção Dessik
       </option>
       <option value="menor-preco">
        Menor preço
       </option>
       <option value="maior-preco">
        Maior preço
       </option>
      </select>
     </label>
    </div>
    <div aria-label="Filtrar por categoria" class="category-tabs" role="group">
     <button aria-pressed="true" data-category="">
      Todos os produtos
     </button>
     <button aria-pressed="false" data-category="Computadores">
      Computadores
     </button>
     <button aria-pressed="false" data-category="Periféricos">
      Periféricos
     </button>
     <button aria-pressed="false" data-category="Monitores">
      Monitores
     </button>
     <button aria-pressed="false" data-category="Áudio">
      Áudio
     </button>
     <button aria-pressed="false" data-category="Acessórios">
      Acessórios
     </button>
     <button aria-pressed="false" data-category="Componentes">
      Componentes
     </button>
    </div>
    <div aria-busy="true" class="grid" id="products">
    </div>
    <div class="pagination">
     <button class="secondary" disabled="" id="previous">
      Anterior
     </button>
     <span id="page-number">
      Página 1
     </span>
     <button class="secondary" disabled="" id="next">
      Próxima
     </button>
    </div>
   </section>
  </main>
  <dialog aria-labelledby="dialog-title" id="confirm-dialog">
   <h2 id="dialog-title">
   </h2>
   <p>
   </p>
   <form class="actions" method="dialog">
    <button autofocus="" class="secondary" value="cancel">
     Cancelar
    </button>
    <button value="confirm">
     Confirmar
    </button>
   </form>
  </dialog>
  <footer>
   <div class="footer-main">
    <div>
     <a class="brand" href="/index.html">
      dessik
      <span>
       .
      </span>
     </a>
     <p>
      Tecnologia para quem faz
      <br/>
      do próprio jeito.
     </p>
    </div>
    <div class="footer-links">
     <a href="/loja.html">
      Explorar produtos
     </a>
     <a href="/login.html">
      Minha conta
     </a>
     <a href="/cadastro.html">
      Criar conta
     </a>
    </div>
   </div>
   <div class="footer-bottom">
    <span>
     © 2026 Dessik. Projeto acadêmico.
    </span>
    <span>
     Produtos fictícios. Compras simuladas. Nenhuma cobrança.
    </span>
   </div>
  </footer>
 </body>
</html>
```

O que este arquivo faz:

- Organiza a vitrine, a busca e as categorias. Os cards são criados pelo JavaScript.


## ARQUIVO: publico/pedidos.html

```html
<!DOCTYPE html>
<html lang="pt-BR">
 <head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1" name="viewport"/>
  <meta content="Dessik: loja fictícia de tecnologia para um projeto acadêmico." name="description"/>
  <title>
   Meus pedidos | Dessik
  </title>
  <link href="/imagens/placeholder.svg" rel="icon" type="image/svg+xml"/>
  <link href="/css/style.css" rel="stylesheet"/>
  <link href="/css/storefront.css?v=3" rel="stylesheet"/>
  <script src="/js/pedidos.js" type="module">
  </script>
 </head>
 <body class="account-page">
  <a class="skip" href="#main">
   Pular para o conteúdo
  </a>
  <div class="topnote">
   SEU SETUP, SUAS REGRAS.
   <span>
    Loja fictícia · Sem cobranças reais
   </span>
  </div>
  <header class="navbar">
   <div class="nav-inner">
    <a aria-label="Dessik início" class="brand" href="/index.html">
     dessik
     <span>
      .
     </span>
    </a>
    <nav aria-label="Navegação principal">
     <a href="/index.html">
      Início
     </a>
     <a href="/carrinho.html">
      Carrinho
     </a>
     <a aria-current="page" href="/loja.html">
      Explorar produtos
     </a>
     <a data-session="" hidden="" href="/pedidos.html">
      Meus pedidos
     </a>
     <a data-admin="" hidden="" href="/admin.html">
      Administração
     </a>
     <a data-guest="" href="/login.html">
      Entrar
     </a>
     <a class="button secondary" data-guest="" href="/cadastro.html">
      Criar conta
     </a>
     <span class="nav-session" data-session="" hidden="">
      <span data-user="">
      </span>
      <button class="secondary" data-logout="">
       Sair
      </button>
     </span>
    </nav>
   </div>
  </header>
  <main id="main">
   <section class="intro">
    <div>
     <p class="eyebrow">
      SUA CONTA / HISTÓRICO
     </p>
     <h1>
      Meus pedidos
      <span>
       .
      </span>
     </h1>
     <p>
      Suas escolhas, todas em um só lugar.
     </p>
    </div>
    <a class="button secondary" href="/loja.html">
     Voltar à loja ↗
    </a>
   </section>
   <div class="message" hidden="" id="message" role="status">
   </div>
   <section hidden="" id="orders-content">
    <div class="catalog-bar">
     <span class="muted" id="order-count">
     </span>
     <button class="secondary" id="reload-orders">
      Atualizar ↻
     </button>
    </div>
    <div aria-busy="false" id="orders-list">
    </div>
   </section>
  </main>
  <footer>
   <div class="footer-main">
    <div>
     <a class="brand" href="/index.html">
      dessik
      <span>
       .
      </span>
     </a>
     <p>
      Tecnologia para quem faz
      <br/>
      do próprio jeito.
     </p>
    </div>
    <div class="footer-links">
     <a href="/loja.html">
      Explorar produtos
     </a>
     <a href="/login.html">
      Minha conta
     </a>
     <a href="/cadastro.html">
      Criar conta
     </a>
    </div>
   </div>
   <div class="footer-bottom">
    <span>
     © 2026 Dessik. Projeto acadêmico.
    </span>
    <span>
     Produtos fictícios. Compras simuladas. Nenhuma cobrança.
    </span>
   </div>
  </footer>
 </body>
</html>
```

O que este arquivo faz:

- Mostra o histórico do usuário autenticado.


## ARQUIVO: privada/.env.example

```text
DB_HOST=
DB_PORT=3306
DB_USER=
DB_PASSWORD=
DB_NAME=loja_ficticia
DB_SSL=true
DB_SSL_CA=

JWT_SECRET=
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
APP_ENV=development
CORS_ORIGINS=http://127.0.0.1:5500,http://localhost:5500
```

O que este arquivo faz:

- Lista variáveis sem incluir segredos reais.


## ARQUIVO: privada/.gitignore

```text
.env
.env.*
!.env.example
venv/
.venv/
__pycache__/
*.pyc
.pytest_cache/
.vercel/
```

O que este arquivo faz:

- Mantém arquivos privados e temporários fora do Git.


## ARQUIVO: privada/api/index.py

```python
"""Ponto de entrada reconhecido pela Vercel."""
from backend.main import app
```

O que este arquivo faz:

- Exporta a aplicação FastAPI para a Vercel.


## ARQUIVO: privada/backend/auth.py

```python
from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
from backend.database import settings
import secrets
import string
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from backend.database import transaction


def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode()


def verify_password(password, hashed):
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode())
    except (ValueError, TypeError):
        return False


def create_token(user_id):
    now = datetime.now(timezone.utc)
    return jwt.encode({"sub": str(user_id), "iat": now,
                       "exp": now + timedelta(minutes=settings()["minutes"]),
                       "iss": "dessik", "aud": "dessik-web"},
                      settings()["secret"], algorithm="HS256")


def decode_token(token):
    return jwt.decode(token, settings()["secret"], algorithms=["HS256"],
                      issuer="dessik", audience="dessik-web",
                      options={"require": ["sub", "exp", "iat", "iss", "aud"]})


def generate_password(length=16):
    groups = (string.ascii_lowercase, string.ascii_uppercase, string.digits, "!@#$%&*+-=?")
    alphabet = "".join(groups)
    # Rejeição garante que todos os grupos apareçam, usando somente secrets.
    while True:
        password = "".join(secrets.choice(alphabet) for _ in range(length))
        if all(any(char in group for char in password) for group in groups):
            return password


bearer = HTTPBearer(auto_error=False)


def current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)):
    unauthorized = HTTPException(401, "Sessão inválida ou expirada. Entre novamente.",
                                 headers={"WWW-Authenticate": "Bearer"})
    if credentials is None:
        raise unauthorized
    try:
        user_id = int(decode_token(credentials.credentials)["sub"])
        if user_id <= 0:
            raise ValueError()
    except (InvalidTokenError, ValueError, TypeError, KeyError):
        raise unauthorized
    with transaction() as cursor:
        cursor.execute("SELECT id_usuario, nome, email, tipo_usuario FROM usuarios WHERE id_usuario = %s", (user_id,))
        user = cursor.fetchone()
    if not user:
        raise unauthorized
    user["is_admin"] = user["tipo_usuario"] == "admin"
    return user


def admin_user(user=Depends(current_user)):
    # A permissão vem do banco em cada requisição, nunca de um botão ou do cliente.
    if user["tipo_usuario"] != "admin":
        raise HTTPException(403, "Esta operação exige um administrador.")
    return user
```

O que este arquivo faz:

- Protege senhas com bcrypt, verifica JWT e consulta a permissão administrativa.


## ARQUIVO: privada/backend/database.py

```python
import os
from functools import lru_cache
from pathlib import Path
from dotenv import load_dotenv
from contextlib import contextmanager
import mysql.connector


load_dotenv(Path(__file__).resolve().parents[1] / ".env")


@lru_cache
def settings():
    """Falha explicitamente se faltam segredos; não existe chave padrão."""
    secret = os.getenv("JWT_SECRET", "")
    if len(secret.encode()) < 32:
        raise RuntimeError("Configure JWT_SECRET com pelo menos 32 bytes aleatórios.")
    if os.getenv("JWT_ALGORITHM", "HS256") != "HS256":
        raise RuntimeError("Este projeto utiliza somente JWT_ALGORITHM=HS256.")
    minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    if not 1 <= minutes <= 1440:
        raise RuntimeError("ACCESS_TOKEN_EXPIRE_MINUTES deve estar entre 1 e 1440.")
    production = os.getenv("APP_ENV") == "production" or os.getenv("VERCEL") == "1"
    host = os.getenv("DB_HOST", "")
    tls = os.getenv("DB_SSL", "true").lower() == "true"
    if not host or not os.getenv("DB_USER") or not os.getenv("DB_NAME"):
        raise RuntimeError("Configure DB_HOST, DB_USER e DB_NAME.")
    if production and (not tls or host.lower() in {"localhost", "127.0.0.1", "::1"}):
        raise RuntimeError("Produção exige MySQL remoto com TLS.")
    origins = [x.strip() for x in os.getenv("CORS_ORIGINS", "").split(",") if x.strip()]
    if "*" in origins:
        raise RuntimeError("CORS_ORIGINS deve conter origens explícitas, sem *.")
    return {"secret": secret, "minutes": minutes, "production": production,
            "host": host, "tls": tls, "origins": origins}


"""Conexões curtas: cada operação libera cursor e conexão, inclusive com erro."""


def connect():
    config = settings()
    options = {
        "host": config["host"], "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.environ["DB_USER"], "password": os.getenv("DB_PASSWORD", ""),
        "database": os.environ["DB_NAME"], "charset": "utf8mb4",
        "autocommit": False, "connection_timeout": 10,
        "read_timeout": 15, "write_timeout": 15, "use_pure": True,
        "ssl_disabled": not config["tls"],
    }
    if config["tls"]:
        options.update(ssl_verify_cert=True, ssl_verify_identity=True)
        if os.getenv("DB_SSL_CA"):
            options["ssl_ca"] = os.environ["DB_SSL_CA"]
    return mysql.connector.connect(**options)


@contextmanager
def transaction():
    connection = connect()
    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        yield cursor
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()
```

O que este arquivo faz:

- Lê configuração privada e garante commit, rollback e fechamento da conexão.


## ARQUIVO: privada/backend/main.py

```python
import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from mysql.connector import Error as DatabaseError
from starlette.exceptions import HTTPException
from backend.database import settings, transaction
import re
import httpx
from decimal import Decimal
from typing import Literal
from fastapi import Depends, Query
from mysql.connector import IntegrityError
from backend.auth import current_user, admin_user, create_token, hash_password, verify_password, generate_password
from backend.schemas import Cadastro, Login, Produto, Pedido
from backend.models import serialize_product


@asynccontextmanager
async def lifespan(app):
    settings()  # Valida configuração no início, sem abrir conexão permanente.
    yield


app = FastAPI(title="Dessik • API da loja", version="1.0.0", lifespan=lifespan,
              docs_url="/api/docs", redoc_url=None, openapi_url="/api/openapi.json")
origins = [value.strip() for value in os.getenv("CORS_ORIGINS", "").split(",") if value.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=False,
                   allow_methods=["GET", "POST", "PUT", "DELETE"],
                   allow_headers=["Authorization", "Content-Type"])


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    if request.url.path.startswith("/api/"):
        response.headers["Cache-Control"] = "no-store"
    if not request.url.path.startswith("/api/docs"):
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self'; style-src 'self'; "
            "img-src 'self' https:; connect-src 'self'; object-src 'none'; "
            "base-uri 'self'; frame-ancestors 'none'; form-action 'self'")
    return response


@app.exception_handler(HTTPException)
async def http_error(request, error):
    return JSONResponse({"mensagem": error.detail}, status_code=error.status_code, headers=error.headers)


@app.exception_handler(RequestValidationError)
async def validation_error(request, error):
    # Nunca devolva error.input: pode conter senhas enviadas pelo usuário.
    fields = [{"campo": ".".join(str(part) for part in item["loc"][1:]),
               "mensagem": item["msg"]} for item in error.errors()]
    return JSONResponse({"mensagem": "Confira os campos informados.", "erros": fields}, status_code=422)


@app.exception_handler(DatabaseError)
async def database_error(request, error):
    logging.getLogger("dessik").error("Falha MySQL: código %s", error.errno)
    if error.errno in (1205, 1213):
        return JSONResponse({"mensagem": "Operação concorrente. Atualize os dados e tente novamente."}, status_code=409)
    return JSONResponse({"mensagem": "Banco indisponível. Tente novamente mais tarde."}, status_code=503)


@app.exception_handler(Exception)
async def unexpected_error(request, error):
    logging.getLogger("dessik").error("Falha inesperada: %s", type(error).__name__)
    return JSONResponse({"mensagem": "Não foi possível concluir a operação."}, status_code=500)


@app.get("/api/health", tags=["Sistema"])
def health():
    return {"status": "ok"}


# USUARIOS
# Hash válido apenas para equalizar o custo do login de um e-mail inexistente.
DUMMY_HASH = hash_password(generate_password())


@app.post("/api/cadastro", status_code=201)
def cadastro(data: Cadastro):
    hashed = hash_password(data.senha)
    try:
        with transaction() as cursor:
            # Query parametrizada: valores separados do SQL evitam SQL Injection.
            cursor.execute(
                """INSERT INTO usuarios
                (nome, email, senha_hash, cep, logradouro, bairro, cidade, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (data.nome, str(data.email), hashed, data.cep, data.logradouro,
                 data.bairro, data.cidade, data.estado))
            user_id = cursor.lastrowid
    except IntegrityError as error:
        if error.errno == 1062:
            raise HTTPException(409, "Este e-mail já está cadastrado.")
        raise
    return {"mensagem": "Conta criada. Você já pode entrar.", "id_usuario": user_id}


@app.post("/api/login")
def login(data: Login):
    with transaction() as cursor:
        cursor.execute("SELECT id_usuario, senha_hash FROM usuarios WHERE email = %s", (str(data.email),))
        user = cursor.fetchone()
    valid = verify_password(data.senha, user["senha_hash"] if user else DUMMY_HASH)
    if not user or not valid:
        raise HTTPException(401, "E-mail ou senha incorretos.", headers={"WWW-Authenticate": "Bearer"})
    return {"access_token": create_token(user["id_usuario"]), "token_type": "bearer"}


@app.get("/api/me")
def me(user=Depends(current_user)):
    return user


@app.get("/api/gerar-senha")
def password():
    return {"senha": generate_password()}


# PRODUTOS
@app.get("/api/produtos")
def list_products(limite: int = Query(100, ge=1, le=100), offset: int = Query(0, ge=0),
                  busca: str = Query('', max_length=100), categoria: str = Query('', max_length=60),
                  ordem: Literal['recentes', 'menor-preco', 'maior-preco'] = 'recentes'):
    # Apenas expressões constantes entram no ORDER BY. Texto do usuário é parametrizado.
    sorting = {'recentes': 'id_produto ASC', 'menor-preco': 'preco ASC, id_produto ASC',
               'maior-preco': 'preco DESC, id_produto ASC'}[ordem]
    with transaction() as cursor:
        cursor.execute("""SELECT * FROM produtos
            WHERE (%s = '' OR LOCATE(%s, CONCAT(nome, ' ', descricao)) > 0)
              AND (%s = '' OR categoria = %s)
            ORDER BY """ + sorting + " LIMIT %s OFFSET %s",
                       (busca.strip(), busca.strip(), categoria, categoria, limite, offset))
        return [serialize_product(p) for p in cursor.fetchall()]


@app.get("/api/produtos/{product_id}")
def get_product(product_id: int):
    with transaction() as cursor:
        cursor.execute("SELECT * FROM produtos WHERE id_produto = %s", (product_id,))
        product = cursor.fetchone()
    if not product:
        raise HTTPException(404, "Produto não encontrado.")
    return serialize_product(product)


@app.post("/api/produtos", status_code=201)
def create_product(data: Produto, user=Depends(admin_user)):
    with transaction() as cursor:
        cursor.execute("""INSERT INTO produtos
            (nome, descricao, categoria, preco, quantidade_estoque, imagem_url)
            VALUES (%s, %s, %s, %s, %s, %s)""", tuple(data.model_dump().values()))
        product_id = cursor.lastrowid
    return {"mensagem": "Produto cadastrado.", "id_produto": product_id}


@app.put("/api/produtos/{product_id}")
def update_product(product_id: int, data: Produto, user=Depends(admin_user)):
    with transaction() as cursor:
        cursor.execute("SELECT id_produto FROM produtos WHERE id_produto = %s FOR UPDATE", (product_id,))
        if not cursor.fetchone():
            raise HTTPException(404, "Produto não encontrado.")
        cursor.execute("""UPDATE produtos SET nome=%s, descricao=%s, categoria=%s,
            preco=%s, quantidade_estoque=%s, imagem_url=%s WHERE id_produto=%s""",
                       (*data.model_dump().values(), product_id))
    return {"mensagem": "Produto atualizado."}


@app.delete("/api/produtos/{product_id}")
def delete_product(product_id: int, user=Depends(admin_user)):
    try:
        with transaction() as cursor:
            cursor.execute("DELETE FROM produtos WHERE id_produto = %s", (product_id,))
            if cursor.rowcount == 0:
                raise HTTPException(404, "Produto não encontrado.")
    except IntegrityError as error:
        if error.errno == 1451:
            raise HTTPException(409, "Produto possui pedidos. Mantenha o histórico e ajuste o estoque para zero.")
        raise
    return {"mensagem": "Produto excluído."}


# PEDIDOS


@app.post("/api/pedidos", status_code=201)
def create_order(data: Pedido, user=Depends(current_user)):
    with transaction() as cursor:
        products = {}
        total = Decimal("0.00")
        # Ordem fixa de bloqueios reduz deadlocks entre pedidos de vários produtos.
        for item in sorted(data.itens, key=lambda item: item.id_produto):
            cursor.execute("SELECT * FROM produtos WHERE id_produto = %s FOR UPDATE", (item.id_produto,))
            product = cursor.fetchone()
            if not product:
                raise HTTPException(404, "Um dos produtos não existe mais.")
            if product["quantidade_estoque"] < item.quantidade:
                raise HTTPException(409, f"Estoque insuficiente para {product['nome']}.")
            products[item.id_produto] = product
            # O navegador envia apenas IDs e quantidades: preço e estoque vêm do banco.
            total += product["preco"] * item.quantidade
        cursor.execute("INSERT INTO pedidos (id_usuario, valor_total, status) VALUES (%s, %s, %s)",
                       (user["id_usuario"], total, "simulado"))
        order_id = cursor.lastrowid
        for item in data.itens:
            cursor.execute("""INSERT INTO itens_pedido
                (id_pedido, id_produto, quantidade, preco_unitario)
                VALUES (%s, %s, %s, %s)""",
                           (order_id, item.id_produto, item.quantidade, products[item.id_produto]["preco"]))
            cursor.execute("""UPDATE produtos SET quantidade_estoque = quantidade_estoque - %s
                WHERE id_produto = %s AND quantidade_estoque >= %s""",
                           (item.quantidade, item.id_produto, item.quantidade))
            if cursor.rowcount != 1:
                raise HTTPException(409, "Estoque alterado. Atualize a loja e tente novamente.")
        # O context manager confirma tudo junto ou desfaz tudo se uma etapa falhar.
    return {"mensagem": "Pedido simulado com sucesso. Nenhuma cobrança foi realizada.",
            "id_pedido": order_id, "valor_total": str(total)}


@app.get("/api/pedidos")
def list_orders(user=Depends(current_user)):
    with transaction() as cursor:
        cursor.execute("""SELECT id_pedido, data_pedido, valor_total, status FROM pedidos
            WHERE id_usuario = %s ORDER BY id_pedido DESC LIMIT 100""", (user["id_usuario"],))
        orders = cursor.fetchall()
    for order in orders:
        order["valor_total"] = str(order["valor_total"])
    return orders


# CEP


@app.get("/api/cep/{cep}")
def lookup_cep(cep: str):
    cep = cep.replace("-", "")
    if not re.fullmatch(r"[0-9]{8}", cep):
        raise HTTPException(422, "Informe um CEP com 8 números.")
    try:
        # Host fixo e CEP numérico impedem que a entrada vire uma URL arbitrária.
        with httpx.Client(timeout=5.0) as client:
            response = client.get(f"https://viacep.com.br/ws/{cep}/json/")
            response.raise_for_status()
            address = response.json()
        if not isinstance(address, dict):
            raise ValueError("Resposta inválida")
    except (httpx.HTTPError, ValueError):
        raise HTTPException(502, "ViaCEP indisponível. Preencha o endereço manualmente.")
    if address.get("erro"):
        raise HTTPException(404, "CEP não encontrado.")
    fields = {"cep": "cep", "logradouro": "logradouro", "bairro": "bairro",
              "cidade": "localidade", "estado": "uf"}
    if any(not isinstance(address.get(key, ""), str) for key in fields.values()):
        raise HTTPException(502, "Resposta inválida do ViaCEP.")
    return {key: address.get(source, "") for key, source in fields.items()}


@app.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"], include_in_schema=False)
def unknown_api(path: str):
    raise HTTPException(404, "Endpoint não encontrado.")


# Somente publico/ é servido. Nunca monte workspace/ ou privada/ como arquivos estáticos.
if os.getenv("VERCEL") != "1":
    app.mount("/", StaticFiles(directory=Path(__file__).resolve().parents[2] / "publico", html=True), name="frontend")
```

O que este arquivo faz:

- Define as rotas, valida pedidos e registra tudo na transação SQL.


## ARQUIVO: privada/backend/models.py

```python
"""Sem ORM: as tabelas estão em database/schema.sql e usamos dicionários."""

def serialize_product(product):
    # Decimal vira texto no JSON para preservar os centavos.
    product["preco"] = str(product["preco"])
    return product
```

O que este arquivo faz:

- Converte valores monetários para JSON, sem usar ORM.


## ARQUIVO: privada/backend/schemas.py

```python
from decimal import Decimal
import re

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator


class Input(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Login(Input):
    email: EmailStr = Field(max_length=254)
    senha: str = Field(min_length=1, max_length=72)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value):
        return value.lower()

    @field_validator("senha")
    @classmethod
    def password_bytes(cls, value):
        if len(value.encode("utf-8")) > 72:
            raise ValueError("A senha deve ter no máximo 72 bytes UTF-8.")
        return value


class Cadastro(Login):
    nome: str = Field(min_length=2, max_length=100)
    senha: str = Field(min_length=8, max_length=72)
    confirmar_senha: str = Field(min_length=8, max_length=72)
    cep: str = ""
    logradouro: str = Field(default="", max_length=150)
    bairro: str = Field(default="", max_length=100)
    cidade: str = Field(default="", max_length=100)
    estado: str = Field(default="", max_length=2)

    @field_validator("nome")
    @classmethod
    def valid_name(cls, value):
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Informe um nome com pelo menos 2 caracteres.")
        return value

    @field_validator("cep")
    @classmethod
    def valid_cep(cls, value):
        value = value.replace("-", "").strip()
        if value and not re.fullmatch(r"[0-9]{8}", value):
            raise ValueError("CEP deve conter 8 números.")
        return value

    @field_validator("estado")
    @classmethod
    def valid_state(cls, value):
        value = value.upper()
        if value and value not in "AC AL AP AM BA CE DF ES GO MA MT MS MG PA PB PR PE PI RJ RN RS RO RR SC SP SE TO".split():
            raise ValueError("UF inválida.")
        return value

    @model_validator(mode="after")
    def matching_passwords(self):
        if self.senha != self.confirmar_senha:
            raise ValueError("As senhas não coincidem.")
        return self


class Produto(Input):
    nome: str = Field(min_length=2, max_length=120)
    descricao: str = Field(min_length=1, max_length=2000)
    categoria: str = Field(min_length=1, max_length=60)
    preco: Decimal = Field(gt=0, le=99999999.99, max_digits=10, decimal_places=2)
    quantidade_estoque: int = Field(ge=0, le=1000000, strict=True)
    imagem_url: str = Field(max_length=1000)

    @field_validator("nome", "descricao", "categoria")
    @classmethod
    def non_blank(cls, value):
        if not value.strip():
            raise ValueError("O campo não pode ficar vazio.")
        return value.strip()

    @field_validator("imagem_url")
    @classmethod
    def safe_image(cls, value):
        from urllib.parse import urlsplit
        parsed = urlsplit(value)
        if (parsed.scheme == "https" and parsed.netloc and not parsed.username
                and not parsed.password):
            return value
        if re.fullmatch(r"/imagens/[a-zA-Z0-9_/-]+\.(png|jpg|jpeg|webp|svg)", value) and ".." not in value:
            return value
        raise ValueError("Use uma URL HTTPS ou imagem local em /imagens/.")


class ItemPedido(Input):
    id_produto: int = Field(gt=0, strict=True)
    quantidade: int = Field(gt=0, le=1000, strict=True)


class Pedido(Input):
    itens: list[ItemPedido] = Field(min_length=1, max_length=50)

    @model_validator(mode="after")
    def unique_items(self):
        if len({i.id_produto for i in self.itens}) != len(self.itens):
            raise ValueError("Agrupe as quantidades de cada produto em um único item.")
        return self
```

O que este arquivo faz:

- Rejeita campos e valores inválidos antes de executar as regras da API.


## ARQUIVO: privada/database/dados.sql

```sql
-- Execute uma vez, após schema.sql, em um banco vazio.
-- As condições por ID permitem repetir a inicialização sem resetar o estoque.
INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 1,'Notebook Horizon 14','Leve para estudar, criar e levar sua rotina a qualquer lugar. Tela de 14 polegadas e SSD de 512 GB.','Computadores',3299.90,8,'/imagens/catalogo-dessik.png'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=1);
INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 2,'Mouse Pulse','Precisão e conforto para trabalhar e jogar. Sensor de 6.400 DPI e seis botões.','Periféricos',129.90,24,'/imagens/catalogo-dessik.png'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=2);
INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 3,'Teclado mecânico Type','Formato compacto, conexão USB e teclas mecânicas para o seu setup.','Periféricos',249.90,15,'/imagens/catalogo-dessik.png'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=3);
INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 4,'Monitor View 24','Mais espaço para suas ideias. Painel de 24 polegadas Full HD com conexão HDMI.','Monitores',899.90,6,'/imagens/catalogo-dessik.png'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=4);
INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 5,'Headset Wave','Áudio estéreo, microfone ajustável e almofadas macias para longas sessões.','Áudio',189.90,18,'/imagens/catalogo-dessik.png'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=5);
INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 6,'Webcam Focus','Videochamadas em Full HD com microfone integrado e suporte para monitor.','Periféricos',219.90,0,'/imagens/catalogo-dessik.png'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=6);
INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 7,'SSD Sprint 1 TB','Espaço e velocidade para arquivos, jogos e projetos. Interface SATA.','Componentes',399.90,20,'/imagens/catalogo-dessik.png'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=7);
INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 8,'Memória RAM Flux 16 GB','Mais fôlego para várias tarefas. Módulo DDR4 de 3.200 MHz.','Componentes',229.90,12,'/imagens/catalogo-dessik.png'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=8);

INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 9,'Hub USB Connect','Quatro portas USB para organizar seus acessórios.','Acessórios',89.90,3,'/imagens/hub.svg'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=9);

INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 10,'Mousepad Glide','Base antiderrapante com espaço para movimentos livres.','Acessórios',49.90,30,'/imagens/mousepad.svg'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=10);

INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 11,'Suporte Rise','Suporte de mesa para elevar seu notebook.','Acessórios',119.90,2,'/imagens/suporte.svg'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=11);

INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 12,'Controle Play','Controle USB para seus jogos no computador.','Periféricos',159.90,10,'/imagens/controle.svg'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=12);
```

O que este arquivo faz:

- Insere doze produtos sem reiniciar estoque já existente.


## ARQUIVO: privada/database/schema.sql

```sql
-- MySQL 8.0.16+ (InnoDB). Execute no banco escolhido na conexão.
-- Em provedores sem CREATE DATABASE, crie/selecione o banco pelo painel.
-- Opcional, em servidor próprio:
-- CREATE DATABASE loja_ficticia CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- USE loja_ficticia;

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(254) NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    tipo_usuario ENUM('cliente', 'admin') NOT NULL DEFAULT 'cliente',
    cep VARCHAR(8) NOT NULL DEFAULT '',
    logradouro VARCHAR(150) NOT NULL DEFAULT '',
    bairro VARCHAR(100) NOT NULL DEFAULT '',
    cidade VARCHAR(100) NOT NULL DEFAULT '',
    estado VARCHAR(2) NOT NULL DEFAULT '',
    data_cadastro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_usuarios_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS produtos (
    id_produto INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    descricao TEXT NOT NULL,
    categoria VARCHAR(60) NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    quantidade_estoque INT NOT NULL DEFAULT 0,
    imagem_url VARCHAR(1000) NOT NULL,
    data_cadastro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    KEY idx_produtos_categoria (categoria),
    CONSTRAINT ck_produtos_preco CHECK (preco > 0),
    CONSTRAINT ck_produtos_estoque CHECK (quantidade_estoque >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS pedidos (
    id_pedido INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    data_pedido TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    valor_total DECIMAL(16,2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'simulado',
    KEY idx_pedidos_usuario_data (id_usuario, data_pedido),
    CONSTRAINT fk_pedidos_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE RESTRICT,
    CONSTRAINT ck_pedidos_total CHECK (valor_total > 0),
    CONSTRAINT ck_pedidos_status CHECK (status = 'simulado')
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS itens_pedido (
    id_item INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10,2) NOT NULL,
    UNIQUE KEY uq_item_produto (id_pedido, id_produto),
    KEY idx_itens_produto (id_produto),
    CONSTRAINT fk_itens_pedido FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido) ON DELETE RESTRICT,
    CONSTRAINT fk_itens_produto FOREIGN KEY (id_produto) REFERENCES produtos(id_produto) ON DELETE RESTRICT,
    CONSTRAINT ck_itens_quantidade CHECK (quantidade > 0),
    CONSTRAINT ck_itens_preco CHECK (preco_unitario > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- A massa de demonstração fica em dados.sql; scripts.init_db executa ambos.
```

O que este arquivo faz:

- Cria as quatro tabelas, seus relacionamentos e restrições.


## ARQUIVO: privada/pytest.ini

```text
[pytest]
testpaths = tests
pythonpath = .
markers =
    integration: requer banco isolado terminado em _test
```

O que este arquivo faz:

- Configura descoberta de testes e a marca de integração.


## ARQUIVO: privada/requirements-dev.txt

```text
-r requirements.txt
pytest==9.0.2
```

O que este arquivo faz:

- Acrescenta pytest para executar os testes.


## ARQUIVO: privada/requirements.txt

```text
fastapi==0.135.1
uvicorn==0.41.0
mysql-connector-python==9.6.0
python-dotenv==1.2.2
PyJWT==2.12.1
bcrypt==5.0.0
httpx==0.28.1
email-validator==2.3.0
```

O que este arquivo faz:

- Lista as bibliotecas necessárias à execução.


## ARQUIVO: privada/tests/conftest.py

```python
import os
import secrets

import pytest
from fastapi.testclient import TestClient

# Os testes não carregam credenciais reais nem sobrescrevem o .env do usuário.
os.environ.setdefault("JWT_SECRET", secrets.token_urlsafe(48))
os.environ.setdefault("DB_HOST", "127.0.0.1")
os.environ.setdefault("DB_USER", "dessik_test")
os.environ.setdefault("DB_NAME", "dessik_test")
os.environ.setdefault("DB_SSL", "false")

from api.index import app
from backend.database import settings


@pytest.fixture
def client():
    settings.cache_clear()
    with TestClient(app) as client:
        yield client
    settings.cache_clear()
```

O que este arquivo faz:

- Verifica funcionalidades e proteções no ambiente de testes.


## ARQUIVO: privada/tests/test_browser.py

```python
"""Opcional: RUN_BROWSER_TESTS=1, pip install playwright, Edge instalado.
Execute com a API em BROWSER_URL usando somente banco terminado em _test.
"""
import os
import uuid
import pytest

pytestmark = pytest.mark.skipif(os.getenv('RUN_BROWSER_TESTS') != '1', reason='Teste visual opcional com Edge e API de teste.')

def test_store_in_browser():
    from playwright.sync_api import sync_playwright, expect
    from backend.database import transaction
    assert os.environ['DB_NAME'].endswith('_test')
    url = os.environ.get('BROWSER_URL', 'http://127.0.0.1:8001')
    identifier = uuid.uuid4().hex[:10]
    email = f'visual{identifier}@example.com'
    errors = []
    with sync_playwright() as engine:
        browser = engine.chromium.launch(channel='msedge', headless=True)
        page = browser.new_page(viewport={'width': 1440, 'height': 1000})
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto(url)
        expect(page.locator('#products .card')).to_have_count(4)
        page.screenshot(path=os.environ.get('QA_SCREENSHOT', 'inicio-qa.png'), full_page=True)
        page.goto(url + '/cadastro.html')
        page.locator('[name=nome]').fill('Aluno de teste')
        page.locator('[name=email]').fill(email)
        page.locator('[name=senha]').fill('SenhaTeste123!')
        page.locator('[name=confirmar_senha]').fill('SenhaTeste123!')
        page.locator('button[type=submit]').click()
        expect(page).to_have_url(url + '/login.html?cadastro=ok')
        page.locator('[name=email]').fill(email)
        page.locator('[name=senha]').fill('SenhaTeste123!')
        page.locator('button[type=submit]').click()
        expect(page).to_have_url(url + '/loja.html')
        with transaction() as cursor:
            cursor.execute("UPDATE usuarios SET tipo_usuario='admin' WHERE email=%s", (email,))
        page.goto(url + '/admin.html')
        expect(page.locator('#admin-content')).to_be_visible()
        name = 'Produto visual ' + identifier
        for field, value in {'nome':name, 'descricao':'Produto temporário de teste', 'categoria':'Teste',
                             'preco':'12.90', 'quantidade_estoque':'3', 'imagem_url':'/imagens/hub.svg'}.items():
            page.locator(f'[name={field}]').fill(value)
        page.locator('#save-product').click()
        expect(page.locator('#message')).to_contain_text('Produto cadastrado')
        page.goto(url + '/loja.html')
        page.locator('#search').fill(identifier)
        expect(page.locator('#products .card')).to_have_count(1)
        page.locator('.buy-row input').fill('2')
        page.locator('.buy-row button').click()
        expect(page.locator('#message')).to_contain_text('Produto adicionado')
        page.goto(url + '/carrinho.html')
        expect(page.locator('#cart-items')).to_contain_text(name)
        expect(page.locator('#cart-total')).to_contain_text('25,80')
        page.locator('#checkout').click()
        expect(page.locator('#message')).to_contain_text('realizado!')
        expect(page.locator('#cart-items')).to_contain_text('vazio')
        page.goto(url + '/loja.html')
        page.locator('#search').fill(identifier)
        expect(page.locator('#products')).to_contain_text('Últimas 1 unidades')
        for width in (390, 768):
            page.set_viewport_size({'width':width, 'height':844})
            for route in ('index.html', 'loja.html', 'cadastro.html', 'login.html', 'carrinho.html', 'admin.html'):
                page.goto(url + '/' + route)
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (route, width)
        assert not errors, errors
        browser.close()
```

O que este arquivo faz:

- Verifica funcionalidades e proteções no ambiente de testes.


## ARQUIVO: privada/tests/test_cep.py

```python
import httpx
import pytest


def test_invalid_cep(client):
    assert client.get('/api/cep/123').status_code == 422


@pytest.mark.parametrize('payload,status,expected', [
    ({'cep': '01001-000', 'logradouro': 'Praça da Sé', 'bairro': 'Sé', 'localidade': 'São Paulo', 'uf': 'SP'}, 200, 200),
    ({'erro': True}, 200, 404),
    ({}, 500, 502),
    ([], 200, 502),
])
def test_viacep_responses(client, monkeypatch, payload, status, expected):
    def get(self, url):
        assert url == 'https://viacep.com.br/ws/01001000/json/'
        return httpx.Response(status, json=payload, request=httpx.Request('GET', url))
    monkeypatch.setattr(httpx.Client, 'get', get)
    # TestClient também herda httpx.Client; chamamos request para não interceptar o teste.
    response = client.request('GET', '/api/cep/01001000')
    assert response.status_code == expected
    if expected == 200:
        assert response.json()['cidade'] == 'São Paulo'


def test_viacep_timeout(client, monkeypatch):
    def get(self, url):
        raise httpx.ReadTimeout('timeout')
    monkeypatch.setattr(httpx.Client, 'get', get)
    assert client.request('GET', '/api/cep/01001000').status_code == 502
```

O que este arquivo faz:

- Verifica funcionalidades e proteções no ambiente de testes.


## ARQUIVO: privada/tests/test_frontend.py

```python
from html.parser import HTMLParser
from pathlib import Path

PUBLIC = Path(__file__).resolve().parents[2] / 'publico'


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = []
    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if 'id' in attributes:
            self.ids.append(attributes['id'])
        for key in ('src', 'href'):
            if attributes.get(key, '').startswith('/'):
                self.links.append(attributes[key].split('?')[0])


def test_pages_have_resolvable_assets_and_unique_ids():
    for path in PUBLIC.glob('*.html'):
        page = Page()
        source = path.read_text(encoding='utf-8')
        page.feed(source)
        assert 'lang="pt-BR"' in source
        assert len(page.ids) == len(set(page.ids)), path
        for link in page.links:
            assert (PUBLIC / link.lstrip('/')).is_file(), (path, link)


def test_catalog_is_not_hardcoded():
    for name in ('index.html', 'loja.html'):
        source = (PUBLIC / name).read_text(encoding='utf-8')
        assert 'Notebook Horizon' not in source
        assert 'id="products"' in source
    script = (PUBLIC / 'js' / 'loja.js').read_text(encoding='utf-8')
    assert 'apiRequest(`/produtos' in script
```

O que este arquivo faz:

- Verifica funcionalidades e proteções no ambiente de testes.


## ARQUIVO: privada/tests/test_mysql.py

```python
"""Integração real, sem SQLite. Cria dados novos e não remove tabelas existentes."""
import os
import uuid
from concurrent.futures import ThreadPoolExecutor

import pytest
from fastapi.testclient import TestClient

from api.index import app
from backend.database import transaction
from backend.auth import verify_password

pytestmark = [pytest.mark.integration,
              pytest.mark.skipif(os.getenv('RUN_MYSQL_TESTS') != '1', reason='Configure um MySQL isolado e RUN_MYSQL_TESTS=1.')]


@pytest.fixture
def account(client):
    assert os.environ['DB_NAME'].endswith('_test'), 'Por segurança, use um banco terminado em _test.'
    email = f'{uuid.uuid4().hex}@example.com'
    body = {'nome': 'Cliente teste', 'email': email, 'senha': 'Teste123!', 'confirmar_senha': 'Teste123!'}
    registered = client.post('/api/cadastro', json=body)
    assert registered.status_code == 201
    assert client.post('/api/cadastro', json=body).status_code == 409
    assert client.post('/api/login', json={'email': email, 'senha': 'wrong'}).status_code == 401
    login = client.post('/api/login', json={'email': email, 'senha': body['senha']})
    assert login.status_code == 200
    headers = {'Authorization': f"Bearer {login.json()['access_token']}"}
    user_id = registered.json()['id_usuario']
    with transaction() as cursor:
        cursor.execute('SELECT senha_hash, tipo_usuario FROM usuarios WHERE id_usuario=%s', (user_id,))
        stored = cursor.fetchone()
    assert verify_password(body['senha'], stored['senha_hash'])
    assert stored['tipo_usuario'] == 'cliente'
    return user_id, headers


def create_product(client, account, stock=3):
    user_id, headers = account
    with transaction() as cursor:
        cursor.execute("UPDATE usuarios SET tipo_usuario='admin' WHERE id_usuario=%s", (user_id,))
    body = {'nome': 'Produto teste', 'descricao': 'Produto de teste isolado', 'categoria': 'Teste',
            'preco': '12.90', 'quantidade_estoque': stock, 'imagem_url': '/imagens/placeholder.svg'}
    response = client.post('/api/produtos', json=body, headers=headers)
    assert response.status_code == 201, response.text
    return response.json()['id_produto'], body


def test_full_crud(client, account):
    _, headers = account
    assert client.delete('/api/produtos/1', headers=headers).status_code == 403
    product_id, body = create_product(client, account)
    assert client.get(f'/api/produtos/{product_id}').json()['preco'] == '12.90'
    assert client.put(f'/api/produtos/{product_id}', json=body | {'preco': '19.90'}, headers=headers).status_code == 200
    assert client.delete(f'/api/produtos/{product_id}', headers=headers).status_code == 200
    assert client.get(f'/api/produtos/{product_id}').status_code == 404


def test_order_and_rollback(client, account):
    _, headers = account
    product_id, _ = create_product(client, account, stock=3)
    other_id, _ = create_product(client, account, stock=0)
    failed = client.post('/api/pedidos', headers=headers, json={'itens': [
        {'id_produto': product_id, 'quantidade': 1}, {'id_produto': other_id, 'quantidade': 1}]})
    assert failed.status_code == 409
    assert client.get(f'/api/produtos/{product_id}').json()['quantidade_estoque'] == 3
    assert client.get('/api/pedidos', headers=headers).json() == []
    success = client.post('/api/pedidos', headers=headers, json={'itens': [{'id_produto': product_id, 'quantidade': 2}]})
    assert success.status_code == 201
    assert success.json()['valor_total'] == '25.80'
    assert client.get(f'/api/produtos/{product_id}').json()['quantidade_estoque'] == 1
    assert client.delete(f'/api/produtos/{product_id}', headers=headers).status_code == 409
    assert len(client.get('/api/pedidos', headers=headers).json()) == 1


def test_concurrent_purchase_never_oversells(client, account):
    _, headers = account
    product_id, _ = create_product(client, account, stock=1)
    def buy():
        with TestClient(app) as buyer:
            return buyer.post('/api/pedidos', headers=headers,
                              json={'itens': [{'id_produto': product_id, 'quantidade': 1}]}).status_code
    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(lambda _: buy(), range(2)))
    assert sorted(results) == [201, 409]
    assert client.get(f'/api/produtos/{product_id}').json()['quantidade_estoque'] == 0


def test_cart_multiple_products_and_price_tampering(client, account):
    _, headers = account
    first, _ = create_product(client, account, stock=4)
    second, _ = create_product(client, account, stock=3)
    forged = client.post('/api/pedidos', headers=headers, json={'itens': [
        {'id_produto': first, 'quantidade': 2, 'preco': '0.01'}]})
    assert forged.status_code == 422
    assert client.get(f'/api/produtos/{first}').json()['quantidade_estoque'] == 4
    order = client.post('/api/pedidos', headers=headers, json={'itens': [
        {'id_produto': first, 'quantidade': 2}, {'id_produto': second, 'quantidade': 1}]})
    assert order.status_code == 201
    assert order.json()['valor_total'] == '38.70'
    assert client.get(f'/api/produtos/{first}').json()['quantidade_estoque'] == 2
    assert client.get(f'/api/produtos/{second}').json()['quantidade_estoque'] == 2


def test_sql_injection_is_data(client, account):
    product_id, body = create_product(client, account)
    _, headers = account
    name = "Mouse'); DROP TABLE produtos; --"
    assert client.put(f'/api/produtos/{product_id}', json=body | {'nome': name}, headers=headers).status_code == 200
    assert client.get(f'/api/produtos/{product_id}').json()['nome'] == name
    assert client.get('/api/produtos').status_code == 200
```

O que este arquivo faz:

- Verifica funcionalidades e proteções no ambiente de testes.


## ARQUIVO: privada/tests/test_security.py

```python
from datetime import datetime, timedelta, timezone
import string

import jwt
import pytest
from mysql.connector import DatabaseError
from pydantic import ValidationError

from backend.database import settings
from backend.schemas import Cadastro, Pedido, Produto
from backend.auth import create_token, decode_token, hash_password, verify_password
from backend.auth import generate_password


def test_hash_salt_and_verification():
    password = generate_password()
    first, second = hash_password(password), hash_password(password)
    assert first != second and first != password
    assert verify_password(password, first)
    assert not verify_password(password + '!', first)


def test_password_generator():
    passwords = {generate_password() for _ in range(100)}
    assert len(passwords) == 100
    for password in passwords:
        assert len(password) == 16
        for group in (string.ascii_lowercase, string.ascii_uppercase, string.digits, '!@#$%&*+-=?'):
            assert any(char in group for char in password)


def test_jwt_signature_expiration():
    token = create_token(1)
    assert decode_token(token)['sub'] == '1'
    with pytest.raises(jwt.InvalidTokenError):
        decode_token(token + 'corrupted')
    now = datetime.now(timezone.utc)
    expired = jwt.encode({'sub': '1', 'iat': now - timedelta(hours=2),
                          'exp': now - timedelta(hours=1), 'iss': 'dessik', 'aud': 'dessik-web'},
                         settings()['secret'], algorithm='HS256')
    with pytest.raises(jwt.ExpiredSignatureError):
        decode_token(expired)


@pytest.mark.parametrize('changes', [
    {'nome': '  '}, {'email': 'invalid'}, {'senha': 'short'},
    {'confirmar_senha': 'Different123!'}, {'senha': 'á' * 40, 'confirmar_senha': 'á' * 40},
    {'is_admin': True}, {'cep': '123'}, {'estado': 'ZZ'},
])
def test_invalid_registration(changes):
    data = {'nome': 'João Silva', 'email': 'joao@example.com', 'senha': 'Senha123!', 'confirmar_senha': 'Senha123!'}
    with pytest.raises(ValidationError):
        Cadastro(**(data | changes))


@pytest.mark.parametrize('quantity', [0, -1, 1.5, True, 1001])
def test_invalid_order_quantities(quantity):
    with pytest.raises(ValidationError):
        Pedido(itens=[{'id_produto': 1, 'quantidade': quantity}])


def test_duplicate_order_items():
    with pytest.raises(ValidationError):
        Pedido(itens=[{'id_produto': 1, 'quantidade': 1}] * 2)


@pytest.mark.parametrize('url', ['javascript:alert(1)', '//evil.com/image.png', '/imagens/../../.env', 'http://example.com/image.png'])
def test_unsafe_image_url(url):
    with pytest.raises(ValidationError):
        Produto(nome='Mouse', descricao='Mouse gamer', categoria='Mouse', preco='12.90', quantidade_estoque=1, imagem_url=url)


def test_api_validation_does_not_leak_password(client):
    response = client.post('/api/cadastro', json={'nome': '', 'email': 'x', 'senha': 'SUPER-SECRET'})
    assert response.status_code == 422
    assert 'SUPER-SECRET' not in response.text


def test_auth_guards(client):
    assert client.post('/api/pedidos', json={'itens': [{'id_produto': 1, 'quantidade': 1}]}).status_code == 401
    assert client.get('/api/me', headers={'Authorization': 'Bearer invalid'}).status_code == 401


def test_admin_without_token_and_negative_stock(client):
    from api.index import app
    from backend.auth import current_user
    product = {'nome': 'Mouse', 'descricao': 'Teste', 'categoria': 'Teste',
               'preco': '10.00', 'quantidade_estoque': -1, 'imagem_url': '/imagens/hub.svg'}
    assert client.post('/api/produtos', json=product).status_code == 401
    app.dependency_overrides[current_user] = lambda: {'id_usuario': 1, 'tipo_usuario': 'admin'}
    try:
        assert client.post('/api/produtos', json=product).status_code == 422
    finally:
        app.dependency_overrides.clear()


def test_expired_token_in_route(client):
    now = datetime.now(timezone.utc)
    token = jwt.encode({'sub': '1', 'iat': now - timedelta(hours=2),
                        'exp': now - timedelta(hours=1), 'iss': 'dessik', 'aud': 'dessik-web'},
                       settings()['secret'], algorithm='HS256')
    assert client.get('/api/me', headers={'Authorization': 'Bearer ' + token}).status_code == 401


def test_no_private_files_served(client):
    for path in ('/.env', '/privada/.env', '/backend/main.py', '/database/schema.sql'):
        assert client.get(path).status_code == 404


def test_admin_guard(client):
    from api.index import app
    from backend.auth import current_user
    app.dependency_overrides[current_user] = lambda: {'id_usuario': 1, 'tipo_usuario': 'cliente'}
    try:
        assert client.delete('/api/produtos/1').status_code == 403
    finally:
        app.dependency_overrides.clear()


def test_database_unavailable(client, monkeypatch):
    def unavailable():
        raise DatabaseError('private database details', errno=2003)
    monkeypatch.setattr('backend.database.connect', unavailable)
    response = client.get('/api/produtos')
    assert response.status_code == 503
    assert 'private' not in response.text


def test_static_and_api_routes(client):
    for path in ['/', '/loja.html', '/login.html', '/cadastro.html', '/admin.html', '/css/style.css', '/js/api.js', '/imagens/placeholder.svg']:
        assert client.get(path).status_code == 200
    assert client.get('/api/health').json() == {'status': 'ok'}
    assert client.get('/api/unknown').status_code == 404
    assert client.get('/api/gerar-senha').headers['cache-control'] == 'no-store'
    assert client.get('/.env').status_code == 404


def test_production_requires_tls(monkeypatch):
    monkeypatch.setenv('APP_ENV', 'production')
    monkeypatch.setenv('DB_SSL', 'false')
    settings.cache_clear()
    with pytest.raises(RuntimeError):
        settings()
    settings.cache_clear()
```

O que este arquivo faz:

- Verifica funcionalidades e proteções no ambiente de testes.


## ARQUIVO: privada/vercel.json

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "framework": "fastapi"
}
```

O que este arquivo faz:

- Seleciona o suporte nativo ao FastAPI.

from pathlib import Path
import re
root = Path(__file__).resolve().parents[1]
pub = root / 'workspace/publico'
private = root / 'workspace/privada'
def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')

# Mantém os cards existentes, substituindo compra imediata por carrinho.
script = (pub / 'js/loja.js').read_text(encoding='utf-8')
script = "import {adicionarProduto} from './carrinho.js';\n" + script
script = script.replace("let demo = new URLSearchParams(location.search).get('demo') === '1';", 'const demo = false;')
start = script.index('    if (!sessionStorage.getItem')
end = script.index('\n  });', start)
script = script[:start] + '''    try {
      if (!quantity.reportValidity()) return;
      adicionarProduto(product, Number(quantity.value));
      message('Produto adicionado ao carrinho.', 'success');
      document.querySelector('#message').scrollIntoView({block: 'nearest'});
    } catch (error) { message(error.message); }''' + script[end:]
start = script.index('    if (demo) {', script.index('async function loadProducts'))
end = script.index('    if (version !== requestVersion) return;', script.index('        return;', start)) if False else script.index('    document.querySelector(\'#demo-notice\')', start)
script = script[:start] + '''    const filters = new URLSearchParams({busca: search.value.trim(), categoria: category, ordem: sort.value});
    products = await apiRequest(`/produtos?limite=${limit}&offset=${offset}&${filters}`);
    if (version !== requestVersion) return;
''' + script[end:]
script = script.replace("    document.querySelector('#demo-notice').hidden = !demo;\n", '')
script = script.replace('demo = false; offset = 0;', 'offset = 0;')
script = script.replace('`${product.quantidade_estoque} unidades ${demo ? \'ilustrativas\' : \'disponíveis\'}`', '(product.quantidade_estoque <= 3 ? `Últimas ${product.quantidade_estoque} unidades` : `Estoque: ${product.quantidade_estoque} unidades`)')
# Remove os ramos de demonstração: a vitrine sempre depende do MySQL.
script = script.replace('const demo = false;\n', '')
script = script.replace("demo ? 'Conhecer produto ↗' : ", '').replace('!demo && ', '')
script = script.replace('  if (demo) quantity.hidden = true;\n', '')
start = script.index('    if (demo) {')
end = script.index('    try {', start)
script = script[:start] + script[end:]
write(pub / 'js/loja.js', script)

loja = (pub / 'loja.html').read_text(encoding='utf-8')
loja = re.sub(r'<div id="demo-notice".*?</div>', '', loja)
loja = loja.replace('<button data-category="Componentes"', '<button data-category="Acessórios" aria-pressed="false">Acessórios</button><button data-category="Componentes"')
write(pub / 'loja.html', loja)

# Página inicial própria, com destaques dinâmicos (mesmo script da loja).
home = loja.replace('<title>Loja | Dessik</title>', '<title>Dessik | Tecnologia para o seu dia a dia</title>')
home = home.replace('href="#catalogo">Explorar coleção', 'href="/loja.html">Ver Produtos')
home = home.replace('<span class="hero-caption">', '<a class="home-register" href="/cadastro.html">Criar Conta ↗</a><span class="hero-caption">')
home = home.replace('Encontre seu essencial<span>.</span>', 'Produtos em destaque<span>.</span>')
home = home.replace('</main>', '''<section class="benefits" aria-label="Benefícios da loja">
<article><span>01 / ESCOLHA</span><h2>Seu próximo upgrade.</h2><p>Tecnologia para estudar, criar e jogar, em um só lugar.</p></article>
<article><span>02 / CONFIANÇA</span><h2>Conta protegida.</h2><p>Senhas protegidas e acesso exclusivo aos seus pedidos.</p></article>
<article><span>03 / TRANQUILIDADE</span><h2>Experimente à vontade.</h2><p>Uma loja acadêmica com compras simuladas, sem cobrança.</p></article>
</section></main>''')
home = home.replace('<body class="store-page">', '<body class="store-page home-page">')
write(pub / 'index.html', home)

header = loja[:loja.index('<main id="main">')]
header = header.replace('<title>Loja | Dessik</title>', '<title>Carrinho | Dessik</title>').replace('/js/loja.js?v=3', '/js/carrinho.js')
footer = loja[loja.index('<footer>'):]
write(pub / 'carrinho.html', header + '''<main id="main">
<section class="intro"><div><p class="eyebrow">SEU PRÓXIMO UPGRADE</p><h1>Meu carrinho<span>.</span></h1><p>Confira seus produtos e finalize a compra simulada.</p></div><a href="/loja.html" class="button secondary">Continuar comprando ↗</a></section>
<div id="message" class="message" role="status" aria-live="polite" hidden></div>
<div class="cart-layout"><section id="cart-items" aria-label="Itens do carrinho"></section>
<aside class="form-panel"><h2>Resumo do pedido</h2><p>Total estimado</p><strong class="price" id="cart-total">R$ 0,00</strong><p class="hint">Compra simulada. Sem pagamento nem entrega.</p>
<div class="fields"><button id="checkout" disabled>Finalizar pedido</button><button id="refresh-cart" class="secondary">Atualizar carrinho</button><a id="cart-login" href="/login.html" hidden>Entrar na minha conta</a><a href="/pedidos.html">Meus pedidos</a></div></aside></div></main>''' + footer)

cad = (pub / 'js/cadastro.js').read_text(encoding='utf-8')
cad += '''\n// Ao sair do campo, consulta automaticamente um CEP completo.
form.elements.cep.addEventListener('blur', () => {
  if (form.elements.cep.value.replace(/\\D/g, '').length === 8) document.querySelector('#lookup-cep').click();
});
'''
write(pub / 'js/cadastro.js', cad)

# Fundo claro solicitado, mantendo a marca grafite e o destaque laranja no hero.
css = '''
/* Superfícies claras: uma única identidade em cadastro, loja e administração. */
:root{color-scheme:light;--ink:#242932;--muted:#59616e;--line:#dce0e6;--bg:#f4f5f7;--red:#a12535}
body{background:var(--bg);color:var(--ink)}
.navbar{background:#fff;border-color:#ddd}.brand{color:#252932}nav a,nav a[aria-current=page]{color:#353c48}nav a.button{background:#252932;color:#fff}
a{color:#984120}a:hover{color:#ad4822}.secondary{background:#e9ecf0;color:#29303b;border-color:#c9ced6}.secondary:hover{background:#dce1e8}
.hero{color:#f4f5f7}.hero a{color:#291a12}.hero .home-register{color:#ffb394;margin-top:16px;font-size:.9rem}
.card,.form-panel,.table-wrap,.cart-item{background:#fff;border-color:#dce0e6;box-shadow:0 4px 16px #27314208}
.card h3,.price,.intro h1{color:#252932}.card .category,.eyebrow{color:#984120}.description,.intro p,.form-intro p,.muted,.hint{color:#59616e}
.stock{color:#246743}.stock.out{color:#a12535}.collection-strip{color:#59616e}.catalog-bar{border-color:#dce0e6}.catalog-bar h2{color:#252932}
.category-tabs button{background:#fff;color:#4d5562;border-color:#cbd0d8}.category-tabs button[aria-pressed=true]{background:#252932;color:#fff;border-color:#252932}
.search-box,.sort-box select,input,select,textarea,.form-panel input,.form-panel textarea{background:#fff;color:#242932;border-color:#bdc5d0}
.search-box input{background:transparent;color:#242932}.sort-box>span,.form-panel label,.form-panel .hint,.form-foot,.form-intro a{color:#59616e}
.form-foot a{color:#984120}.form-section{border-color:#dce0e6}.empty{background:white;color:#59616e;border-color:#bdc5d0}
.message.error{color:#8d2133;background:#fff0f2;border-color:#e9bfc7}.message.success{color:#215f3e;background:#eaf6ef;border-color:#b1d9bf}
th{background:#edf0f4;color:#3d4552}td,th{border-color:#dce0e6}td{color:#454e5d}
footer{border-color:#dce0e6;color:#59616e}.footer-links a,.footer-main p,.footer-bottom{color:#59616e}.footer-bottom{border-color:#dce0e6}
dialog{background:white;color:#242932;border-color:#bdc5d0}dialog p{color:#59616e}
.order-card{background:white;border-color:#dce0e6}.order-card>div:last-child{color:#59616e}.order-status{color:#246743}
.cart-layout{display:grid;grid-template-columns:1fr 340px;gap:28px;align-items:start}.cart-item{border:1px solid #dce0e6;border-radius:12px;padding:24px;margin-bottom:16px;display:flex;align-items:center;justify-content:space-between;gap:20px}.cart-item h2{font-size:1.2rem;margin-bottom:8px}.cart-item input{max-width:110px}.cart-item p{color:#59616e}.cart-item strong{white-space:nowrap}
.benefits{display:grid;grid-template-columns:repeat(3,1fr);gap:26px;margin-top:65px}.benefits article{border-top:2px solid #dce0e6;padding-top:22px}.benefits span{font-size:.7rem;letter-spacing:1px;color:#984120}.benefits h2{font-size:1.25rem;margin-top:15px}.benefits p{color:#59616e}
.home-page .catalog-tools,.home-page .category-tabs,.home-page .pagination{display:none}.home-page .card:nth-child(n+5){display:none}
@media(max-width:850px){.nav-inner{flex-wrap:wrap}.cart-layout{grid-template-columns:1fr}.benefits{grid-template-columns:1fr}.cart-item{flex-wrap:wrap}.nav-inner nav{flex-wrap:wrap}.hero h1{overflow-wrap:anywhere}}
@media(max-width:520px){.nav-inner{flex-direction:column;align-items:flex-start}.nav-inner nav{justify-content:flex-start}nav>a[aria-current=page]{display:inline}.cart-item{padding:18px}.benefits{margin-top:35px}}
'''
with (pub / 'css/storefront.css').open('a', encoding='utf-8') as file: file.write(css)

# Corrige a indentação do comentário inserido no cadastro.
main = (private / 'backend/main.py').read_text(encoding='utf-8')
main = main.replace('        cursor.execute(\n                """INSERT INTO usuarios', '            cursor.execute(\n                """INSERT INTO usuarios')
write(private / 'backend/main.py', main)
print('Carrinho, páginas e tema claro preparados.')

from pathlib import Path

root = Path(__file__).resolve().parents[1]
public = root / 'public'
source = (public / 'loja.html').read_text(encoding='utf-8')
start = source.index('<section class="hero"')
end = source.index('<div id="demo-notice"', start)
hero = '''<section class="hero" aria-labelledby="hero-title">
  <div class="hero-copy">
    <p class="collection-label">TECNOLOGIA COM A SUA IDENTIDADE <span>01 / 08</span></p>
    <h1 id="hero-title">MENOS LIMITES.<br><em>MAIS VOCÊ.</em></h1>
    <p>Do play ao próximo projeto. Encontre o que falta no seu setup e faça do seu jeito.</p>
    <a class="button hero-button" href="#catalogo">Explorar coleção <span aria-hidden="true">↗</span></a>
    <span class="hero-caption">ESSENTIALS COLLECTION — 2026</span>
  </div>
  <div class="hero-showcase">
    <span class="showcase-kicker">EM DESTAQUE / ÁUDIO</span>
    <div class="hero-product product-art art-headset" role="img" aria-label="Ilustração do headset Wave preto com detalhes azuis"></div>
    <div class="showcase-bottom"><div><span>OUÇA CADA DETALHE.</span><strong>Headset Wave</strong></div><a href="#catalogo" aria-label="Explorar produtos">↗</a></div>
  </div>
</section>
<div class="collection-strip"><span>FEITO PARA O SEU DIA A DIA</span><span>CRIAR <b>✳</b> TRABALHAR <b>✳</b> JOGAR <b>✳</b> EXPLORAR</span></div>
'''
source = source[:start] + hero + source[end:]
start = source.index('<section id="catalogo"')
end = source.index('<div id="products"', start)
catalog = '''<section id="catalogo" aria-labelledby="catalog-title">
  <div class="catalog-bar"><div><p class="eyebrow">O PRÓXIMO UPGRADE É SEU</p><h2 id="catalog-title">Encontre seu essencial<span>.</span></h2><span id="product-count" class="muted" aria-live="polite">Carregando produtos…</span></div><button id="reload" class="secondary">Atualizar ↻</button></div>
  <div class="catalog-tools">
    <label class="search-box"><span aria-hidden="true">⌕</span><span class="sr-only">Buscar produtos</span><input id="search" type="search" placeholder="O que falta no seu setup?" maxlength="100" autocomplete="off"></label>
    <label class="sort-box"><span>Ordenar por</span><select id="sort"><option value="recentes">Seleção Dessik</option><option value="menor-preco">Menor preço</option><option value="maior-preco">Maior preço</option></select></label>
  </div>
  <div class="category-tabs" role="group" aria-label="Filtrar por categoria">
    <button data-category="" aria-pressed="true">Todos os produtos</button><button data-category="Computadores" aria-pressed="false">Computadores</button><button data-category="Periféricos" aria-pressed="false">Periféricos</button><button data-category="Monitores" aria-pressed="false">Monitores</button><button data-category="Áudio" aria-pressed="false">Áudio</button><button data-category="Componentes" aria-pressed="false">Componentes</button>
  </div>
'''
source = source[:start] + catalog + source[end:]
for name in ('index.html', 'loja.html'):
    (public / name).write_text(source, encoding='utf-8')

orders = source[:source.index('<main id="main">')] + '''<main id="main"><section class="intro"><div><p class="eyebrow">SUA CONTA / HISTÓRICO</p><h1>Meus pedidos<span>.</span></h1><p>Suas escolhas, todas em um só lugar.</p></div><a class="button secondary" href="/loja.html">Voltar à loja ↗</a></section><div id="message" class="message" role="status" hidden></div><section id="orders-content" hidden><div class="catalog-bar"><span id="order-count" class="muted"></span><button id="reload-orders" class="secondary">Atualizar ↻</button></div><div id="orders-list" aria-busy="false"></div></section></main>''' + source[source.index('<footer>'):]
orders = orders.replace('<title>Loja | Dessik</title>', '<title>Meus pedidos | Dessik</title>').replace('/js/loja.js', '/js/pedidos.js').replace('class="store-page"', 'class="account-page"')
(public / 'pedidos.html').write_text(orders, encoding='utf-8')

for path in public.glob('*.html'):
    html = path.read_text(encoding='utf-8')
    html = html.replace('<a href="/admin.html" data-admin', '<a href="/pedidos.html" data-session hidden>Meus pedidos</a><a href="/admin.html" data-admin')
    html = html.replace('Loja fictícia · Compras simuladas, sem cobrança', 'SEU SETUP, SUAS REGRAS. <span>Loja fictícia · Sem cobranças reais</span>')
    footer = html.index('<footer>')
    html = html[:footer] + '''<footer><div class="footer-main"><div><a class="brand" href="/loja.html">dessik<span>.</span></a><p>Tecnologia para quem faz<br>do próprio jeito.</p></div><div class="footer-links"><a href="/loja.html">Explorar produtos</a><a href="/login.html">Minha conta</a><a href="/cadastro.html">Criar conta</a></div></div><div class="footer-bottom"><span>© 2026 Dessik. Projeto acadêmico.</span><span>Produtos fictícios. Compras simuladas. Nenhuma cobrança.</span></div></footer></body></html>'''
    # Substitui os dois arquivos de estilo pelo tema consolidado com base reutilizada.
    html = html.replace('/css/storefront.css', '/css/storefront.css?v=3')
    html = html.replace('/js/loja.js', '/js/loja.js?v=3')
    path.write_text(html, encoding='utf-8')
print('Vitrine, navegação, filtros e página de pedidos criados.')

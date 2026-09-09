from pathlib import Path
import json
import re

root = Path(__file__).resolve().parents[1]
public = root / 'public'
html = (public / 'loja.html').read_text(encoding='utf-8')
start = html.index('<section class="intro">')
end = html.index('<div id="message"', start)
hero = '''<section class="hero" aria-labelledby="hero-title">
<div class="hero-copy"><span class="collection-label"><span></span> DESSIK ESSENTIALS / VOL. 01</span>
<h1 id="hero-title">Seu espaço.<br>Seu estilo.<br><em>Seu próximo nível.</em></h1>
<p>O essencial para transformar suas ideias em realidade. Tecnologia que combina com você.</p>
<a class="button hero-button" href="#catalogo">Encontre seu upgrade <span aria-hidden="true">↗</span></a>
<div class="hero-caption"><span>01 — 08</span> Uma seleção para criar, jogar e ir além.</div></div>
<div class="hero-showcase"><span class="showcase-kicker">DESIGN QUE VOCÊ SENTE.</span>
<div class="hero-product product-art art-headset" role="img" aria-label="Headset fictício preto com detalhes azuis"></div>
<div class="showcase-bottom"><div><span>ÁUDIO / ESSENTIALS</span><strong>Headset Wave</strong></div><a href="#catalogo" aria-label="Explorar o catálogo">↙</a></div>
</div></section>
<div class="store-values" aria-label="Sobre a loja"><div><span aria-hidden="true">✳</span><p><strong>Escolhas com personalidade</strong><span>Do primeiro setup ao próximo upgrade</span></p></div><div><span aria-hidden="true">◇</span><p><strong>Estoque transparente</strong><span>Disponibilidade em cada produto</span></p></div><div><span aria-hidden="true">↗</span><p><strong>Explore sem compromisso</strong><span>Uma experiência de compra fictícia</span></p></div></div>
<div id="demo-notice" class="demo-notice" hidden><span><strong>Catálogo demonstrativo</strong> · Produtos e preços fictícios. Compras disponíveis somente com a API e o banco conectados.</span><a href="/loja.html">Tentar loja conectada ↗</a></div>
'''
html = html[:start] + hero + html[end:]
html = html.replace('<section aria-labelledby="catalog-title">', '<section id="catalogo" aria-labelledby="catalog-title">')
html = html.replace('<h2 id="catalog-title">Nossos produtos</h2>', '<p class="eyebrow">CURADORIA DESSIK</p><h2 id="catalog-title">Pequenos detalhes.<br>Grandes possibilidades.</h2>')
html = html.replace('>Atualizar</button>', '>Atualizar catálogo ↻</button>')
html = html.replace('<body>', '<body class="store-page">')
html = html.replace('<a href="/loja.html">Produtos</a>', '<a href="/loja.html" aria-current="page">Explorar produtos</a>')
for name in ('loja.html', 'index.html'):
    (public / name).write_text(html, encoding='utf-8')

sql_path = root / 'database' / 'dados.sql'
sql = sql_path.read_text(encoding='utf-8').replace('/images/placeholder.svg', '/images/catalogo-dessik.png')
sql_path.write_text(sql, encoding='utf-8')
products = []
pattern = r"SELECT (\d+),'([^']*)','([^']*)','([^']*)',([\d.]+),(\d+),'([^']*)'"
for match in re.finditer(pattern, sql):
    ident, name, description, category, price, stock, image = match.groups()
    products.append(dict(id_produto=int(ident), nome=name, descricao=description, categoria=category,
                         preco=price, quantidade_estoque=int(stock), imagem_url=image))
assert len(products) == 8
(public / 'data').mkdir(exist_ok=True)
(public / 'data' / 'produtos-demo.json').write_text(json.dumps(products, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

for name in ('cadastro.html', 'login.html', 'admin.html'):
    path = public / name
    source = path.read_text(encoding='utf-8').replace('<body>', '<body class="account-page">')
    path.write_text(source, encoding='utf-8')
print('Nova estrutura visual e oito produtos de demonstração preparados.')

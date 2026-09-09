from pathlib import Path

root = Path(__file__).resolve().parents[1]
for path in (root / 'public').glob('*.html'):
    source = path.read_text(encoding='utf-8')
    source = source.replace('<link rel="stylesheet" href="/css/style.css">',
        '<link rel="stylesheet" href="/css/style.css"><link rel="stylesheet" href="/css/storefront.css">')
    path.write_text(source, encoding='utf-8')
readme = root / 'README.md'
text = readme.read_text(encoding='utf-8')
text = text.replace('As imagens iniciais são placeholders locais identificados como ilustrativos, sem dependência de serviço externo.',
    'Os oito produtos fictícios usam ilustrações locais criadas com IA, organizadas em um atlas visual `public/images/catalogo-dessik.png`. O CSS recorta cada item visualmente. A correspondência usa o nome do produto; imagens próprias cadastradas no administrador continuam sendo exibidas normalmente.')
text = text.replace('Em indisponibilidade do banco, aparece um erro real; não há catálogo falso de fallback.',
    'Em indisponibilidade da API/banco, a página informa o erro e abre um catálogo demonstrativo identificado, com oito itens de `public/data/produtos-demo.json`. Nesse modo não são criados pedidos nem apresentados estoques como reais. É possível abri-lo diretamente em `/loja.html?demo=1`. O botão Atualizar catálogo tenta reconectar à API. O catálogo conectado continua vindo exclusivamente do MySQL.')
text = text.replace('│   ├── css/style.css', '│   ├── css/style.css\n│   ├── css/storefront.css\n│   ├── data/produtos-demo.json')
text = text.replace('│   └── images/placeholder.svg', '│   ├── images/placeholder.svg\n│   └── images/catalogo-dessik.png')
readme.write_text(text, encoding='utf-8')

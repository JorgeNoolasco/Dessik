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

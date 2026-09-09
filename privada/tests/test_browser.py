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

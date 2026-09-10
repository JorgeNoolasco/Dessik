import { test, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { apiRequest, apiUrl, productPage, limparSessao } from '../js/api.js';

const storage = new Map();
globalThis.sessionStorage = { getItem: key => storage.get(key) ?? null, setItem: (key, value) => storage.set(key, value), removeItem: key => storage.delete(key) };
globalThis.document = { querySelectorAll: () => [] };
beforeEach(() => storage.clear());

test('base única, prefixo único e bloqueio de URL externa', () => {
    for (const path of ['/produtos', '/api/produtos', '/api/api/produtos']) {
        assert.equal(apiUrl(path), 'https://dessik-back-end.vercel.app/api/produtos');
    }
    assert.equal(apiUrl('/'), 'https://dessik-back-end.vercel.app/');
    for (const path of ['https://example.com', '//example.com', '/../login', '/\\example.com']) assert.throws(() => apiUrl(path));
});

test('JSON e Bearer somente nas rotas protegidas; logout remove sessão', async () => {
    storage.set('dessik_token', 'test-token');
    storage.set('dessik_login_ok', '1');
    const requests = [];
    globalThis.fetch = async (url, options) => { requests.push({ url, ...options }); return Response.json({ ok: true }); };
    await apiRequest('/login', { method: 'POST', body: { email: 'teste@example.com', senha: 'literal ' } });
    await apiRequest('/produtos/1/entrada', { method: 'POST', auth: true, body: { quantidade: 2 } });
    assert.equal(requests[0].headers.Authorization, undefined);
    assert.equal(JSON.parse(requests[0].body).senha, 'literal ');
    assert.equal(requests[0].headers['Content-Type'], 'application/json');
    assert.equal(requests[1].headers.Authorization, 'Bearer test-token');
    limparSessao();
    assert.equal(storage.size, 0);
    await assert.rejects(apiRequest('/me', { auth: true }), { status: 401 });
    assert.equal(requests.length, 2);
});

for (const status of [401, 403, 404, 422, 500, 502, 503, 504]) {
    test(`HTTP ${status} preservado mesmo com HTML; 401 limpa sessão`, async () => {
        storage.set('dessik_token', 'expired');
        globalThis.fetch = async () => new Response('<html>error</html>', { status });
        await assert.rejects(apiRequest('/me', { auth: true }), error => error.status === status && error.message.length > 10);
        assert.equal(storage.has('dessik_token'), status !== 401);
    });
}

test('validação FastAPI padrão e customizada, mensagens e JSON inválido', async () => {
    for (const body of [{ detail: [{ loc: ['body', 'email'], msg: 'Inválido' }] }, { erros: [{ campo: 'email', mensagem: 'Inválido' }] }]) {
        globalThis.fetch = async () => Response.json(body, { status: 422 });
        await assert.rejects(apiRequest('/usuarios'), { status: 422, message: 'email: Inválido' });
    }
    globalThis.fetch = async () => Response.json({ detail: 'Sem permissão' }, { status: 403 });
    await assert.rejects(apiRequest('/produtos'), { status: 403, message: 'Sem permissão' });
    globalThis.fetch = async () => new Response('bad JSON');
    await assert.rejects(apiRequest('/produtos'), /JSON válido/);
    globalThis.fetch = async () => new Response(null, { status: 204 });
    assert.equal(await apiRequest('/produtos/1', { method: 'DELETE' }), null);
});

test('rede indisponível e timeout liberam a requisição', async () => {
    globalThis.fetch = async () => { throw new TypeError('Failed to fetch'); };
    await assert.rejects(apiRequest('/produtos'), /conectar à loja/);
    globalThis.fetch = (_url, { signal }) => new Promise((_resolve, reject) => signal.addEventListener('abort', () => reject(new DOMException('Abort', 'AbortError'))));
    await assert.rejects(apiRequest('/produtos', { timeoutMs: 5 }), /demorou/);
});

test('paginação mantém filtros, detecta última página e rejeita contrato inválido', async () => {
    let requested;
    globalThis.fetch = async url => { requested = new URL(url); return Response.json([1, 2, 3, 4, 5]); };
    assert.deepEqual(await productPage({ limite: 4, offset: 4, busca: 'á & b', categoria: 'Teste', ordem: 'menor-preco' }), { products: [1, 2, 3, 4], hasNext: true });
    assert.equal(requested.searchParams.get('busca'), 'á & b');
    assert.equal(requested.searchParams.get('categoria'), 'Teste');
    assert.equal(requested.searchParams.get('offset'), '4');
    for (const products of [[], [1, 2, 3, 4]]) {
        globalThis.fetch = async () => Response.json(products);
        assert.deepEqual(await productPage({ limite: 4 }), { products, hasNext: false });
    }
    globalThis.fetch = async () => Response.json({ products: [] });
    await assert.rejects(productPage({ limite: 4 }), /catálogo inválido/);
});

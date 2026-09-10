// Vitrine: cartões, busca, categorias, ordenação e paginação de produtos.
import {
    adicionarProduto
} from './carrinho.js';
import {
    siteUrl,
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

// Monta um cartão acessível com imagem, preço, estoque e seleção de quantidade.
function card(product) {
    const article = element('article', undefined, 'card');
    const visual = element('div', undefined, 'product-visual');
    const image = element('img');
    // Imagens locais pertencem ao projeto; URLs externas são mantidas.
    image.src = /^\/?imagens\//.test(product.imagem_url)
        ? siteUrl(product.imagem_url.replace(/^\//, ''))
        : product.imagem_url;
    image.alt = product.nome;
    image.loading = 'lazy';
    image.addEventListener('error', () => image.src = siteUrl('imagens/placeholder.svg'), {
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
// Busca a página de produtos e atualiza a listagem e os botões de paginação.
async function loadProducts(clear = true) {
    // Ignora respostas antigas quando uma busca mais recente já foi iniciada.
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
        // Restaura os controles mesmo quando a operação falha.
        if (version === requestVersion) grid.setAttribute('aria-busy', 'false');
    }
}
// Aguarda 250 ms sem digitação antes de buscar, reduzindo as requisições.
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
// Reinicia a paginação quando a ordenação muda.
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
// Volta uma página sem permitir deslocamento negativo.
document.querySelector('#previous').onclick = () => {
    offset = Math.max(0, offset - limit);
    loadProducts();
};
// Avança a listagem pelo limite de produtos por página.
document.querySelector('#next').onclick = () => {
    offset += limit;
    loadProducts();
};
document.querySelector('#reload').onclick = () => {
    offset = 0;
    loadProducts();
};
loadProducts();

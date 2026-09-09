import {apiRequest, message, money, element, setupSession, confirmAction} from './api.js';
setupSession();
const grid = document.querySelector('#products');
let offset = 0;
const limit = 12;
let category = '';
let requestVersion = 0;
const search = document.querySelector('#search');
const sort = document.querySelector('#sort');
let demo = new URLSearchParams(location.search).get('demo') === '1';
const productArt = new Map([
  ['Notebook Horizon 14', 'notebook'], ['Mouse Pulse', 'mouse'],
  ['Teclado mecânico Type', 'teclado'], ['Monitor View 24', 'monitor'],
  ['Headset Wave', 'headset'], ['Webcam Focus', 'webcam'],
  ['SSD Sprint 1 TB', 'ssd'], ['Memória RAM Flux 16 GB', 'ram'],
]);
function card(product) {
  const article = element('article', undefined, 'card');
  const visual = element('div', undefined, 'product-visual');
  const image = element('img');
  image.src = product.imagem_url;
  image.alt = product.nome;
  image.loading = 'lazy';
  image.addEventListener('error', () => image.src = '/images/placeholder.svg', {once: true});
  const art = productArt.get(product.nome);
  if (art && ['/images/placeholder.svg', '/images/catalogo-dessik.png'].includes(product.imagem_url)) {
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
    element('p', product.quantidade_estoque ? `${product.quantidade_estoque} unidades ${demo ? 'ilustrativas' : 'disponíveis'}` : 'Produto indisponível',
      product.quantidade_estoque ? 'stock' : 'stock out'));
  const row = element('div', undefined, 'buy-row');
  const quantity = element('input');
  quantity.type = 'number'; quantity.min = '1'; quantity.max = String(Math.min(product.quantidade_estoque, 1000)); quantity.value = '1';
  quantity.setAttribute('aria-label', `Quantidade de ${product.nome}`);
  quantity.disabled = product.quantidade_estoque === 0;
  const button = element('button', demo ? 'Conhecer produto ↗' : product.quantidade_estoque ? 'Comprar ↗' : 'Indisponível');
  if (demo) quantity.hidden = true;
  button.disabled = !demo && product.quantidade_estoque === 0;
  button.addEventListener('click', async () => {
    if (demo) {
      await confirmAction(product.nome, `${product.descricao} Preço fictício: ${money(product.preco)}. Para simular uma compra com estoque, configure o banco e abra a loja conectada.`, 'Entendi');
      return;
    }
    if (!sessionStorage.getItem('dessik_token')) { location.assign('/login.html'); return; }
    const amount = Number(quantity.value);
    if (!Number.isInteger(amount) || amount < 1 || !quantity.reportValidity()) {
      message('Informe uma quantidade válida.'); return;
    }
    button.disabled = true;
    try {
      const confirmed = await confirmAction('Simular compra', `${amount} × ${product.nome} — ${money(Number(product.preco) * amount)}. Nenhuma cobrança será realizada.`, 'Confirmar compra');
      if (!confirmed) return;
      const order = await apiRequest('/pedidos', {method: 'POST', auth: true,
        body: {itens: [{id_produto: product.id_produto, quantidade: amount}]}});
      message(`Pedido #${order.id_pedido} confirmado · ${money(order.valor_total)}. ${order.mensagem}`, 'success');
      await loadProducts(false);
    } catch (error) {
      message(error.message);
      if (error.status === 409) await loadProducts(false);
    } finally { button.disabled = product.quantidade_estoque === 0; }
  });
  row.append(quantity, button); body.append(row); article.append(visual, body);
  return article;
}
async function loadProducts(clear = true) {
  const version = ++requestVersion;
  if (clear) message();
  grid.setAttribute('aria-busy', 'true');
  try {
    let products;
    if (demo) {
      const response = await fetch('/data/produtos-demo.json');
      if (!response.ok) throw new Error('Não foi possível abrir o catálogo demonstrativo.');
      const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
      const term = normalize(search.value.trim());
      products = (await response.json()).filter(product =>
        (!category || product.categoria === category) && normalize(`${product.nome} ${product.descricao}`).includes(term));
      if (sort.value !== 'recentes') products.sort((a, b) => sort.value === 'menor-preco' ? Number(a.preco) - Number(b.preco) : Number(b.preco) - Number(a.preco));
      products = products.slice(offset, offset + limit);
    } else {
      try {
        const filters = new URLSearchParams({busca: search.value.trim(), categoria: category, ordem: sort.value});
        products = await apiRequest(`/produtos?limite=${limit}&offset=${offset}&${filters}`);
      } catch (error) {
        if (version !== requestVersion) return;
        // Demonstração identificada; não representa estoque ou pedidos de um banco ativo.
        demo = true;
        message('A loja conectada está indisponível. Você está vendo apenas o catálogo demonstrativo.', '');
        await loadProducts(false);
        return;
      }
    }
    if (version !== requestVersion) return;
    document.querySelector('#demo-notice').hidden = !demo;
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
  } finally { if (version === requestVersion) grid.setAttribute('aria-busy', 'false'); }
}
let searchTimer;
search.addEventListener('input', () => {
  clearTimeout(searchTimer);
  // Invalida resultados anteriores ainda em trânsito antes da próxima busca.
  requestVersion++;
  searchTimer = setTimeout(() => { offset = 0; loadProducts(); }, 250);
});
sort.addEventListener('change', () => { offset = 0; loadProducts(); });
document.querySelectorAll('[data-category]').forEach(button => button.addEventListener('click', () => {
  category = button.dataset.category;
  document.querySelectorAll('[data-category]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  offset = 0;
  loadProducts();
}));
document.querySelector('#previous').onclick = () => { offset = Math.max(0, offset - limit); loadProducts(); };
document.querySelector('#next').onclick = () => { offset += limit; loadProducts(); };
document.querySelector('#reload').onclick = () => { demo = false; offset = 0; loadProducts(); };
loadProducts();

import {apiRequest, message, money, element, setupSession, confirmAction} from './api.js';
setupSession();
const grid = document.querySelector('#products');
let offset = 0;
const limit = 12;
function card(product) {
  const article = element('article', undefined, 'card');
  const image = element('img');
  image.src = product.imagem_url;
  image.alt = product.nome;
  image.loading = 'lazy';
  image.addEventListener('error', () => image.src = '/images/placeholder.svg', {once: true});
  const body = element('div', undefined, 'card-body');
  body.append(element('p', `${product.categoria} · #${product.id_produto}`, 'category'),
    element('h3', product.nome), element('p', product.descricao, 'description'),
    element('p', money(product.preco), 'price'),
    element('p', product.quantidade_estoque ? `${product.quantidade_estoque} unidades disponíveis` : 'Produto indisponível',
      product.quantidade_estoque ? 'stock' : 'stock out'));
  const row = element('div', undefined, 'buy-row');
  const quantity = element('input');
  quantity.type = 'number'; quantity.min = '1'; quantity.max = String(Math.min(product.quantidade_estoque, 1000)); quantity.value = '1';
  quantity.setAttribute('aria-label', `Quantidade de ${product.nome}`);
  quantity.disabled = product.quantidade_estoque === 0;
  const button = element('button', product.quantidade_estoque ? 'Comprar' : 'Indisponível');
  button.disabled = product.quantidade_estoque === 0;
  button.addEventListener('click', async () => {
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
  row.append(quantity, button); body.append(row); article.append(image, body);
  return article;
}
async function loadProducts(clear = true) {
  if (clear) message();
  grid.setAttribute('aria-busy', 'true');
  try {
    const products = await apiRequest(`/produtos?limite=${limit}&offset=${offset}`);
    grid.replaceChildren(...products.map(card));
    if (!products.length) grid.append(element('p', 'Nenhum produto nesta página.', 'empty'));
    document.querySelector('#product-count').textContent = `${products.length} produtos nesta página`;
    document.querySelector('#previous').disabled = offset === 0;
    document.querySelector('#next').disabled = products.length < limit;
    document.querySelector('#page-number').textContent = `Página ${offset / limit + 1}`;
  } catch (error) {
    grid.replaceChildren(element('p', 'Não foi possível carregar o catálogo.', 'empty'));
    message(error.message);
  } finally { grid.setAttribute('aria-busy', 'false'); }
}
document.querySelector('#previous').onclick = () => { offset = Math.max(0, offset - limit); loadProducts(); };
document.querySelector('#next').onclick = () => { offset += limit; loadProducts(); };
document.querySelector('#reload').onclick = () => loadProducts();
loadProducts();

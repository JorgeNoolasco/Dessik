import {apiRequest, message, money, element, setupSession, confirmAction} from './api.js';
const form = document.querySelector('#product-form');
const table = document.querySelector('#product-rows');
let editing = null;
let offset = 0;
const limit = 20;
function resetForm() {
  form.reset(); editing = null;
  document.querySelector('#form-title').textContent = 'Novo produto';
  document.querySelector('#save-product').textContent = 'Cadastrar produto';
}
async function loadProducts() {
  const products = await apiRequest(`/produtos?limite=${limit}&offset=${offset}`);
  table.replaceChildren();
  for (const product of products) {
    const row = element('tr');
    row.append(element('td', `#${product.id_produto} ${product.nome}`), element('td', money(product.preco)),
      element('td', String(product.quantidade_estoque)));
    const actions = element('td');
    const edit = element('button', 'Editar', 'secondary');
    edit.setAttribute('aria-label', `Editar ${product.nome}`);
    edit.onclick = () => {
      editing = product.id_produto;
      for (const key of ['nome', 'descricao', 'categoria', 'preco', 'quantidade_estoque', 'imagem_url']) form.elements[key].value = product[key];
      document.querySelector('#form-title').textContent = `Editar produto #${editing}`;
      document.querySelector('#save-product').textContent = 'Salvar alterações';
      form.elements.nome.focus();
    };
    const remove = element('button', 'Excluir', 'danger');
    remove.setAttribute('aria-label', `Excluir ${product.nome}`);
    remove.onclick = async () => {
      if (!await confirmAction('Excluir produto?', `O produto ${product.nome} será removido do catálogo.`, 'Excluir')) return;
      remove.disabled = true;
      try {
        await apiRequest(`/produtos/${product.id_produto}`, {method: 'DELETE', auth: true});
        if (editing === product.id_produto) resetForm();
        message('Produto excluído.', 'success');
        await loadProducts();
      } catch (error) { message(error.message); }
      finally { remove.disabled = false; }
    };
    actions.append(edit, remove); row.append(actions); table.append(row);
  }
  if (!products.length) {
    const row = element('tr'); const cell = element('td', 'Nenhum produto nesta página.');
    cell.colSpan = 4; row.append(cell); table.append(row);
  }
  document.querySelector('#previous').disabled = offset === 0;
  document.querySelector('#next').disabled = products.length < limit;
  document.querySelector('#page-number').textContent = `Página ${offset / limit + 1}`;
}
async function refresh() { try { await loadProducts(); } catch (error) { message(error.message); } }
form.addEventListener('submit', async event => {
  event.preventDefault();
  const button = document.querySelector('#save-product'); button.disabled = true;
  try {
    const body = Object.fromEntries(new FormData(form));
    body.quantidade_estoque = Number(body.quantidade_estoque);
    const data = await apiRequest(editing ? `/produtos/${editing}` : '/produtos',
      {method: editing ? 'PUT' : 'POST', auth: true, body});
    resetForm(); message(data.mensagem, 'success'); await refresh();
  } catch (error) { message(error.message); }
  finally { button.disabled = false; }
});
document.querySelector('#cancel-edit').onclick = resetForm;
document.querySelector('#previous').onclick = () => { offset = Math.max(0, offset - limit); refresh(); };
document.querySelector('#next').onclick = () => { offset += limit; refresh(); };
const user = await setupSession(true, true);
if (user) { document.querySelector('#admin-content').hidden = false; await refresh(); }

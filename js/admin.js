// Administração: cadastro, edição, exclusão confirmada e paginação de produtos.
import {
    apiRequest,
    productPage,
    message,
    money,
    element,
    setupSession,
    confirmAction
} from './api.js';
const form = document.querySelector('#product-form');
const table = document.querySelector('#product-rows');
let editing = null;
let offset = 0;
const limit = 20;
let loading = false;
const stockForm = document.querySelector('#stock-form');
let stockProduct = null;

// Limpa os campos e encerra o modo de edição.
function resetForm() {
    form.reset();
    editing = null;
    document.querySelector('#form-title').textContent = 'Novo produto';
    document.querySelector('#save-product').textContent = 'Cadastrar produto';
}
// Busca a página de produtos e atualiza a listagem e os botões de paginação.
async function loadProducts() {
    if (loading) return;
    loading = true;
    document.querySelector('#previous').disabled = true;
    document.querySelector('#next').disabled = true;
    try {
    let page = await productPage({ limite: limit, offset });
    if (!page.products.length && offset > 0) {
        offset = Math.max(0, offset - limit);
        page = await productPage({ limite: limit, offset });
    }
    const { products, hasNext } = page;
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
                await apiRequest(`/produtos/${product.id_produto}`, {
                    method: 'DELETE',
                    auth: true
                });
                if (editing === product.id_produto) resetForm();
                message('Produto excluído.', 'success');
                await loadProducts();
            } catch (error) {
                message(error.message);
            } finally {
                // Restaura os controles mesmo quando a operação falha.
                remove.disabled = false;
            }
        };
        const stock = element('button', 'Estoque', 'secondary');
        stock.onclick = () => {
            stockProduct = product.id_produto;
            stockForm.reset();
            stockForm.hidden = false;
            document.querySelector('#stock-product').textContent = `Estoque: ${product.nome} · Saldo consultado: ${product.quantidade_estoque}`;
            stockForm.elements.quantidade.focus();
        };
        actions.append(edit, stock, remove);
        row.append(actions);
        table.append(row);
    }
    if (!products.length) {
        const row = element('tr');
        const cell = element('td', 'Nenhum produto nesta página.');
        cell.colSpan = 4;
        row.append(cell);
        table.append(row);
    }
    document.querySelector('#previous').disabled = offset === 0;
    document.querySelector('#next').disabled = !hasNext;
    document.querySelector('#page-number').textContent = `Página ${offset / limit + 1}`;
    } finally {
        loading = false;
        document.querySelector('#previous').disabled = offset === 0;
    }
}
// Atualiza a tabela e apresenta eventuais falhas na área de mensagens.
async function refresh() {
    try {
        await loadProducts();
    } catch (error) {
        message(error.message);
    }
}
// Envia pela API sem recarregar a página; o botão é bloqueado durante o envio.
form.addEventListener('submit', async event => {
    event.preventDefault();
    const button = document.querySelector('#save-product');
    if (button.disabled || !form.reportValidity()) return;
    button.disabled = true;
    try {
        const body = Object.fromEntries(new FormData(form));
        body.quantidade = Number(body.quantidade_estoque);
        delete body.quantidade_estoque;
        const data = await apiRequest(editing ? `/produtos/${editing}` : '/produtos', {
            method: editing ? 'PUT' : 'POST',
            auth: true,
            body
        });
        resetForm();
        message(data.mensagem, 'success');
        await refresh();
    } catch (error) {
        message(error.message);
    } finally {
        // Restaura os controles mesmo quando a operação falha.
        button.disabled = false;
    }
});
// Movimentações relativas são calculadas e registradas pelo backend, com JWT.
stockForm.addEventListener('submit', async event => {
    event.preventDefault();
    const button = stockForm.querySelector('[type="submit"]');
    if (button.disabled || !stockProduct || !stockForm.reportValidity()) return;
    const productId = stockProduct;
    const operation = stockForm.elements.operacao.value;
    const quantidade = Number(stockForm.elements.quantidade.value);
    if (!['entrada', 'saida', 'ajuste'].includes(operation)) return;
    if (!Number.isInteger(quantidade) || quantidade < (operation === 'ajuste' ? 0 : 1)) {
        return message('Informe uma quantidade inteira válida. Entrada e saída devem ser maiores que zero.');
    }
    button.disabled = true;
    try {
        const data = await apiRequest(`/produtos/${productId}${operation === 'ajuste' ? '' : `/${operation}`}`, {
            method: operation === 'ajuste' ? 'PUT' : 'POST',
            auth: true,
            body: { quantidade }
        });
        stockForm.hidden = true;
        stockProduct = null;
        if (editing === productId) form.elements.quantidade_estoque.value = data.quantidade_estoque;
        message(`Estoque atualizado. Saldo confirmado: ${data.quantidade_estoque}.`, 'success');
        await refresh();
    } catch (error) {
        message(error.message);
    } finally {
        button.disabled = false;
    }
});
document.querySelector('#cancel-stock').onclick = () => { stockForm.hidden = true; stockProduct = null; };
document.querySelector('#cancel-edit').onclick = resetForm;
// Volta uma página sem permitir deslocamento negativo.
document.querySelector('#previous').onclick = () => {
    offset = Math.max(0, offset - limit);
    refresh();
};
// Avança a listagem pelo limite de produtos por página.
document.querySelector('#next').onclick = () => {
    offset += limit;
    refresh();
};
const user = await setupSession(true, true);
if (user) {
    document.querySelector('#admin-content').hidden = false;
    await refresh();
}

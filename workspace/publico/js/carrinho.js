import {
    apiRequest,
    element,
    message,
    money,
    setupSession
} from './api.js';

// Apenas IDs e quantidades: o preço verdadeiro será consultado na API.
export function lerCarrinho() {
    try {
        const itens = JSON.parse(sessionStorage.getItem('dessik_carrinho') || '[]');
        if (!Array.isArray(itens)) return [];
        const validos = [];
        for (const item of itens) {
            if (Number.isInteger(item.id_produto) && item.id_produto > 0 &&
                Number.isInteger(item.quantidade) && item.quantidade > 0 && item.quantidade <= 1000 &&
                !validos.some(outro => outro.id_produto === item.id_produto)) validos.push(item);
        }
        return validos.slice(0, 50);
    } catch {
        return [];
    }
}

function salvarCarrinho(itens) {
    sessionStorage.setItem('dessik_carrinho', JSON.stringify(itens));
}
export function adicionarProduto(produto, quantidade) {
    const itens = lerCarrinho();
    const existente = itens.find(item => item.id_produto === produto.id_produto);
    const total = (existente?.quantidade || 0) + quantidade;
    if (!Number.isInteger(quantidade) || quantidade < 1 || total > Math.min(produto.quantidade_estoque, 1000)) {
        throw new Error('Estoque insuficiente para essa quantidade no carrinho.');
    }
    if (existente) existente.quantidade = total;
    else {
        if (itens.length >= 50) throw new Error('O carrinho aceita até 50 produtos diferentes.');
        itens.push({
            id_produto: produto.id_produto,
            quantidade
        });
    }
    salvarCarrinho(itens);
}

async function iniciarCarrinho() {
    await setupSession();
    const lista = document.querySelector('#cart-items');
    const finalizar = document.querySelector('#checkout');
    let enviando = false;
    let atualizando = false;
    async function mostrarCarrinho() {
        if (atualizando || enviando) return;
        atualizando = true;
        document.querySelector('#refresh-cart').disabled = true;
        finalizar.disabled = true;
        lista.replaceChildren();
        const itens = lerCarrinho();
        let totalCentavos = 0;
        let valido = itens.length > 0;
        for (const item of itens) {
            const linha = element('article', undefined, 'cart-item');
            const detalhes = element('div');
            try {
                const produto = await apiRequest(`/produtos/${item.id_produto}`);
                const subtotal = Math.round(Number(produto.preco) * 100) * item.quantidade;
                totalCentavos += subtotal;
                detalhes.append(element('h2', produto.nome), element('p', `${money(produto.preco)} por unidade`));
                const label = element('label', 'Quantidade');
                const quantidade = element('input');
                quantidade.type = 'number';
                quantidade.min = '1';
                quantidade.max = String(Math.min(produto.quantidade_estoque, 1000));
                quantidade.value = String(item.quantidade);
                quantidade.addEventListener('change', async () => {
                    const valor = Number(quantidade.value);
                    if (!Number.isInteger(valor) || !quantidade.reportValidity()) return;
                    const atuais = lerCarrinho();
                    const atual = atuais.find(p => p.id_produto === item.id_produto);
                    if (atual) atual.quantidade = valor;
                    salvarCarrinho(atuais);
                    await mostrarCarrinho();
                });
                label.append(quantidade);
                detalhes.append(label);
                if (item.quantidade > produto.quantidade_estoque) {
                    valido = false;
                    detalhes.append(element('p', `Estoque insuficiente. Disponível: ${produto.quantidade_estoque}. Ajuste a quantidade ou remova o item.`, 'stock out'));
                }
                linha.append(detalhes, element('strong', money(subtotal / 100)));
            } catch (erro) {
                valido = false;
                linha.append(element('p', `Produto #${item.id_produto}: ${erro.message}`));
            }
            const remover = element('button', 'Remover', 'secondary');
            remover.addEventListener('click', async () => {
                salvarCarrinho(lerCarrinho().filter(p => p.id_produto !== item.id_produto));
                await mostrarCarrinho();
            });
            linha.append(remover);
            linha.querySelectorAll('button, input').forEach(campo => campo.disabled = true);
            lista.append(linha);
        }
        if (!itens.length) lista.append(element('p', 'Seu carrinho está vazio. Explore a loja para começar.', 'empty'));
        document.querySelector('#cart-total').textContent = money(totalCentavos / 100);
        finalizar.disabled = !valido || enviando;
        atualizando = false;
        lista.querySelectorAll('button, input').forEach(campo => campo.disabled = false);
        document.querySelector('#refresh-cart').disabled = false;
    }
    finalizar.addEventListener('click', async () => {
        if (enviando) return;
        if (!sessionStorage.getItem('dessik_token')) {
            message('Entre na sua conta para finalizar. Seus itens ficam guardados nesta aba.');
            document.querySelector('#cart-login').hidden = false;
            return;
        }
        enviando = true;
        finalizar.disabled = true;
        finalizar.textContent = 'Finalizando...';
        lista.querySelectorAll('button, input').forEach(campo => campo.disabled = true);
        try {
            const pedido = await apiRequest('/pedidos', {
                method: 'POST',
                auth: true,
                body: {
                    itens: lerCarrinho()
                }
            });
            salvarCarrinho([]);
            message(`Pedido #${pedido.id_pedido} realizado! Total: ${money(pedido.valor_total)}. Nenhuma cobrança.`, 'success');
        } catch (erro) {
            message(erro.message + ' Se houve perda de conexão, confira Meus pedidos antes de tentar novamente.');
        } finally {
            enviando = false;
            finalizar.textContent = 'Finalizar pedido';
            await mostrarCarrinho();
        }
    });
    document.querySelector('#refresh-cart').onclick = mostrarCarrinho;
    await mostrarCarrinho();
}
if (document.querySelector('#cart-items')) iniciarCarrinho().catch(erro => message(erro.message));

// Histórico: exige sessão e apresenta os pedidos retornados pelo servidor.
import {
    siteUrl,
    apiRequest,
    setupSession,
    element,
    money,
    message
} from './api.js';

const content = document.querySelector('#orders-content');
const list = document.querySelector('#orders-list');
const reload = document.querySelector('#reload-orders');

// Consulta pedidos autenticados e apresenta o histórico ou uma indicação de lista vazia.
async function loadOrders() {
    reload.disabled = true;
    list.setAttribute('aria-busy', 'true');
    message();
    try {
        const orders = await apiRequest('/pedidos', {
            auth: true
        });
        list.replaceChildren();
        if (!orders.length) {
            const empty = element('div', undefined, 'empty');
            const link = element('a', 'Explorar produtos ↗', 'button');
            link.href = siteUrl('html/loja.html');
            empty.append(element('h2', 'Seu primeiro upgrade começa aqui.'),
                element('p', 'Você ainda não fez nenhuma compra simulada.'), link);
            list.append(empty);
        }
        for (const order of orders) {
            const card = element('article', undefined, 'order-card');
            const date = new Date(order.data_pedido);
            const heading = element('div');
            heading.append(element('p', `PEDIDO #${order.id_pedido}`, 'eyebrow'),
                element('h2', money(order.valor_total)));
            const details = element('div');
            details.append(element('p', Number.isNaN(date.getTime()) ? 'Data não disponível' : date.toLocaleString('pt-BR')),
                element('span', 'Compra simulada • Sem cobrança', 'order-status'));
            card.append(heading, details);
            list.append(card);
        }
        document.querySelector('#order-count').textContent = `${orders.length} pedidos • até os 100 mais recentes`;
    } catch (error) {
        message(error.message);
    } finally {
        // Restaura os controles mesmo quando a operação falha.
        reload.disabled = false;
        list.setAttribute('aria-busy', 'false');
    }
}

// Permite consultar novamente o histórico sem recarregar a página.
reload.addEventListener('click', loadOrders);
if (await setupSession(true)) {
    content.hidden = false;
    await loadOrders();
}

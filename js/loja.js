// Vitrine: cartões, busca, categorias, ordenação e paginação de produtos.
import {
    adicionarProduto,
    estoqueDisponivel,
    lerCarrinho
} from './carrinho.js';
import {
    siteUrl,
    apiRequest,
    productPage,
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
// Guarda somente os cartões visíveis, evitando acumular ouvintes ao paginar.
let atualizarEstoques = [];
window.addEventListener('dessik:carrinho-atualizado', () => atualizarEstoques.forEach(atualizar => atualizar()));
// Reconsulta o servidor ao voltar pelo histórico, inclusive após remover itens ou comprar.
window.addEventListener('pageshow', event => {
    if (event.persisted) loadProducts(false);
});
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
        : product.imagem_url || siteUrl('imagens/placeholder.svg');
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
    let adicionando = false;
    // Atualiza texto, limites e controles usando o estoque menos a quantidade no carrinho.
    function atualizarEstoque() {
        const disponivel = estoqueDisponivel(product);
        const noCarrinho = lerCarrinho().find(item => item.id_produto === product.id_produto)?.quantidade || 0;
        const stock = body.querySelector('.stock');
        stock.textContent = `Disponível para adicionar: ${disponivel} unidades` + (noCarrinho ? ` · No carrinho: ${noCarrinho}` : '');
        stock.className = disponivel ? 'stock' : 'stock out';
        quantity.max = String(Math.max(0, Math.min(disponivel, 1000 - noCarrinho)));
        quantity.disabled = adicionando || Number(quantity.max) === 0;
        if (Number(quantity.value) > Number(quantity.max) || Number(quantity.value) < 1) quantity.value = Number(quantity.max) ? '1' : '0';
        button.disabled = quantity.disabled;
        button.textContent = adicionando ? 'Adicionando...' : Number(quantity.max) ? 'Comprar ↗' : noCarrinho ? 'Limite no carrinho' : 'Indisponível';
        visual.querySelector('.product-tag').textContent = disponivel ? 'DESSIK / ESSENTIALS' : noCarrinho ? 'NO CARRINHO' : 'ESGOTADO';
    }
    atualizarEstoques.push(atualizarEstoque);
    atualizarEstoque();
    button.addEventListener('click', async () => {
        if (adicionando || !quantity.reportValidity()) return;
        const desejada = Number(quantity.value);
        adicionando = true;
        atualizarEstoque();
        try {
            // Consulta o saldo atual antes de adicionar; cliques repetidos ficam bloqueados.
            const atualizado = await apiRequest(`/produtos/${product.id_produto}`);
            product.quantidade_estoque = atualizado.quantidade_estoque;
            adicionarProduto(product, desejada);
            message('Produto adicionado ao carrinho.', 'success');
            document.querySelector('#message').scrollIntoView({
                block: 'nearest'
            });
        } catch (error) {
            message(error.message);
        } finally {
            adicionando = false;
            atualizarEstoque();
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
    document.querySelector('#previous').disabled = true;
    document.querySelector('#next').disabled = true;
    try {
        const { products, hasNext } = await productPage({
            limite: limit,
            offset,
            busca: search.value.trim(),
            categoria: category,
            ordem: sort.value
        });
        if (version !== requestVersion) return;
        atualizarEstoques = [];
        grid.replaceChildren(...products.map(card));
        if (!products.length) grid.append(element('p', 'Nenhum produto encontrado. Experimente outra busca ou categoria.', 'empty'));
        document.querySelector('#product-count').textContent = `${products.length} produtos nesta seleção`;
        document.querySelector('#previous').disabled = offset === 0;
        document.querySelector('#next').disabled = !hasNext;
        document.querySelector('#page-number').textContent = `Página ${offset / limit + 1}`;
    } catch (error) {
        if (version !== requestVersion) return;
        atualizarEstoques = [];
        grid.replaceChildren(element('p', 'Não foi possível carregar o catálogo.', 'empty'));
        document.querySelector('#product-count').textContent = 'Catálogo indisponível';
        document.querySelector('#previous').disabled = offset === 0;
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
    document.querySelector('#previous').disabled = true;
    document.querySelector('#next').disabled = true;
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
// ============================================================
// MONTADOR DE SETUP
// ============================================================

const btnMontarSetup =
    document.getElementById("btnMontarSetup");

const montadorSetup =
    document.getElementById("montadorSetup");

const btnGerarSetup =
    document.getElementById("btnGerarSetup");

const resultadoSetup =
    document.getElementById("resultadoSetup");


if (btnMontarSetup && montadorSetup) {
    btnMontarSetup.addEventListener(
        "click",
        () => {
            montadorSetup.hidden = false;

            montadorSetup.scrollIntoView({
                behavior: "smooth",
                block: "center"
            });
        }
    );
}


if (btnGerarSetup && resultadoSetup) {

    btnGerarSetup.addEventListener(
        "click",
        async () => {

            const uso =
                document.getElementById(
                    "setupUso"
                ).value;

            const orcamento =
                Number(
                    document.getElementById(
                        "setupOrcamento"
                    ).value
                );

            const prioridade =
                document.getElementById(
                    "setupPrioridade"
                ).value;


            if (!orcamento || orcamento <= 0) {
                resultadoSetup.innerHTML = `
                    <p class="message error">
                        Informe um orçamento válido.
                    </p>
                `;

                return;
            }


            resultadoSetup.innerHTML = `
                <p class="muted">
                    Procurando produtos para seu setup...
                </p>
            `;


            try {

                const response = await fetch(
                    "https://dessik-back-end.vercel.app/api/setup/recomendar",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            uso,
                            orcamento,
                            prioridade
                        })
                    }
                );


                const data =
                    await response.json();


                if (!response.ok) {
                    throw new Error(
                        data.detail
                        || data.mensagem
                        || "Não foi possível montar o setup."
                    );
                }


                renderizarSetup(data);

            } catch (erro) {

                resultadoSetup.innerHTML = `
                    <p class="message error">
                        ${erro.message}
                    </p>
                `;
            }
        }
    );
}


function renderizarSetup(setup) {

    if (
        !setup.produtos
        || setup.produtos.length === 0
    ) {
        resultadoSetup.innerHTML = `
            <p>
                Nenhum setup encontrado
                dentro desse orçamento.
            </p>
        `;

        return;
    }


    const produtosHTML =
        setup.produtos
            .map(
                (produto) => `
                    <article class="setup-product">

                        ${
                            produto.imagem_url
                                ? `
                                    <img
                                        src="${produto.imagem_url}"
                                        alt="${produto.nome}"
                                    >
                                `
                                : ""
                        }

                        <div>
                            <span class="muted">
                                ${produto.categoria}
                            </span>

                            <h3>
                                ${produto.nome}
                            </h3>

                            <strong>
                                ${formatarPreco(
                                    produto.preco
                                )}
                            </strong>
                        </div>

                    </article>
                `
            )
            .join("");


    resultadoSetup.innerHTML = `

        <div class="setup-result">

            <h3>
                Seu setup recomendado
            </h3>

            <div class="setup-products">
                ${produtosHTML}
            </div>

            <div class="setup-summary">

                <p>
                    Orçamento:
                    <strong>
                        ${formatarPreco(
                            setup.orcamento
                        )}
                    </strong>
                </p>

                <p>
                    Total:
                    <strong>
                        ${formatarPreco(
                            setup.total
                        )}
                    </strong>
                </p>

                <p>
                    Restante:
                    <strong>
                        ${formatarPreco(
                            setup.restante
                        )}
                    </strong>
                </p>

            </div>

            <button
                class="button"
                id="btnAdicionarSetup"
            >
                Adicionar setup ao carrinho
            </button>

        </div>
    `;


    const btnAdicionar =
        document.getElementById(
            "btnAdicionarSetup"
        );


    if (btnAdicionar) {

        btnAdicionar.addEventListener(
            "click",
            () => {

                adicionarSetupAoCarrinho(
                    setup.produtos
                );
            }
        );
    }
}


function formatarPreco(valor) {

    return Number(valor).toLocaleString(
        "pt-BR",
        {
            style: "currency",
            currency: "BRL"
        }
    );
}


function adicionarSetupAoCarrinho(produtos) {

    /*
     * Aqui precisamos usar a função que
     * seu loja.js já utiliza atualmente
     * para adicionar produtos ao carrinho.
     */

    console.log(
        "Produtos escolhidos:",
        produtos
    );

    alert(
        "Setup montado! Agora falta ligar esta função ao carrinho atual."
    );
}
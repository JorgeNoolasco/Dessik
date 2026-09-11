// ============================================================
// LOJA DESSIK
// Catálogo + busca + carrinho + montador de setup.
// ============================================================

import {
    adicionarProduto,
    estoqueDisponivel,
    lerCarrinho
} from "./carrinho.js";

import {
    siteUrl,
    apiRequest,
    productPage,
    message,
    money,
    element,
    setupSession
} from "./api.js";


setupSession();


const grid =
    document.querySelector("#products");

let offset = 0;

const limit =
    document.body.classList.contains("home-page")
        ? 4
        : 12;

let category = "";

let requestVersion = 0;

let atualizarEstoques = [];


window.addEventListener(
    "dessik:carrinho-atualizado",
    () => {
        atualizarEstoques.forEach(
            atualizar => atualizar()
        );
    }
);


window.addEventListener(
    "pageshow",
    event => {
        if (event.persisted) {
            loadProducts(false);
        }
    }
);


const search =
    document.querySelector("#search");

const sort =
    document.querySelector("#sort");


const productArt = new Map([
    ["Notebook Horizon 14", "notebook"],
    ["Mouse Pulse", "mouse"],
    ["Teclado mecânico Type", "teclado"],
    ["Monitor View 24", "monitor"],
    ["Headset Wave", "headset"],
    ["Webcam Focus", "webcam"],
    ["SSD Sprint 1 TB", "ssd"],
    ["Memória RAM Flux 16 GB", "ram"],
]);


function card(product) {

    const article =
        element(
            "article",
            undefined,
            "card"
        );

    const visual =
        element(
            "div",
            undefined,
            "product-visual"
        );

    const image =
        element("img");


    image.src =
        /^\/?imagens\//.test(
            product.imagem_url
        )
            ? siteUrl(
                product.imagem_url.replace(
                    /^\//,
                    ""
                )
            )
            : product.imagem_url
                || siteUrl(
                    "imagens/placeholder.svg"
                );


    image.alt = product.nome;

    image.loading = "lazy";


    image.addEventListener(
        "error",
        () => {
            image.src =
                siteUrl(
                    "imagens/placeholder.svg"
                );
        },
        {
            once: true
        }
    );


    const art =
        productArt.get(
            product.nome
        );


    if (
        art
        && [
            "/imagens/placeholder.svg",
            "/imagens/catalogo-dessik.png"
        ].includes(
            product.imagem_url
        )
    ) {

        const sprite =
            element(
                "div",
                undefined,
                `product-art art-${art}`
            );

        sprite.setAttribute(
            "role",
            "img"
        );

        sprite.setAttribute(
            "aria-label",
            `Ilustração de ${product.nome}`
        );

        visual.append(
            sprite
        );

    } else {

        visual.append(
            image
        );
    }


    visual.append(
        element(
            "span",
            product.quantidade_estoque
                ? "DESSIK / ESSENTIALS"
                : "ESGOTADO",
            "product-tag"
        )
    );


    const body =
        element(
            "div",
            undefined,
            "card-body"
        );


    body.append(
        element(
            "p",
            product.categoria,
            "category"
        ),

        element(
            "h3",
            product.nome
        ),

        element(
            "p",
            product.descricao,
            "description"
        ),

        element(
            "p",
            money(product.preco),
            "price"
        ),

        element(
            "p",
            product.quantidade_estoque
                ? (
                    product.quantidade_estoque <= 3
                        ? `Últimas ${product.quantidade_estoque} unidades`
                        : `Estoque: ${product.quantidade_estoque} unidades`
                )
                : "Produto indisponível",
            product.quantidade_estoque
                ? "stock"
                : "stock out"
        )
    );


    const row =
        element(
            "div",
            undefined,
            "buy-row"
        );


    const quantity =
        element("input");

    quantity.type = "number";

    quantity.min = "1";

    quantity.max =
        String(
            Math.min(
                product.quantidade_estoque,
                1000
            )
        );

    quantity.value = "1";

    quantity.setAttribute(
        "aria-label",
        `Quantidade de ${product.nome}`
    );

    quantity.disabled =
        product.quantidade_estoque === 0;


    const button =
        element(
            "button",
            product.quantidade_estoque
                ? "Comprar ↗"
                : "Indisponível"
        );


    button.disabled =
        product.quantidade_estoque === 0;


    let adicionando = false;


    function atualizarEstoque() {

        const disponivel =
            estoqueDisponivel(
                product
            );

        const noCarrinho =
            lerCarrinho().find(
                item =>
                    item.id_produto
                    === product.id_produto
            )?.quantidade || 0;


        const stock =
            body.querySelector(
                ".stock"
            );


        stock.textContent =
            `Disponível para adicionar: ${disponivel} unidades`
            + (
                noCarrinho
                    ? ` · No carrinho: ${noCarrinho}`
                    : ""
            );


        stock.className =
            disponivel
                ? "stock"
                : "stock out";


        quantity.max =
            String(
                Math.max(
                    0,
                    Math.min(
                        disponivel,
                        1000 - noCarrinho
                    )
                )
            );


        quantity.disabled =
            adicionando
            || Number(
                quantity.max
            ) === 0;


        if (
            Number(quantity.value)
            > Number(quantity.max)
            || Number(quantity.value) < 1
        ) {
            quantity.value =
                Number(quantity.max)
                    ? "1"
                    : "0";
        }


        button.disabled =
            quantity.disabled;


        button.textContent =
            adicionando
                ? "Adicionando..."
                : Number(
                    quantity.max
                )
                    ? "Comprar ↗"
                    : noCarrinho
                        ? "Limite no carrinho"
                        : "Indisponível";


        visual
            .querySelector(
                ".product-tag"
            )
            .textContent =
                disponivel
                    ? "DESSIK / ESSENTIALS"
                    : noCarrinho
                        ? "NO CARRINHO"
                        : "ESGOTADO";
    }


    atualizarEstoques.push(
        atualizarEstoque
    );


    atualizarEstoque();


    button.addEventListener(
        "click",
        async () => {

            if (
                adicionando
                || !quantity.reportValidity()
            ) {
                return;
            }


            const desejada =
                Number(
                    quantity.value
                );


            adicionando = true;

            atualizarEstoque();


            try {

                const atualizado =
                    await apiRequest(
                        `/produtos/${product.id_produto}`
                    );


                product.quantidade_estoque =
                    atualizado.quantidade_estoque;


                adicionarProduto(
                    product,
                    desejada
                );


                message(
                    "Produto adicionado ao carrinho.",
                    "success"
                );


                document
                    .querySelector(
                        "#message"
                    )
                    ?.scrollIntoView({
                        block: "nearest"
                    });


            } catch (error) {

                message(
                    error.message
                );

            } finally {

                adicionando = false;

                atualizarEstoque();
            }
        }
    );


    row.append(
        quantity,
        button
    );


    body.append(
        row
    );


    article.append(
        visual,
        body
    );


    return article;
}


// ============================================================
// CARREGAR PRODUTOS
// ============================================================

async function loadProducts(
    clear = true
) {

    const version =
        ++requestVersion;


    if (clear) {
        message();
    }


    grid?.setAttribute(
        "aria-busy",
        "true"
    );


    document.querySelector(
        "#previous"
    ).disabled = true;


    document.querySelector(
        "#next"
    ).disabled = true;


    try {

        const {
            products,
            hasNext
        } = await productPage({

            limite: limit,

            offset,

            busca:
                search.value.trim(),

            categoria:
                category,

            ordem:
                sort.value
        });


        if (
            version
            !== requestVersion
        ) {
            return;
        }


        atualizarEstoques = [];


        grid.replaceChildren(
            ...products.map(
                card
            )
        );


        if (!products.length) {

            grid.append(
                element(
                    "p",
                    "Nenhum produto encontrado. Experimente outra busca ou categoria.",
                    "empty"
                )
            );
        }


        document.querySelector(
            "#product-count"
        ).textContent =
            `${products.length} produtos nesta seleção`;


        document.querySelector(
            "#previous"
        ).disabled =
            offset === 0;


        document.querySelector(
            "#next"
        ).disabled =
            !hasNext;


        document.querySelector(
            "#page-number"
        ).textContent =
            `Página ${offset / limit + 1}`;


    } catch (error) {

        if (
            version
            !== requestVersion
        ) {
            return;
        }


        atualizarEstoques = [];


        grid.replaceChildren(
            element(
                "p",
                "Não foi possível carregar o catálogo.",
                "empty"
            )
        );


        document.querySelector(
            "#product-count"
        ).textContent =
            "Catálogo indisponível";


        document.querySelector(
            "#previous"
        ).disabled =
            offset === 0;


        message(
            error.message
        );


    } finally {

        if (
            version
            === requestVersion
        ) {
            grid.setAttribute(
                "aria-busy",
                "false"
            );
        }
    }
}


// ============================================================
// BUSCA E PAGINAÇÃO
// ============================================================

let searchTimer;


search.addEventListener(
    "input",
    () => {

        clearTimeout(
            searchTimer
        );


        requestVersion++;


        document.querySelector(
            "#previous"
        ).disabled = true;


        document.querySelector(
            "#next"
        ).disabled = true;


        searchTimer =
            setTimeout(
                () => {

                    offset = 0;

                    loadProducts();

                },
                250
            );
    }
);


sort.addEventListener(
    "change",
    () => {

        offset = 0;

        loadProducts();
    }
);


document
    .querySelectorAll(
        "[data-category]"
    )
    .forEach(
        button => {

            button.addEventListener(
                "click",
                () => {

                    category =
                        button.dataset.category;


                    document
                        .querySelectorAll(
                            "[data-category]"
                        )
                        .forEach(
                            item => {

                                item.setAttribute(
                                    "aria-pressed",
                                    String(
                                        item === button
                                    )
                                );
                            }
                        );


                    offset = 0;

                    loadProducts();
                }
            );
        }
    );


document.querySelector(
    "#previous"
).onclick = () => {

    offset =
        Math.max(
            0,
            offset - limit
        );

    loadProducts();
};


document.querySelector(
    "#next"
).onclick = () => {

    offset += limit;

    loadProducts();
};


document.querySelector(
    "#reload"
).onclick = () => {

    offset = 0;

    loadProducts();
};


// ============================================================
// MONTADOR DE SETUP
// ============================================================

const btnMontarSetup =
    document.querySelector(
        "#btnMontarSetup"
    );


const montadorSetup =
    document.querySelector(
        "#montadorSetup"
    );


const btnGerarSetup =
    document.querySelector(
        "#btnGerarSetup"
    );


const resultadoSetup =
    document.querySelector(
        "#resultadoSetup"
    );


if (
    btnMontarSetup
    && montadorSetup
) {

    btnMontarSetup.addEventListener(
        "click",
        () => {

            montadorSetup.hidden =
                !montadorSetup.hidden;


            if (
                !montadorSetup.hidden
            ) {
                montadorSetup.scrollIntoView({
                    behavior: "smooth",
                    block: "center"
                });
            }
        }
    );
}


if (
    btnGerarSetup
    && resultadoSetup
) {

    btnGerarSetup.addEventListener(
        "click",
        async () => {

            const uso =
                document.querySelector(
                    "#setupUso"
                ).value;


            const orcamento =
                Number(
                    document.querySelector(
                        "#setupOrcamento"
                    ).value
                );


            const prioridade =
                document.querySelector(
                    "#setupPrioridade"
                ).value;


            if (
                !Number.isFinite(
                    orcamento
                )
                || orcamento <= 0
            ) {

                resultadoSetup.replaceChildren(
                    element(
                        "p",
                        "Informe um orçamento válido.",
                        "message error"
                    )
                );

                return;
            }


            btnGerarSetup.disabled =
                true;


            btnGerarSetup.textContent =
                "Montando...";


            resultadoSetup.replaceChildren(
                element(
                    "p",
                    "Procurando os melhores produtos...",
                    "muted"
                )
            );


            try {

                const setup =
                    await apiRequest(
                        "/setup/recomendar",
                        {
                            method:
                                "POST",

                            body: {
                                uso,
                                orcamento,
                                prioridade
                            }
                        }
                    );


                renderizarSetup(
                    setup
                );


            } catch (error) {

                resultadoSetup.replaceChildren(
                    element(
                        "p",
                        error.message,
                        "message error"
                    )
                );


            } finally {

                btnGerarSetup.disabled =
                    false;

                btnGerarSetup.textContent =
                    "Encontrar Setup";
            }
        }
    );
}


function renderizarSetup(
    setup
) {

    resultadoSetup.replaceChildren();


    const titulo =
        element(
            "h3",
            "Seu setup recomendado"
        );


    const resumo =
        element(
            "p",
            `Total: ${money(setup.total)} · Restante: ${money(setup.restante)}`,
            "setup-total"
        );


    const lista =
        element(
            "div",
            undefined,
            "setup-products"
        );


    for (
        const produto
        of setup.produtos
    ) {

        const item =
            element(
                "article",
                undefined,
                "setup-product"
            );


        const imagem =
            element("img");


        imagem.src =
            produto.imagem_url
                || siteUrl(
                    "imagens/placeholder.svg"
                );


        imagem.alt =
            produto.nome;


        imagem.addEventListener(
            "error",
            () => {

                imagem.src =
                    siteUrl(
                        "imagens/placeholder.svg"
                    );
            },
            {
                once: true
            }
        );


        const info =
            element(
                "div"
            );


        info.append(
            element(
                "span",
                produto.categoria,
                "category"
            ),

            element(
                "h4",
                produto.nome
            ),

            element(
                "strong",
                money(
                    produto.preco
                )
            )
        );


        item.append(
            imagem,
            info
        );


        lista.append(
            item
        );
    }


    const adicionar =
        element(
            "button",
            "Adicionar setup ao carrinho",
            "button"
        );


    adicionar.addEventListener(
        "click",
        async () => {

            adicionar.disabled =
                true;


            adicionar.textContent =
                "Adicionando...";


            try {

                // Primeiro confirma o estoque de todos.
                const atualizados = [];


                for (
                    const produto
                    of setup.produtos
                ) {

                    const atualizado =
                        await apiRequest(
                            `/produtos/${produto.id_produto}`
                        );


                    if (
                        estoqueDisponivel(
                            atualizado
                        ) < 1
                    ) {
                        throw new Error(
                            `${atualizado.nome} não possui estoque disponível.`
                        );
                    }


                    atualizados.push(
                        atualizado
                    );
                }


                // Depois adiciona cada item.
                for (
                    const produto
                    of atualizados
                ) {

                    adicionarProduto(
                        produto,
                        1
                    );
                }


                message(
                    "Setup adicionado ao carrinho!",
                    "success"
                );


                adicionar.textContent =
                    "Setup adicionado ✓";


            } catch (error) {

                message(
                    error.message
                );


                adicionar.disabled =
                    false;


                adicionar.textContent =
                    "Adicionar setup ao carrinho";
            }
        }
    );


    resultadoSetup.append(
        titulo,
        resumo,
        lista,
        adicionar
    );
}


loadProducts();
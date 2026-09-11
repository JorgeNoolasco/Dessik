// Administração da Dessik.
//
// Este arquivo controla:
// - sessão do administrador;
// - cadastro de produtos;
// - edição de produtos;
// - exclusão;
// - movimentação de estoque;
// - paginação;
// - Security Center;
// - logs de segurança.

import {
    apiRequest,
    productPage,
    message,
    money,
    element,
    setupSession,
    confirmAction
} from "./api.js";


// Formulário principal de produtos.
const form = document.querySelector(
    "#product-form"
);

// Corpo da tabela de produtos.
const table = document.querySelector(
    "#product-rows"
);

// Produto atualmente sendo editado.
let editing = null;

// Controle da paginação.
let offset = 0;

// Quantidade de produtos por página.
const limit = 20;

// Evita duas consultas simultâneas.
let loading = false;

// Formulário de movimentação de estoque.
const stockForm = document.querySelector(
    "#stock-form"
);

// Produto selecionado para movimentação.
let stockProduct = null;


// Limpa o formulário de produtos
// e encerra o modo de edição.
function resetForm() {

    form.reset();

    editing = null;

    document.querySelector(
        "#form-title"
    ).textContent = "Novo produto";

    document.querySelector(
        "#save-product"
    ).textContent = "Cadastrar produto";
}


// Busca os produtos no Back-End.
async function loadProducts() {

    // Evita carregar duas vezes ao mesmo tempo.
    if (loading) {
        return;
    }

    loading = true;

    const previousButton =
        document.querySelector("#previous");

    const nextButton =
        document.querySelector("#next");


    // Desativa temporariamente os botões.
    previousButton.disabled = true;
    nextButton.disabled = true;


    try {

        // Busca uma página de produtos.
        let page = await productPage({
            limite: limit,
            offset
        });


        // Se a página atual ficou vazia,
        // volta uma página automaticamente.
        if (
            !page.products.length
            && offset > 0
        ) {

            offset = Math.max(
                0,
                offset - limit
            );

            page = await productPage({
                limite: limit,
                offset
            });
        }


        const {
            products,
            hasNext
        } = page;


        // Limpa a tabela antes
        // de adicionar os novos dados.
        table.replaceChildren();


        // Cria uma linha para cada produto.
        for (const product of products) {

            const row = element(
                "tr"
            );


            // Produto.
            row.append(
                element(
                    "td",
                    `#${product.id_produto} ${product.nome}`
                ),

                // Preço.
                element(
                    "td",
                    money(
                        product.preco
                    )
                ),

                // Estoque.
                element(
                    "td",
                    String(
                        product.quantidade_estoque
                    )
                )
            );


            // Coluna de ações.
            const actions = element(
                "td"
            );


            // Botão editar.
            const edit = element(
                "button",
                "Editar",
                "secondary"
            );


            edit.setAttribute(
                "aria-label",
                `Editar ${product.nome}`
            );


            edit.onclick = () => {

                // Guarda o ID em edição.
                editing =
                    product.id_produto;


                // Preenche os campos
                // com os dados atuais.
                for (const key of [
                    "nome",
                    "descricao",
                    "categoria",
                    "preco",
                    "quantidade_estoque",
                    "imagem_url"
                ]) {

                    if (form.elements[key]) {
                        form.elements[key].value =
                            product[key] ?? "";
                    }
                }


                document.querySelector(
                    "#form-title"
                ).textContent =
                    `Editar produto #${editing}`;


                document.querySelector(
                    "#save-product"
                ).textContent =
                    "Salvar alterações";


                form.elements.nome.focus();
            };


            // Botão excluir.
            const remove = element(
                "button",
                "Excluir",
                "danger"
            );


            remove.setAttribute(
                "aria-label",
                `Excluir ${product.nome}`
            );


            remove.onclick = async () => {

                // Exibe confirmação antes
                // de remover o produto.
                const confirmed =
                    await confirmAction(
                        "Excluir produto?",
                        `O produto ${product.nome} será removido do catálogo.`,
                        "Excluir"
                    );


                if (!confirmed) {
                    return;
                }


                remove.disabled = true;


                try {

                    await apiRequest(
                        `/produtos/${product.id_produto}`,
                        {
                            method: "DELETE",
                            auth: true
                        }
                    );


                    // Se estava editando o mesmo produto,
                    // limpa o formulário.
                    if (
                        editing
                        === product.id_produto
                    ) {

                        resetForm();
                    }


                    message(
                        "Produto excluído.",
                        "success"
                    );


                    // Atualiza a tabela.
                    await loadProducts();

                    // Atualiza também os logs,
                    // pois a exclusão gera evento.
                    await carregarLogsSeguranca();


                } catch (error) {

                    message(
                        error.message
                    );

                } finally {

                    remove.disabled = false;
                }
            };


            // Botão de estoque.
            const stock = element(
                "button",
                "Estoque",
                "secondary"
            );


            stock.onclick = () => {

                stockProduct =
                    product.id_produto;

                stockForm.reset();

                stockForm.hidden = false;


                document.querySelector(
                    "#stock-product"
                ).textContent =
                    `Estoque: ${product.nome} · Saldo consultado: ${product.quantidade_estoque}`;


                stockForm
                    .elements
                    .quantidade
                    .focus();
            };


            actions.append(
                edit,
                stock,
                remove
            );


            row.append(
                actions
            );


            table.append(
                row
            );
        }


        // Caso não exista produto na página.
        if (!products.length) {

            const row = element(
                "tr"
            );

            const cell = element(
                "td",
                "Nenhum produto nesta página."
            );

            cell.colSpan = 4;

            row.append(
                cell
            );

            table.append(
                row
            );
        }


        // Atualiza paginação.
        previousButton.disabled =
            offset === 0;

        nextButton.disabled =
            !hasNext;


        document.querySelector(
            "#page-number"
        ).textContent =
            `Página ${offset / limit + 1}`;


    } finally {

        loading = false;

        previousButton.disabled =
            offset === 0;
    }
}


// Atualiza a tabela de produtos
// e mostra eventuais erros.
async function refresh() {

    try {

        await loadProducts();

    } catch (error) {

        message(
            error.message
        );
    }
}


// Cadastro ou edição de produto.
form.addEventListener(
    "submit",
    async event => {

        event.preventDefault();


        const button =
            document.querySelector(
                "#save-product"
            );


        if (
            button.disabled
            || !form.reportValidity()
        ) {

            return;
        }


        button.disabled = true;


        try {

            // Converte formulário
            // para um objeto JavaScript.
            const body =
                Object.fromEntries(
                    new FormData(form)
                );


            // O Back-End utiliza "quantidade".
            body.quantidade =
                Number(
                    body.quantidade_estoque
                );


            delete body.quantidade_estoque;


            const data =
                await apiRequest(
                    editing
                        ? `/produtos/${editing}`
                        : "/produtos",
                    {
                        method:
                            editing
                                ? "PUT"
                                : "POST",

                        auth: true,

                        body
                    }
                );


            resetForm();


            message(
                data.mensagem
                || "Produto salvo com sucesso.",
                "success"
            );


            // Atualiza produtos.
            await refresh();

            // Atualiza Security Center.
            await carregarLogsSeguranca();


        } catch (error) {

            message(
                error.message
            );

        } finally {

            button.disabled = false;
        }
    }
);


// Movimentação de estoque.
stockForm.addEventListener(
    "submit",
    async event => {

        event.preventDefault();


        const button =
            stockForm.querySelector(
                '[type="submit"]'
            );


        if (
            button.disabled
            || !stockProduct
            || !stockForm.reportValidity()
        ) {

            return;
        }


        const productId =
            stockProduct;


        const operation =
            stockForm
                .elements
                .operacao
                .value;


        const quantidade =
            Number(
                stockForm
                    .elements
                    .quantidade
                    .value
            );


        // Garante que somente
        // operações conhecidas sejam usadas.
        if (
            ![
                "entrada",
                "saida",
                "ajuste"
            ].includes(operation)
        ) {

            return;
        }


        // Entrada e saída precisam
        // ser maiores que zero.
        //
        // Ajuste pode ser zero.
        if (
            !Number.isInteger(quantidade)

            || quantidade < (
                operation === "ajuste"
                    ? 0
                    : 1
            )
        ) {

            message(
                "Informe uma quantidade inteira válida. Entrada e saída devem ser maiores que zero."
            );

            return;
        }


        button.disabled = true;


        try {

            const data =
                await apiRequest(

                    `/produtos/${productId}${
                        operation === "ajuste"
                            ? ""
                            : `/${operation}`
                    }`,

                    {
                        method:
                            operation === "ajuste"
                                ? "PUT"
                                : "POST",

                        auth: true,

                        body: {
                            quantidade
                        }
                    }
                );


            stockForm.hidden = true;

            stockProduct = null;


            // Se o produto também estiver
            // aberto para edição,
            // atualiza o campo do formulário.
            if (
                editing === productId
                && form.elements.quantidade_estoque
            ) {

                form.elements
                    .quantidade_estoque
                    .value =
                        data.quantidade_estoque;
            }


            message(
                `Estoque atualizado. Saldo confirmado: ${data.quantidade_estoque}.`,
                "success"
            );


            // Atualiza catálogo.
            await refresh();

            // Atualiza logs.
            await carregarLogsSeguranca();


        } catch (error) {

            message(
                error.message
            );

        } finally {

            button.disabled = false;
        }
    }
);


// Cancela movimentação de estoque.
document.querySelector(
    "#cancel-stock"
).onclick = () => {

    stockForm.hidden = true;

    stockProduct = null;
};


// Limpa formulário de produto.
document.querySelector(
    "#cancel-edit"
).onclick = resetForm;


// Volta uma página.
document.querySelector(
    "#previous"
).onclick = () => {

    offset = Math.max(
        0,
        offset - limit
    );

    refresh();
};


// Avança uma página.
document.querySelector(
    "#next"
).onclick = () => {

    offset += limit;

    refresh();
};


// Protege textos recebidos da API
// antes de inserir com innerHTML.
//
// Isso reduz risco de XSS
// caso algum texto inesperado
// seja armazenado no banco.
function escaparHtml(valor) {

    return String(
        valor ?? ""
    )

        .replaceAll(
            "&",
            "&amp;"
        )

        .replaceAll(
            "<",
            "&lt;"
        )

        .replaceAll(
            ">",
            "&gt;"
        )

        .replaceAll(
            '"',
            "&quot;"
        )

        .replaceAll(
            "'",
            "&#039;"
        );
}


// Escolhe a aparência do badge
// de acordo com o tipo do evento.
function obterClasseBadge(
    evento
) {

    const texto =
        String(
            evento || ""
        ).toUpperCase();


    // Eventos positivos.
    if (
        texto.includes("SUCESSO")
        || texto.includes("CRIADO")
    ) {

        return "success";
    }


    // Eventos relacionados
    // a falhas ou bloqueios.
    if (
        texto.includes("FALHOU")
        || texto.includes("NEGADO")
        || texto.includes("REMOVIDO")
    ) {

        return "danger";
    }


    // Alterações de estoque.
    if (
        texto.includes("ESTOQUE")
        || texto.includes("SAIDA")
        || texto.includes("AJUSTE")
    ) {

        return "warning";
    }


    // Qualquer outro evento.
    return "info";
}


// Atualiza os cards superiores
// do Security Center.
function atualizarResumoSeguranca(
    logs
) {

    // Total de eventos carregados.
    const total =
        logs.length;


    // Conta tentativas de login falhas.
    const loginFalhou =
        logs.filter(
            log =>
                log.evento
                === "LOGIN_FALHOU"
        ).length;


    // Conta logins válidos.
    const loginSucesso =
        logs.filter(
            log =>
                log.evento
                === "LOGIN_SUCESSO"
        ).length;


    // Conta alterações administrativas
    // de estoque.
    const estoque =
        logs.filter(
            log =>
                log.evento
                === "ALTERACAO_ESTOQUE"
        ).length;


    const totalElement =
        document.querySelector(
            "#security-total"
        );

    const falhouElement =
        document.querySelector(
            "#security-login-falhou"
        );

    const sucessoElement =
        document.querySelector(
            "#security-login-sucesso"
        );

    const estoqueElement =
        document.querySelector(
            "#security-estoque"
        );


    if (totalElement) {
        totalElement.textContent =
            String(total);
    }

    if (falhouElement) {
        falhouElement.textContent =
            String(loginFalhou);
    }

    if (sucessoElement) {
        sucessoElement.textContent =
            String(loginSucesso);
    }

    if (estoqueElement) {
        estoqueElement.textContent =
            String(estoque);
    }
}


// Monta visualmente os logs
// recebidos do Back-End.
function renderizarLogsSeguranca(
    logs
) {

    const container =
        document.querySelector(
            "#logsSeguranca"
        );


    if (!container) {
        return;
    }


    // Sem eventos.
    if (
        !Array.isArray(logs)
        || logs.length === 0
    ) {

        atualizarResumoSeguranca(
            []
        );


        container.innerHTML = `
            <div class="log-empty">
                Nenhum evento de segurança registrado.
            </div>
        `;


        return;
    }


    // Atualiza os cards.
    atualizarResumoSeguranca(
        logs
    );


    // Converte cada log
    // em um card visual.
    container.innerHTML =
        logs

            .map(
                log => {

                    const evento =
                        escaparHtml(
                            log.evento
                            || "EVENTO"
                        );


                    const descricao =
                        escaparHtml(
                            log.descricao
                            || "Sem descrição."
                        );


                    const usuario =
                        escaparHtml(
                            log.usuario_id
                            ?? "Não identificado"
                        );


                    const ip =
                        escaparHtml(
                            log.ip
                            || "Não informado"
                        );


                    const classe =
                        obterClasseBadge(
                            log.evento
                        );


                    // Formata data
                    // para padrão brasileiro.
                    const data =
                        log.data_evento

                            ? new Date(
                                log.data_evento
                            ).toLocaleString(
                                "pt-BR"
                            )

                            : "Data não informada";


                    return `
                        <article class="log-card">

                            <div class="log-top">

                                <div class="log-title-wrap">

                                    <span
                                        class="log-badge ${classe}"
                                    >
                                        ${evento}
                                    </span>

                                    <strong class="log-title">
                                        Evento #${escaparHtml(log.id)}
                                    </strong>

                                </div>


                                <span class="log-date">
                                    ${escaparHtml(data)}
                                </span>

                            </div>


                            <p class="log-description">
                                ${descricao}
                            </p>


                            <div class="log-meta">

                                <span>
                                    Usuário:
                                    ${usuario}
                                </span>

                                <span>
                                    IP:
                                    ${ip}
                                </span>

                            </div>

                        </article>
                    `;
                }
            )

            .join("");
}


// Consulta os logs no FastAPI.
async function carregarLogsSeguranca() {

    const container =
        document.querySelector(
            "#logsSeguranca"
        );


    // Caso a página não tenha
    // a área de segurança.
    if (!container) {
        return;
    }


    // Feedback enquanto carrega.
    container.innerHTML = `
        <div class="log-empty">
            Carregando logs de segurança...
        </div>
    `;


    try {

        // A rota exige autenticação
        // de administrador.
        const logs =
            await apiRequest(
                "/seguranca/logs",
                {
                    auth: true
                }
            );


        renderizarLogsSeguranca(
            logs
        );


    } catch (erro) {

        console.error(
            "Erro ao carregar logs:",
            erro
        );


        atualizarResumoSeguranca(
            []
        );


        container.innerHTML = `
            <div class="log-empty">
                Não foi possível carregar
                os logs de segurança.
            </div>
        `;
    }
}


// Botão Atualizar logs.
const btnAtualizarLogs =
    document.querySelector(
        "#btnAtualizarLogs"
    );


if (btnAtualizarLogs) {

    btnAtualizarLogs.addEventListener(
        "click",
        async () => {

            // Bloqueia o botão
            // durante a consulta.
            btnAtualizarLogs.disabled = true;

            const textoOriginal =
                btnAtualizarLogs.textContent;


            btnAtualizarLogs.textContent =
                "Atualizando...";


            try {

                await carregarLogsSeguranca();

            } finally {

                btnAtualizarLogs.disabled = false;

                btnAtualizarLogs.textContent =
                    textoOriginal;
            }
        }
    );
}


// Verifica a sessão.
//
// true, true significa que esta página
// exige usuário autenticado e administrador.
const user =
    await setupSession(
        true,
        true
    );


// Somente continua se
// o usuário for válido.
if (user) {

    // Exibe o conteúdo administrativo.
    const adminContent =
        document.querySelector(
            "#admin-content"
        );


    if (adminContent) {
        adminContent.hidden = false;
    }


    // Carrega os produtos.
    await refresh();


    // Carrega o Security Center.
    await carregarLogsSeguranca();
}
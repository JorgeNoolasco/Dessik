// Utilitários: requisições HTTP, navegação, sessão e criação segura de elementos.
export const API_URL = "https://dessik-back-end.vercel.app";

// Aceita caminhos da API com ou sem prefixo; nunca envia JWT para outra origem.
export function apiUrl(path) {
    if (typeof path !== 'string' || !/^\/(?!\/)/.test(path) || /[\\#]/.test(path)) {
        throw new Error('Caminho de API inválido.');
    }
    const normalized = path === '/' ? '/' : `/api/${path.replace(/^(?:\/api)+(?=\/|\?|$)/, '').replace(/^\//, '')}`;
    const url = new URL(normalized, API_URL);
    if (url.origin !== API_URL || (path !== '/' && !url.pathname.startsWith('/api/'))) {
        throw new Error('Caminho de API inválido.');
    }
    return url.href;
}
// Resolve caminhos pela localização deste módulo, preservando subpastas de publicação.
export function siteUrl(relativePath) {
    return new URL(relativePath, new URL('../', import.meta.url)).href;
}

// Formata números como reais apenas para apresentação.
export const money = value => Number(value).toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL'
});

// Envia JSON e o token quando necessário. Converte falhas de rede e respostas HTTP em erros legíveis.
export async function apiRequest(path, {
    method = 'GET',
    body,
    auth = false,
    token = sessionStorage.getItem('dessik_token'),
    timeoutMs = 15000
} = {}) {
    const url = apiUrl(path);
    const headers = { Accept: 'application/json' };
    if (body !== undefined) headers['Content-Type'] = 'application/json';
    if (auth) {
        if (!token) {
            const error = new Error('Entre na sua conta para continuar.');
            error.status = 401;
            throw error;
        }
        headers.Authorization = `Bearer ${token}`;
    }
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);
    try {
        const response = await fetch(url, {
            method,
            headers,
            cache: 'no-store',
            credentials: 'omit',
            redirect: 'error',
            signal: controller.signal,
            body: body === undefined ? undefined : JSON.stringify(body)
        });
        if (response.status === 204) return null;
        const data = await response.json().catch(() => null);
        if (!response.ok) {
        // Uma sessão expirada também esconde os dados e atalhos da conta aberta.
        if (response.status === 401 && auth) limparSessao();
        const errors = Array.isArray(data?.erros) ? data.erros : Array.isArray(data?.detail) ? data.detail : [];
        const detail = errors.filter(item => item && typeof item === 'object').map(item =>
            `${item.campo || item.loc?.filter(part => part !== 'body').join('.') || 'Dados'}: ${item.mensagem || item.msg || 'Valor inválido.'}`).join(' ');
        const defaults = {
            401: 'Sua sessão expirou. Entre novamente.',
            403: 'Você não tem permissão para esta operação.',
            404: 'O recurso solicitado não foi encontrado.',
            422: 'Confira os dados enviados.',
            500: 'A loja encontrou um erro interno. Tente novamente mais tarde.',
            502: 'A loja está temporariamente indisponível.',
            503: 'A loja está temporariamente indisponível.',
            504: 'O servidor demorou para responder. Tente novamente.'
        };
        const error = new Error(detail || (typeof data?.detail === 'string' && data.detail) ||
            (typeof data?.mensagem === 'string' && data.mensagem) || defaults[response.status] || `Erro HTTP ${response.status}. Tente novamente.`);
        error.status = response.status;
        throw error;
        }
        if (data === null) throw new Error('O servidor não retornou JSON válido. Tente novamente.');
        return data;
    } catch (error) {
        if (controller.signal.aborted) throw new Error('O servidor demorou para responder. Confira o resultado antes de repetir uma alteração.');
        if (error instanceof TypeError) throw new Error('Não foi possível conectar à loja. Verifique sua conexão ou tente novamente mais tarde.');
        throw error;
    } finally {
        clearTimeout(timer);
    }
}

// Um item extra indica se existe próxima página, sem exibir uma página vazia ao final.
export async function productPage({ limite, offset = 0, busca = '', categoria = '', ordem = 'recentes' }) {
    const query = new URLSearchParams({ limite: limite + 1, offset, busca, categoria, ordem });
    const products = await apiRequest(`/produtos?${query}`);
    if (!Array.isArray(products)) throw new Error('O servidor retornou um catálogo inválido.');
    return { products: products.slice(0, limite), hasNext: products.length > limite };
}

// Atualiza o texto e o estado visual da mensagem; sem texto, oculta a área.
export function message(text = '', kind = 'error', target = document.querySelector('#message')) {
    if (!target) return;
    target.textContent = text;
    target.className = `message ${kind}`;
    target.hidden = !text;
}

// Cria nós com textContent para que dados externos não sejam interpretados como HTML.
export function element(tag, text, className) {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = text; // Dados do banco nunca viram HTML executável.
    if (className) node.className = className;
    return node;
}

// Remove credenciais e dados visíveis ao sair ou receber uma rejeição do servidor.
export function limparSessao() {
    sessionStorage.removeItem('dessik_token');
    sessionStorage.removeItem('dessik_login_ok');
    document.querySelectorAll('[data-guest]').forEach(el => el.hidden = false);
    document.querySelectorAll('[data-session], [data-admin], [data-private], #admin-content, #orders-content, #profile-content').forEach(el => el.hidden = true);
    document.querySelectorAll('[data-user], [data-profile-field]').forEach(el => el.textContent = '');
}

// Confere o contrato público de /me; a autenticidade do token é validada pelo servidor.
export function validarUsuario(user) {
    if (!user || typeof user.nome !== 'string' || !user.nome.trim() ||
        typeof user.email !== 'string' || !user.email.includes('@')) {
        throw new Error('Não foi possível validar sua conta. Tente entrar novamente.');
    }
    return user;
}

// Consulta o usuário e atualiza o menu. Pode exigir login ou perfil; a API também deve validar permissões.
export async function setupSession(required = false, admin = false) {
    const token = sessionStorage.getItem('dessik_token');
    if (!token) {
        if (required) location.replace(siteUrl('html/login.html'));
        return null;
    }
    try {
        const user = validarUsuario(await apiRequest('/me', {
            auth: true
        }));
        document.querySelectorAll('[data-guest]').forEach(el => el.hidden = true);
        document.querySelectorAll('[data-session]').forEach(el => el.hidden = false);
        document.querySelectorAll('[data-admin]').forEach(el => el.hidden = !user.is_admin);
        document.querySelectorAll('[data-user]').forEach(el => el.textContent = user.nome.split(' ')[0]);
        document.querySelectorAll('[data-logout]').forEach(el => el.onclick = () => {
            limparSessao();
            location.assign(siteUrl('html/login.html'));
        });
        // Só anuncia sucesso depois de o servidor reconhecer a conta.
        if (sessionStorage.getItem('dessik_login_ok')) {
            sessionStorage.removeItem('dessik_login_ok');
            message('Login realizado com sucesso.', 'success');
        }
        if (admin && !user.is_admin) throw new Error('Esta área está disponível apenas para administradores.');
        return user;
    } catch (error) {
        if (error.status === 401) {
            sessionStorage.removeItem('dessik_token');
            if (required) location.replace(siteUrl('html/login.html'));
        }
        if (required) message(error.message);
        return null;
    }
}

// Espera o fechamento do diálogo e retorna se a ação foi confirmada.
export function confirmAction(title, description, action = 'Confirmar') {
    return new Promise(resolve => {
        const dialog = document.querySelector('#confirm-dialog');
        dialog.querySelector('h2').textContent = title;
        dialog.querySelector('p').textContent = description;
        dialog.querySelector('[value="confirm"]').textContent = action;
        dialog.returnValue = 'cancel';
        dialog.addEventListener('close', () => resolve(dialog.returnValue === 'confirm'), {
            once: true
        });
        dialog.showModal();
    });
}

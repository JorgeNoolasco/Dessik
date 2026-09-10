// Utilitários: requisições HTTP, navegação, sessão e criação segura de elementos.
export const API_URL = "https://dessik-back-end.vercel.app/api"; // Back-end separado; esta base já inclui /api.
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
    token = sessionStorage.getItem('dessik_token')
} = {}) {
    const headers = {};
    if (body !== undefined) headers['Content-Type'] = 'application/json';
    if (auth) {
        if (!token) throw new Error('Entre na sua conta para continuar.');
        headers.Authorization = `Bearer ${token}`;
    }
    let response;
    try {
        response = await fetch(`${API_URL}${path}`, {
            method,
            headers,
            cache: 'no-store',
            body: body === undefined ? undefined : JSON.stringify(body)
        });
    } catch {
        throw new Error('Sem conexão com a loja. Verifique sua internet e tente novamente.');
    }
    let data;
    // DELETE retorna 204 sem JSON; a exclusão já foi confirmada pelo servidor.
    if (response.status === 204) return null;
    try {
        data = await response.json();
    } catch {
        throw new Error('O servidor não respondeu corretamente. Tente novamente.');
    }
    if (!response.ok) {
        // Uma sessão expirada também esconde os dados e atalhos da conta aberta.
        if (response.status === 401 && auth) limparSessao();
        const detail = data.erros?.map(item => `${item.campo || 'Dados'}: ${item.mensagem}`).join(' ');
        const error = new Error(detail || data.mensagem || (typeof data.detail === 'string' ? data.detail : '') || 'Não foi possível concluir a operação.');
        error.status = response.status;
        throw error;
    }
    return data;
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
    document.querySelectorAll('[data-session], [data-admin], [data-private]').forEach(el => el.hidden = true);
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

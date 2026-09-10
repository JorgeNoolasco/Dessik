// Autenticação: envia credenciais e guarda o token apenas na sessão desta aba.
import {
    siteUrl,
    apiRequest,
    message,
    setupSession,
    limparSessao,
    validarUsuario
} from './api.js';
import { lerCarrinho } from './carrinho.js';
// Uma conta já autenticada segue diretamente para o perfil.
const sessaoInicial = setupSession();
sessaoInicial.then(user => {
    if (user) location.replace(siteUrl('html/perfil.html'));
});
if (new URLSearchParams(location.search).get('cadastro') === 'ok') {
    message('Conta criada com sucesso. Entre para começar.', 'success');
}
// Envia pela API sem recarregar a página; o botão é bloqueado durante o envio.
document.querySelector('#login-form').addEventListener('submit', async event => {
    event.preventDefault();
    const form = event.currentTarget;
    const button = form.querySelector('[type="submit"]');
    if (button.disabled) return;
    // Valida o formulário inclusive em envios disparados por JavaScript; preserva a senha literal.
    form.elements.email.value = form.elements.email.value.trim().toLowerCase();
    if (!form.reportValidity()) return;
    button.disabled = true;
    message();
    try {
        await sessaoInicial;
        limparSessao();
        const data = await apiRequest('/login', {
            method: 'POST',
            body: Object.fromEntries(new FormData(form))
        });
        // Uma resposta 200 sem token não representa login; confirma /me antes de salvar a sessão.
        if (typeof data?.access_token !== 'string' || !data.access_token.trim()) {
            throw new Error('O servidor não confirmou o login. Tente novamente.');
        }
        validarUsuario(await apiRequest('/me', { auth: true, token: data.access_token }));
        sessionStorage.setItem('dessik_token', data.access_token);
        sessionStorage.setItem('dessik_login_ok', '1');
        location.assign(lerCarrinho().length ? siteUrl('html/carrinho.html') : siteUrl('html/perfil.html'));
    } catch (error) {
        // Nenhuma credencial fica armazenada quando o login ou a validação falha.
        limparSessao();
        message(error.status === 401 ? 'E-mail ou senha incorretos.' : error.message);
    } finally {
        // Restaura os controles mesmo quando a operação falha.
        button.disabled = false;
    }
});

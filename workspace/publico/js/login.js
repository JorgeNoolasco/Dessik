import {
    apiRequest,
    message,
    setupSession
} from './api.js';
setupSession();
if (new URLSearchParams(location.search).get('cadastro') === 'ok') {
    message('Conta criada com sucesso. Entre para começar.', 'success');
}
document.querySelector('#login-form').addEventListener('submit', async event => {
    event.preventDefault();
    const form = event.currentTarget;
    const button = form.querySelector('[type="submit"]');
    button.disabled = true;
    message();
    try {
        const data = await apiRequest('/login', {
            method: 'POST',
            body: Object.fromEntries(new FormData(form))
        });
        sessionStorage.setItem('dessik_token', data.access_token);
        sessionStorage.setItem('dessik_login_ok', '1');
        location.assign(sessionStorage.getItem('dessik_carrinho') ? '/carrinho.html' : '/loja.html');
    } catch (error) {
        message(error.message);
    } finally {
        button.disabled = false;
    }
});

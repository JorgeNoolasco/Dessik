// Perfil: exige uma conta reconhecida pelo servidor antes de exibir seus dados.
import { setupSession, message } from './api.js';

async function carregarPerfil() {
    const content = document.querySelector('#profile-content');
    content.hidden = true;
    const user = await setupSession(true);
    if (!user) return;
    // textContent apresenta os dados como texto, sem executar HTML recebido da API.
    document.querySelector('#profile-name').textContent = user.nome;
    document.querySelector('#profile-email').textContent = user.email;
    content.hidden = false;
}

// Ao voltar pelo histórico, reconfirma a sessão em vez de reapresentar dados antigos.
window.addEventListener('pageshow', event => {
    if (event.persisted) carregarPerfil().catch(error => message(error.message));
});
carregarPerfil().catch(error => message(error.message));

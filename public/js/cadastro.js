import {apiRequest, message, setupSession} from './api.js';
setupSession();
const form = document.querySelector('#register-form');
const cepMessage = document.querySelector('#cep-message');
const senha = form.elements.senha;
const confirmation = form.elements.confirmar_senha;
function validatePasswords() {
  confirmation.setCustomValidity(confirmation.value && confirmation.value !== senha.value ? 'As senhas não coincidem.' : '');
  senha.setCustomValidity(new TextEncoder().encode(senha.value).length > 72 ? 'Use no máximo 72 bytes na senha.' : '');
}
senha.addEventListener('input', validatePasswords);
confirmation.addEventListener('input', validatePasswords);
document.querySelector('#generate-password').addEventListener('click', async event => {
  const button = event.currentTarget;
  button.disabled = true;
  try {
    const data = await apiRequest('/gerar-senha');
    senha.value = confirmation.value = data.senha;
    senha.type = 'text';
    validatePasswords();
    message('Senha sugerida preenchida. Guarde-a antes de cadastrar.', 'success');
  } catch (error) { message(error.message); }
  finally { button.disabled = false; }
});
document.querySelector('#lookup-cep').addEventListener('click', async event => {
  const value = form.elements.cep.value.replace(/\D/g, '');
  if (value.length !== 8) return message('Informe os 8 números do CEP.', 'error', cepMessage);
  const button = event.currentTarget;
  button.disabled = true;
  message('Consultando CEP…', '', cepMessage);
  try {
    const address = await apiRequest(`/cep/${value}`);
    // Não substitui um endereço caso o usuário tenha alterado o CEP durante a consulta.
    if (form.elements.cep.value.replace(/\D/g, '') !== value) return;
    for (const key of ['logradouro', 'bairro', 'cidade', 'estado']) form.elements[key].value = address[key];
    message('Endereço encontrado. Confira os dados abaixo.', 'success', cepMessage);
  } catch (error) { message(error.message, 'error', cepMessage); }
  finally { button.disabled = false; }
});
form.addEventListener('submit', async event => {
  event.preventDefault();
  validatePasswords();
  if (!form.reportValidity()) return;
  const button = form.querySelector('[type="submit"]');
  button.disabled = true;
  message();
  try {
    const body = Object.fromEntries(new FormData(form));
    body.cep = body.cep.replace(/\D/g, '');
    await apiRequest('/cadastro', {method: 'POST', body});
    location.assign('/login.html?cadastro=ok');
  } catch (error) { message(error.message); }
  finally { button.disabled = false; }
});

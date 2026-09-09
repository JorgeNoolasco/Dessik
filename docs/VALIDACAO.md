# Validação da entrega

Executada em 08/09/2026, em Windows, com Python 3.13.14.

## Resultado

- **39 testes passaram**, incluindo integração com MariaDB 11.4.11 (protocolo MySQL, tabelas InnoDB), sem substituir o banco por SQLite.
- A instância de teste ficou isolada na porta local 33316, com credencial aleatória e dados próprios. Foi encerrada após a validação. Não foi usado nem alterado um banco remoto do usuário.
- Cadastro e e-mail duplicado; login válido/inválido; senha com hash e salt; JWT assinado e expirado; campos inválidos e ausência de vazamento de senha nos erros.
- Permissão de administrador, criação, leitura, atualização e exclusão de produtos; SQL injection tratado como texto.
- Pedido com total correto, redução de estoque, recusa de pedido multitem com estoque insuficiente e preservação do histórico por chave estrangeira.
- Duas compras concorrentes da última unidade: **uma resposta 201, uma 409 e estoque final zero**.
- Rotas e arquivos estáticos acessíveis por TestClient, links locais existentes e IDs HTML sem duplicação.
- Falhas de banco retornando 503; ViaCEP simulado com sucesso, CEP inexistente, resposta inválida, erro HTTP e timeout.
- Consulta real ao ViaCEP para `01001000`: HTTP 200, cidade São Paulo, UF SP.
- Os cinco módulos JavaScript passaram na análise sintática com tree-sitter-javascript.
- `python -m compileall -q api backend scripts tests`: aprovado.
- `python -m pip check`: nenhuma dependência incompatível.

## Limites da verificação

Não houve deploy real na Vercel, conexão com banco remoto do usuário ou teste visual/interativo em navegador. A configuração da Vercel foi preparada consultando a documentação oficial; a publicação deve ser validada no ambiente da conta do usuário. TLS com o provedor remoto também precisa ser verificado com as credenciais e CA reais.

O teste em MariaDB verifica o protocolo MySQL e comportamento transacional, mas não substitui a execução da suíte no serviço e versão finais, especialmente em serviços compatíveis como TiDB.

O pytest emitiu dois avisos de depreciação provenientes da combinação Starlette/TestClient/httpx e de um alias de AnyIO. Não houve falha de teste. As versões usadas estão registradas em `requirements-lock.txt`.

Para repetir: siga os comandos e a configuração do banco isolado na etapa 10 do README. As dependências de análise sintática e a instalação portátil do banco foram usadas apenas como ferramentas locais de QA, dentro de `.local/`, que é ignorada pelo Git e pela Vercel.

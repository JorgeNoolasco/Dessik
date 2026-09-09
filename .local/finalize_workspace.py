from pathlib import Path
from bs4 import BeautifulSoup
import jsbeautifier
import cssbeautifier

root = Path(__file__).resolve().parents[1]
ws = root / 'workspace'
pub = ws / 'publico'

for path in pub.glob('*.html'):
    source = path.read_text(encoding='utf-8')
    source = source.replace('01 / 08', 'DESSIK / 2026')
    if path.name == 'index.html':
        source = source.replace('href="/loja.html" aria-current="page"', 'href="/loja.html"')
        source = source.replace('<a href="/index.html">Início</a>', '<a href="/index.html" aria-current="page">Início</a>')
    if path.name == 'carrinho.html':
        source = source.replace('href="/loja.html" aria-current="page"', 'href="/loja.html"')
        source = source.replace('<a href="/carrinho.html">Carrinho</a>', '<a href="/carrinho.html" aria-current="page">Carrinho</a>')
    # Formata para estudar: tags em linhas separadas e indentação visível.
    path.write_text(BeautifulSoup(source, 'html.parser').prettify(), encoding='utf-8')
for path in (pub / 'js').glob('*.js'):
    path.write_text(jsbeautifier.beautify(path.read_text(encoding='utf-8')) + '\n', encoding='utf-8')
for path in (pub / 'css').glob('*.css'):
    path.write_text(cssbeautifier.beautify(path.read_text(encoding='utf-8')) + '\n', encoding='utf-8')

descriptions = {
 'index.html': 'Apresenta a loja, carrega quatro produtos da API e mostra os benefícios.',
 'loja.html': 'Organiza a vitrine, a busca e as categorias. Os cards são criados pelo JavaScript.',
 'cadastro.html': 'Mostra o formulário de conta e endereço.',
 'login.html': 'Mostra os campos de e-mail e senha.',
 'carrinho.html': 'Mostra itens selecionados, resumo e botão de finalizar pedido.',
 'admin.html': 'Organiza o formulário de produto e a tabela administrativa.',
 'pedidos.html': 'Mostra o histórico do usuário autenticado.',
 'style.css': 'Define a estrutura responsiva e os componentes básicos.',
 'storefront.css': 'Define a identidade visual Dessik e adapta as superfícies para o fundo claro.',
 'api.js': 'Centraliza a URL da API, fetch, mensagens, sessão e elementos com textContent.',
 'loja.js': 'Consulta produtos, cria cards, mostra estoque e adiciona ao carrinho.',
 'carrinho.js': 'Guarda IDs e quantidades na aba, consulta preços e envia todos os itens do pedido.',
 'cadastro.js': 'Valida o formulário, sugere senha e consulta ViaCEP por meio da API.',
 'login.js': 'Autentica e guarda o JWT temporário na sessão da aba.',
 'admin.js': 'Envia requisições para criar, atualizar e excluir produtos.',
 'pedidos.js': 'Consulta e exibe os próprios pedidos.',
 'index.py': 'Exporta a aplicação FastAPI para a Vercel.',
 'main.py': 'Define as rotas, valida pedidos e registra tudo na transação SQL.',
 'database.py': 'Lê configuração privada e garante commit, rollback e fechamento da conexão.',
 'auth.py': 'Protege senhas com bcrypt, verifica JWT e consulta a permissão administrativa.',
 'models.py': 'Converte valores monetários para JSON, sem usar ORM.',
 'schemas.py': 'Rejeita campos e valores inválidos antes de executar as regras da API.',
 'schema.sql': 'Cria as quatro tabelas, seus relacionamentos e restrições.',
 'dados.sql': 'Insere doze produtos sem reiniciar estoque já existente.',
 'vercel.json': 'Seleciona o suporte nativo ao FastAPI.',
 '.env.example': 'Lista variáveis sem incluir segredos reais.',
 '.gitignore': 'Mantém arquivos privados e temporários fora do Git.',
 'requirements.txt': 'Lista as bibliotecas necessárias à execução.',
 'requirements-dev.txt': 'Acrescenta pytest para executar os testes.',
 'pytest.ini': 'Configura descoberta de testes e a marca de integração.',
}
extensions = {'.py':'python', '.js':'javascript', '.css':'css', '.html':'html', '.sql':'sql', '.json':'json', '.svg':'xml'}
guide = ['# Dessik — código completo\n', 'Esta cópia reúne os arquivos textuais da entrega. Consulte README.md para executar, estudar, testar e apresentar. Nenhum segredo do `.env` é incluído. As imagens PNG são entregues como arquivos em `publico/imagens/`.\n']
for folder in (pub, ws / 'privada'):
    for path in sorted(folder.rglob('*')):
        if not path.is_file() or any(part in {'.venv', '__pycache__', '.pytest_cache'} for part in path.parts): continue
        if path.name == '.env' or path.suffix in {'.png', '.pyc', '.md'}: continue
        source = path.read_text(encoding='utf-8')
        relative = path.relative_to(ws).as_posix()
        guide.extend([f'\n## ARQUIVO: {relative}\n', f'```{extensions.get(path.suffix, "text")}\n{source.rstrip()}\n```\n',
                      'O que este arquivo faz:\n\n- ' + descriptions.get(path.name, 'Fornece uma imagem local editável.' if path.suffix == '.svg' else 'Verifica funcionalidades e proteções no ambiente de testes.') + '\n'])
(ws / 'CODIGO_COMPLETO.md').write_text('\n'.join(guide), encoding='utf-8')
print('Código formatado e guia integral gerado.')

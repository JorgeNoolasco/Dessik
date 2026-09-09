-- MySQL 8.0.16+ (InnoDB). Execute no banco escolhido na conexão.
-- Em provedores sem CREATE DATABASE, crie/selecione o banco pelo painel.
-- Opcional, em servidor próprio:
-- CREATE DATABASE loja_ficticia CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- USE loja_ficticia;

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(254) NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    cep VARCHAR(8) NOT NULL DEFAULT '',
    logradouro VARCHAR(150) NOT NULL DEFAULT '',
    bairro VARCHAR(100) NOT NULL DEFAULT '',
    cidade VARCHAR(100) NOT NULL DEFAULT '',
    estado VARCHAR(2) NOT NULL DEFAULT '',
    data_cadastro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_usuarios_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS produtos (
    id_produto INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    descricao TEXT NOT NULL,
    categoria VARCHAR(60) NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    quantidade_estoque INT NOT NULL DEFAULT 0,
    imagem_url VARCHAR(1000) NOT NULL,
    data_cadastro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    KEY idx_produtos_categoria (categoria),
    CONSTRAINT ck_produtos_preco CHECK (preco > 0),
    CONSTRAINT ck_produtos_estoque CHECK (quantidade_estoque >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS pedidos (
    id_pedido INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    data_pedido TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    valor_total DECIMAL(16,2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'simulado',
    KEY idx_pedidos_usuario_data (id_usuario, data_pedido),
    CONSTRAINT fk_pedidos_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE RESTRICT,
    CONSTRAINT ck_pedidos_total CHECK (valor_total > 0),
    CONSTRAINT ck_pedidos_status CHECK (status = 'simulado')
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS itens_pedido (
    id_item INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10,2) NOT NULL,
    UNIQUE KEY uq_item_produto (id_pedido, id_produto),
    KEY idx_itens_produto (id_produto),
    CONSTRAINT fk_itens_pedido FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido) ON DELETE RESTRICT,
    CONSTRAINT fk_itens_produto FOREIGN KEY (id_produto) REFERENCES produtos(id_produto) ON DELETE RESTRICT,
    CONSTRAINT ck_itens_quantidade CHECK (quantidade > 0),
    CONSTRAINT ck_itens_preco CHECK (preco_unitario > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- A massa de demonstração fica em dados.sql; scripts.init_db executa ambos.

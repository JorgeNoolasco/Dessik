-- Execute uma vez, após schema.sql, em um banco vazio.
-- As condições por ID permitem repetir a inicialização sem resetar o estoque.
INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 1,'Notebook Horizon 14','Leve para estudar, criar e levar sua rotina a qualquer lugar. Tela de 14 polegadas e SSD de 512 GB.','Computadores',3299.90,8,'/imagens/catalogo-dessik.png'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=1);
INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 2,'Mouse Pulse','Precisão e conforto para trabalhar e jogar. Sensor de 6.400 DPI e seis botões.','Periféricos',129.90,24,'/imagens/catalogo-dessik.png'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=2);
INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 3,'Teclado mecânico Type','Formato compacto, conexão USB e teclas mecânicas para o seu setup.','Periféricos',249.90,15,'/imagens/catalogo-dessik.png'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=3);
INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 4,'Monitor View 24','Mais espaço para suas ideias. Painel de 24 polegadas Full HD com conexão HDMI.','Monitores',899.90,6,'/imagens/catalogo-dessik.png'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=4);
INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 5,'Headset Wave','Áudio estéreo, microfone ajustável e almofadas macias para longas sessões.','Áudio',189.90,18,'/imagens/catalogo-dessik.png'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=5);
INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 6,'Webcam Focus','Videochamadas em Full HD com microfone integrado e suporte para monitor.','Periféricos',219.90,0,'/imagens/catalogo-dessik.png'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=6);
INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 7,'SSD Sprint 1 TB','Espaço e velocidade para arquivos, jogos e projetos. Interface SATA.','Componentes',399.90,20,'/imagens/catalogo-dessik.png'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=7);
INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 8,'Memória RAM Flux 16 GB','Mais fôlego para várias tarefas. Módulo DDR4 de 3.200 MHz.','Componentes',229.90,12,'/imagens/catalogo-dessik.png'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=8);

INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 9,'Hub USB Connect','Quatro portas USB para organizar seus acessórios.','Acessórios',89.90,3,'/imagens/hub.svg'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=9);

INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 10,'Mousepad Glide','Base antiderrapante com espaço para movimentos livres.','Acessórios',49.90,30,'/imagens/mousepad.svg'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=10);

INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 11,'Suporte Rise','Suporte de mesa para elevar seu notebook.','Acessórios',119.90,2,'/imagens/suporte.svg'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=11);

INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 12,'Controle Play','Controle USB para seus jogos no computador.','Periféricos',159.90,10,'/imagens/controle.svg'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=12);

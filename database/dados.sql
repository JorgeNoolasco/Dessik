-- Execute uma vez, após schema.sql, em um banco vazio.
-- As condições por ID permitem repetir a inicialização sem resetar o estoque.
INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 1,'Notebook Horizon 14','Leve para estudar, criar e levar sua rotina a qualquer lugar. Tela de 14 polegadas e SSD de 512 GB.','Computadores',3299.90,8,'/images/catalogo-dessik.png'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=1);
INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 2,'Mouse Pulse','Precisão e conforto para trabalhar e jogar. Sensor de 6.400 DPI e seis botões.','Periféricos',129.90,24,'/images/catalogo-dessik.png'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=2);
INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 3,'Teclado mecânico Type','Formato compacto, conexão USB e teclas mecânicas para o seu setup.','Periféricos',249.90,15,'/images/catalogo-dessik.png'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=3);
INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 4,'Monitor View 24','Mais espaço para suas ideias. Painel de 24 polegadas Full HD com conexão HDMI.','Monitores',899.90,6,'/images/catalogo-dessik.png'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=4);
INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 5,'Headset Wave','Áudio estéreo, microfone ajustável e almofadas macias para longas sessões.','Áudio',189.90,18,'/images/catalogo-dessik.png'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=5);
INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 6,'Webcam Focus','Videochamadas em Full HD com microfone integrado e suporte para monitor.','Periféricos',219.90,0,'/images/catalogo-dessik.png'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=6);
INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 7,'SSD Sprint 1 TB','Espaço e velocidade para arquivos, jogos e projetos. Interface SATA.','Componentes',399.90,20,'/images/catalogo-dessik.png'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=7);
INSERT INTO produtos (id_produto,nome,descricao,categoria,preco,quantidade_estoque,imagem_url)
SELECT 8,'Memória RAM Flux 16 GB','Mais fôlego para várias tarefas. Módulo DDR4 de 3.200 MHz.','Componentes',229.90,12,'/images/catalogo-dessik.png'
WHERE NOT EXISTS (SELECT 1 FROM produtos WHERE id_produto=8);

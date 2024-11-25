# pip install vanna
from vanna.remote import VannaDefault

api_key = 'c0fd6c4f7f934137bd3b138c10fa237c'
vanna_model_name = 'premick-test' 

vn = VannaDefault(model=vanna_model_name, api_key=api_key)
# pip install 'vanna[mysql]'
vn.connect_to_mysql(host='localhost', dbname='banquinho', user='root', password='SuaSenha', port=3306)

#-----------------------------------------------------------------------------------------------------------------#

# A consulta do esquema de informações pode precisar de alguns ajustes dependendo do seu banco de dados. Este é um bom ponto de partida.
# df_information_schema = vn.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")

# Isso dividirá o esquema de informações em pedaços pequenos que podem ser referenciados pelo LLM.
# plan = vn.get_training_plan_generic(df_information_schema)
# print(plan)
# print("----------------------------------------------------------------------------------------------------------------------------------")

# Se você gostou do plano, descomente e execute-o para treinar.
# vn.train(plan=plan)

#-----------------------------------------------------------------------------------------------------------------#

# A seguir estão os MÉTODOS para ADICIONAR DADOS de TREINAMENTO.

#-----------------------------------------------------------------------------------------------------------------#

# Instruções DDL são poderosas porque especificam nomes de tabelas, nomes de colunas, tipos e, potencialmente, relacionamentos.
vn.train(ddl="""
    CREATE TABLE IF NOT EXISTS `banquinho`.`usuarios` (
    `id_usuario` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `nome_usuario` VARCHAR(45) NULL,
    `email_usuario` VARCHAR(255) NOT NULL UNIQUE,
    `senha_usuario` VARCHAR(255) NOT NULL,
    `status` SMALLINT NOT NULL DEFAULT 1,
    `perfil_acesso` VARCHAR(100) NOT NULL DEFAULT 'GERENTE'
    );

    CREATE TABLE IF NOT EXISTS `banquinho`.`clientes` (
    `id_cliente` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `nome_cliente` VARCHAR(100) NOT NULL,
    `cep` VARCHAR(10) NULL,
    `logradouro` VARCHAR(100) NULL,
    `numero` VARCHAR(10) NULL,
    `complemento` VARCHAR(50) NULL,
    `bairro` VARCHAR(50) NULL,
    `cidade` VARCHAR(50) NULL,
    `uf` VARCHAR(2) NULL,
    `telefone_cliente` VARCHAR(11) NULL,
    `CPF_cliente` VARCHAR(11) NOT NULL UNIQUE,
    `status` SMALLINT NOT NULL DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS `banquinho`.`categorias` (
    `id_categoria` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `nome_categoria` ENUM('Refrigerantes', 'Cervejas', 'Vinhos', 'Destilados', 'Sucos') NOT NULL
    );

    CREATE TABLE IF NOT EXISTS `banquinho`.`produtos` (
    `id_produto` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `nome_produto` VARCHAR(100) NOT NULL,
    `unidade_medida` VARCHAR(25) NOT NULL,
    `preco_venda` FLOAT NOT NULL DEFAULT 0.0,
    `codigo_barras` VARCHAR(255) NOT NULL,
    `codigo_interno` VARCHAR(255) NOT NULL,
    `estoque_minimo` INT NULL,
    `estoque_maximo` INT NULL,
    `status` SMALLINT NOT NULL DEFAULT 1,
    `id_categoria` INT NOT NULL,
    FOREIGN KEY (`id_categoria`) REFERENCES `banquinho`.`categorias` (`id_categoria`)
    );

    CREATE TABLE IF NOT EXISTS `banquinho`.`vendas` (
    `id_venda` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `data_compra` DATETIME NOT NULL,
    `nf_venda` VARCHAR(45) NOT NULL,
    `valor_total` FLOAT NOT NULL,
    `metodo_pagamento` VARCHAR(45) NOT NULL,
    `desconto` FLOAT NOT NULL,
    `obs_vendas` VARCHAR(255) NULL,
    `id_cliente` INT NOT NULL DEFAULT 1,
    `id_usuario` INT NOT NULL DEFAULT 1,
    FOREIGN KEY (`id_cliente`) REFERENCES `banquinho`.`clientes` (`id_cliente`),
    FOREIGN KEY (`id_usuario`) REFERENCES `banquinho`.`usuarios` (`id_usuario`)
    );

    CREATE TABLE IF NOT EXISTS `banquinho`.`produtos_vendidos` (
    `id_produto_vendido` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `id_venda` INT NOT NULL,
    `id_produto` INT NOT NULL,
    `qtde_produto` INT NOT NULL,
    `preco_unitario` FLOAT NOT NULL,
    FOREIGN KEY (`id_venda`) REFERENCES `banquinho`.`vendas` (`id_venda`),
    FOREIGN KEY (`id_produto`) REFERENCES `banquinho`.`produtos` (`id_produto`)
    );

    CREATE TABLE IF NOT EXISTS `banquinho`.`vendas_canceladas` (
    `id_venda_cancelada` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `data_venda_cancelada` DATETIME NOT NULL,
    `valor_total` FLOAT NOT NULL,
    `metodo_pagamento` VARCHAR(45) NULL,
    `desconto` FLOAT NOT NULL,
    `obs_vendas_canceladas` VARCHAR(255) NULL,
    `id_cliente` INT NOT NULL DEFAULT 1,
    `id_usuario` INT NOT NULL DEFAULT 1,
    FOREIGN KEY (`id_cliente`) REFERENCES `banquinho`.`clientes` (`id_cliente`),
    FOREIGN KEY (`id_usuario`) REFERENCES `banquinho`.`usuarios` (`id_usuario`)
    );

    CREATE TABLE IF NOT EXISTS `banquinho`.`produtos_cancelados` (
    `id_produto_cancelado` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `id_venda_cancelada` INT NULL,
    `id_venda` INT NULL,
    `id_produto` INT NOT NULL,
    `qtde_cancelada` INT NOT NULL,
    `preco_unitario` FLOAT NOT NULL,  -- Preço unitário no momento do cancelamento
    FOREIGN KEY (`id_venda`) REFERENCES `banquinho`.`vendas` (`id_venda`),
    FOREIGN KEY (`id_venda_cancelada`) REFERENCES `banquinho`.`vendas_canceladas` (`id_venda_cancelada`),
    FOREIGN KEY (`id_produto`) REFERENCES `banquinho`.`produtos` (`id_produto`)
    );

    CREATE TABLE IF NOT EXISTS `banquinho`.`entrada_produto` (
    `id_entrada_produto` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `quantidade` INT NOT NULL,
    `quantidade_disponivel` INT NOT NULL, -- Atributo FIFO
    `valor_unitario` FLOAT NOT NULL,
    `data_entrada` DATETIME NOT NULL,
    `obs_entrada_produto` VARCHAR(255) NULL,
    `id_produto` INT NOT NULL,
    `id_usuario` INT NOT NULL DEFAULT 1,
    FOREIGN KEY (`id_produto`) REFERENCES `banquinho`.`produtos` (`id_produto`),
    FOREIGN KEY (`id_usuario`) REFERENCES `banquinho`.`usuarios` (`id_usuario`)
    );

    CREATE TABLE IF NOT EXISTS `banquinho`.`saida_produto` (
    `id_saida_produto` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `quantidade` INT NOT NULL,
    `valor_unitario` FLOAT NOT NULL,
    `data_saida` DATETIME NOT NULL,
    `obs_saida_produto` VARCHAR(255) NULL,
    `id_produto` INT NOT NULL,
    `id_usuario` INT NOT NULL DEFAULT 1,
    FOREIGN KEY (`id_produto`) REFERENCES `banquinho`.`produtos` (`id_produto`),
    FOREIGN KEY (`id_usuario`) REFERENCES `banquinho`.`usuarios` (`id_usuario`)
    );

    CREATE TABLE IF NOT EXISTS `banquinho`.`estoque` (
    `id_estoque` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `qtde_atual` INT NOT NULL,
    `status` SMALLINT NOT NULL DEFAULT 1,
    `id_produto` INT NOT NULL
    );

    CREATE TABLE `banquinho`.`alertas_estoque` (
        `id_alerta` INT AUTO_INCREMENT PRIMARY KEY,
        `id_produto` INT,
        `mensagem` VARCHAR(255),
        `data_alerta` DATETIME,
        `visualizado` SMALLINT NOT NULL,
        FOREIGN KEY (`id_produto`) REFERENCES `banquinho`.`produtos` (`id_produto`)
    );
""")

# vn.train(ddl="""
#     -- --------------------- --
#     -- TRIGGERS & PROCEDURES --
#     -- --------------------- --
    
#     -- Gatilho para CRIAÇÃO do ESTOQUE
#     DELIMITER //
#     CREATE TRIGGER apos_insert_produto_no_estoque
#     AFTER INSERT ON produtos
#     FOR EACH ROW
#     BEGIN
#         INSERT INTO estoque ( qtde_atual, status, id_produto) 
#         VALUES (0, 1, NEW.id_produto);
#     END;
#     //
#     DELIMITER ;

#     -- Gatilho para SAÍDA AUTOMÁTICA após PRODUTO ser VENDIDO
#     DELIMITER //
#     CREATE TRIGGER apos_insert_produto_vendido
#     AFTER INSERT ON produtos_vendidos
#     FOR EACH ROW
#     BEGIN
#         DECLARE var_preco FLOAT;
            
#         SELECT preco_venda INTO var_preco
#         FROM produtos
#         WHERE id_produto = NEW.id_produto;
        
#         INSERT INTO saida_produto (quantidade, valor_unitario, data_saida, obs_saida_produto, id_produto) 
#         VALUES (NEW.qtde_produto, var_preco, NOW(), 'VENDA PDV', NEW.id_produto);
#     END;
#     //
#     DELIMITER ;

#     -- Gatilho para ENTRADA AUTOMÁTICA no ESTOQUE
#     DELIMITER //
#     CREATE TRIGGER apos_insert_entrada_produto
#     AFTER INSERT ON entrada_produto
#     FOR EACH ROW
#     BEGIN
#         UPDATE estoque
#         SET qtde_atual = qtde_atual + NEW.quantidade
#         WHERE id_produto = NEW.id_produto;
#     END;
#     //
#     DELIMITER ;

#     -- Gatilho para ATUALIZAÇÃO de ENTRADA no ESTOQUE
#     DELIMITER //
#     CREATE TRIGGER apos_entrada_produto_update
#     AFTER UPDATE ON entrada_produto
#     FOR EACH ROW
#     BEGIN
#         UPDATE estoque
#         SET qtde_atual = qtde_atual - OLD.quantidade + NEW.quantidade
#         WHERE id_produto = NEW.id_produto;
#     END;
#     //
#     DELIMITER ;

#     -- Gatilho para ATUALIZAÇÃO de SAIDA no ESTOQUE
#     DELIMITER //
#     CREATE TRIGGER apos_update_saida_produto
#     AFTER UPDATE ON saida_produto
#     FOR EACH ROW
#     BEGIN
#         UPDATE estoque
#         SET qtde_atual = qtde_atual + OLD.quantidade - NEW.quantidade
#         WHERE id_produto = NEW.id_produto;
#     END;
#     //
#     DELIMITER ;

#     -- Gatilho de verificação de ESTOQUE MIN E MAX
#     DELIMITER //
#     CREATE TRIGGER apos_update_estoque
#     AFTER UPDATE ON estoque
#     FOR EACH ROW
#     BEGIN
#         DECLARE min_estoque INT;
#         DECLARE max_estoque INT;

#         SELECT estoque_minimo, estoque_maximo INTO min_estoque, max_estoque
#         FROM produtos
#         WHERE id_produto = NEW.id_produto;

#         -- Verifica se o estoque está abaixo do mínimo
#         IF NEW.qtde_atual < min_estoque THEN
#             INSERT INTO alertas_estoque (id_produto, mensagem, data_alerta)
#             VALUES (NEW.id_produto, 'Estoque abaixo do mínimo', NOW());
#         END IF;

#         -- Verifica se o estoque está acima do máximo
#         IF NEW.qtde_atual > max_estoque THEN
#             INSERT INTO alertas_estoque (id_produto, mensagem, data_alerta)
#             VALUES (NEW.id_produto, 'Estoque acima do máximo', NOW());
#         END IF;
#     END;
#     //
#     DELIMITER ;


#     -- ------------------- --
#     -- GERENCIAMENTO FIFO  --
#     -- ------------------- --

#     -- Procedure para Realizar a Lógica FIFO
#     DELIMITER //
#     CREATE PROCEDURE atualizar_estoque_fifo(IN produto_id INT, IN quantidade_retirada INT)
#     BEGIN
#         DECLARE quantidade_a_retirar INT DEFAULT quantidade_retirada;
#         DECLARE qtde_disponivel INT DEFAULT 0;
#         DECLARE entrada_id INT;

#         -- Calcula a quantidade total disponível antes de prosseguir
#         SELECT SUM(quantidade_disponivel) INTO qtde_disponivel
#         FROM entrada_produto
#         WHERE id_produto = produto_id AND quantidade_disponivel > 0;

#         -- Se a quantidade total disponível for insuficiente, lança o erro
#         IF qtde_disponivel < quantidade_a_retirar THEN
#             SIGNAL SQLSTATE '45000' 
#             SET MESSAGE_TEXT = 'Quantidade insuficiente no estoque com base no método FIFO';
#         END IF;

#         -- Verifica se há pelo menos um lote disponível
#         SELECT COUNT(*) INTO qtde_disponivel
#         FROM entrada_produto
#         WHERE id_produto = produto_id AND quantidade_disponivel > 0;

#         IF qtde_disponivel = 0 THEN
#             SIGNAL SQLSTATE '45000' 
#             SET MESSAGE_TEXT = 'Não há lotes disponíveis para retirar';
#         END IF;

#         -- Loop para retirar a quantidade desejada do estoque em ordem FIFO
#         WHILE quantidade_a_retirar > 0 DO
#             -- Seleciona o lote mais antigo com quantidade disponível
#             SELECT id_entrada_produto, quantidade_disponivel 
#             INTO entrada_id, qtde_disponivel
#             FROM entrada_produto
#             WHERE id_produto = produto_id AND quantidade_disponivel > 0
#             ORDER BY data_entrada ASC
#             LIMIT 1;

#             -- Se não encontrar nenhum lote, sai do loop
#             IF entrada_id IS NULL THEN
#                 SIGNAL SQLSTATE '45000' 
#                 SET MESSAGE_TEXT = 'Não há mais lotes disponíveis para retirar';
#             END IF;

#             -- Verifica se o lote selecionado é suficiente
#             IF quantidade_a_retirar <= qtde_disponivel THEN
#                 UPDATE entrada_produto 
#                 SET quantidade_disponivel = quantidade_disponivel - quantidade_a_retirar
#                 WHERE id_entrada_produto = entrada_id;
#                 SET quantidade_a_retirar = 0;
#             ELSE
#                 SET quantidade_a_retirar = quantidade_a_retirar - qtde_disponivel;
#                 UPDATE entrada_produto 
#                 SET quantidade_disponivel = 0
#                 WHERE id_entrada_produto = entrada_id;
#             END IF;
#         END WHILE;
#     END;
#     //
#     DELIMITER ;

#     -- Chama a procedure FIFO
#     DELIMITER //
#     CREATE TRIGGER antes_saida_produto_insert
#     BEFORE INSERT ON saida_produto
#     FOR EACH ROW
#     BEGIN
#         CALL atualizar_estoque_fifo(NEW.id_produto, NEW.quantidade);
#     END;
#     //
#     DELIMITER ;

#     -- Gatilho que soma as quantidades disponíveis e registra no estoque
#     DELIMITER //
#     CREATE TRIGGER apos_insert_saida_produto
#     AFTER INSERT ON saida_produto
#     FOR EACH ROW
#     BEGIN
#         DECLARE quantidade_total INT;

#         -- Calcula a quantidade atualizada no estoque para o produto
#         SELECT SUM(quantidade_disponivel) INTO quantidade_total
#         FROM entrada_produto
#         WHERE id_produto = NEW.id_produto;

#         -- Atualiza o estoque
#         UPDATE estoque
#         SET qtde_atual = quantidade_total
#         WHERE id_produto = NEW.id_produto;
#     END;
#     //
#     DELIMITER ;
# """)

#-----------------------------------------------------------------------------------------------------------------#

# Documentação sobre as definições da sua empresa.
# vn.train(documentation="""
#     Seu nome é Mick, você é um assistente para um aplicativo de Gerenciamento de Recursos 
# """)


# Tabela usuarios
vn.train(documentation="A tabela `usuarios` armazena informações dos usuários do sistema (Todos os usuários podem vender, ou seja, também são vendedores), incluindo nome, email, senha e perfil de acesso. Os perfis de acesso definem o cargo do colaborador (usuário que está utilizando o sistema). Apenas usuários com `status = 1` estão ativos no sistema.")

# Tabela clientes
vn.train(documentation='A tabela `clientes` armazena dados de clientes, incluindo nome, endereço, telefone e CPF. Apenas clientes com `status = 1` estão ativos. Os campos de endereço incluem `cep`, `logradouro`, `numero`, `complemento`, `bairro`, `cidade`, e `uf`.')

# Tabela categorias
vn.train(documentation='A tabela `categorias` define categorias de produtos disponíveis. Cada produto deve estar vinculado a uma categoria.')

# Tabela produtos
vn.train(documentation='A tabela `produtos` contém informações sobre os produtos, como nome, unidade de medida, preço de venda, códigos de identificação, e estoques mínimos e máximos. Apenas produtos com `status = 1` estão ativos. Cada produto está associado a uma categoria via `id_categoria`.')

# Tabela vendas
vn.train(documentation='A tabela `vendas` registra todas as vendas realizadas, incluindo data, nota fiscal, valor total, método de pagamento, desconto e observações. Cada venda está vinculada a um cliente (`id_cliente`) e a um usuário (`id_usuario`).')

# Tabela produtos_vendidos
vn.train(documentation='A tabela `produtos_vendidos` detalha os produtos de cada venda, com informações como quantidade, preço unitário e referências à venda (`id_venda`) e ao produto (`id_produto`).')

# Tabela vendas_canceladas
vn.train(documentation='A tabela `vendas_canceladas` registra vendas que foram canceladas, com informações similares à tabela `vendas` exceto nota fiscal. Cada venda cancelada é vinculada a um cliente e a um usuário.')

# Tabela produtos_cancelados
vn.train(documentation='A tabela `produtos_cancelados` detalha tanto os produtos cancelados de uma venda legítima, quanto de vendas canceladas completamente, com informações sobre quantidade cancelada, preço unitário no momento do cancelamento, e referências às tabelas de vendas, vendas_canceladas e produtos.')

# Tabela entrada_produto
vn.train(documentation='A tabela `entrada_produto` registra entradas de produtos no estoque, incluindo quantidade, valor unitário, data e observações. A coluna `quantidade_disponivel` é usada para implementar o método FIFO.')

# Tabela saida_produto
vn.train(documentation='A tabela `saida_produto` registra saídas de produtos do estoque tanto por vendas quanto por baixas manuais (perdas ou avarias), incluindo quantidade, valor unitário, data e observações. Saídas de produtos com a observação "VENDA PDV" na coluna obs_saida_produto estão ligadas a vendas realizadas.')

# Tabela estoque
vn.train(documentation='A tabela `estoque` mantém o saldo atual de produtos no estoque. Alertas de estoque mínimo e máximo são gerados automaticamente com base nos limites configurados na tabela `produtos`.')

# Tabela alertas_estoque
vn.train(documentation='A tabela `alertas_estoque` armazena notificações geradas quando o estoque está abaixo do mínimo ou acima do máximo. Alertas com `visualizado = 1` foram visualizadas. Cada alerta está vinculado a um produto e inclui uma mensagem e a data do alerta.')

# Regras FIFO
# vn.train(documentation='A lógica FIFO (First In, First Out) é aplicada para saídas de produtos, garantindo que os lotes mais antigos sejam consumidos primeiro. A procedure `atualizar_estoque_fifo` gerencia essa lógica.')

# Gatilhos de Estoque
# vn.train(documentation="""
#     Gatilhos que garantem a consistência do estoque:
#         - `apos_insert_entrada_produto`: Atualiza o estoque ao registrar novas entradas.
#         - `apos_insert_saida_produto`: Ajusta o estoque após saídas de produtos.
#         - `apos_update_estoque`: Gera alertas para estoques abaixo do mínimo ou acima do máximo.
# """)

# Relacionamentos Importantes
vn.train(documentation="""
    Relacionamentos Importantes:
        - Produtos estão vinculados a categorias via `id_categoria`.
        - Vendas e vendas canceladas estão associadas a clientes e usuários.
        - Produtos vendidos e cancelados estão relacionados às tabelas `vendas`, `vendas_canceladas` e `produtos`.
""")


# vn.train(documentation='')

#-----------------------------------------------------------------------------------------------------------------#

# Você também pode adicionar consultas SQL aos seus dados de treinamento. Isso é útil se você já tiver algumas dúvidas.
vn.train(question="Qual é o produto mais vendido?",
        sql="SELECT p.nome_produto, SUM(pv.qtde_produto) AS total_vendido FROM produtos_vendidos pv JOIN produtos p ON pv.id_produto = p.id_produto GROUP BY pv.id_produto ORDER BY total_vendido DESC LIMIT 1;")

vn.train(question="Qual é o nome do cliente que mais comprou?",
        sql="SELECT c.nome_cliente, SUM(pv.qtde_produto) AS total_comprado FROM clientes c JOIN vendas v ON c.id_cliente = v.id_cliente JOIN produtos_vendidos pv ON v.id_venda = pv.id_venda GROUP BY c.id_cliente ORDER BY total_comprado DESC LIMIT 1;")

#-----------------------------------------------------------------------------------------------------------------#

# 1. Vendas Totais por Período
vn.train(
    question="Quais são as vendas totais por período?",
    sql="""
    SELECT DATE(data_compra) AS dia, 
            COUNT(v.id_venda) AS total_vendas, 
            SUM(valor_total) AS valor_total_vendido,
            SUM(pv.qtde_produto) AS produtos_vendidos
    FROM vendas v
    JOIN produtos_vendidos pv ON v.id_venda = pv.id_venda
    GROUP BY dia
    ORDER BY dia DESC;
""")

# 2. Vendas por Produto
vn.train(
    question="Quais são os produtos mais vendidos e os valores totais vendidos?",
    sql="""
    SELECT p.nome_produto, 
            SUM(pv.qtde_produto) AS total_vendido, 
            SUM(pv.qtde_produto * pv.preco_unitario) AS valor_total_vendido
    FROM produtos_vendidos pv
    JOIN produtos p ON pv.id_produto = p.id_produto
    GROUP BY p.nome_produto
    ORDER BY total_vendido DESC;
""")

# 3. Vendas por Cliente
vn.train(
    question="Quais clientes mais compraram e quanto gastaram no total?",
    sql="""
    SELECT c.nome_cliente, 
            COUNT(v.id_venda) AS total_compras, 
            SUM(v.valor_total) AS valor_total_gasto
    FROM vendas v
    JOIN clientes c ON v.id_cliente = c.id_cliente
    GROUP BY c.nome_cliente
    ORDER BY valor_total_gasto DESC;
""")

# 4. Método de Pagamento Mais Usado
vn.train(
    question="Qual é o método de pagamento mais usado e seu total em vendas?",
    sql="""
    SELECT metodo_pagamento, 
            COUNT(id_venda) AS total_transacoes,
            SUM(valor_total) AS valor_total
    FROM vendas
    GROUP BY metodo_pagamento
    ORDER BY total_transacoes DESC;
    """
)

# 5. Estoque Atual
vn.train(
    question="Qual é o estoque atual de cada produto e seus limites?",
    sql="""
    SELECT p.nome_produto, 
            e.qtde_atual AS estoque_atual, 
            p.estoque_minimo, 
            p.estoque_maximo
    FROM estoque e
    JOIN produtos p ON e.id_produto = p.id_produto
    ORDER BY p.nome_produto;
    """
)

# 6. Produtos com Alerta de Estoque
vn.train(
    question="Quais produtos estão com alertas de estoque e quais são os alertas?",
    sql="""
    SELECT p.nome_produto, 
            a.mensagem, 
            a.data_alerta
    FROM alertas_estoque a
    JOIN produtos p ON a.id_produto = p.id_produto
    ORDER BY a.data_alerta DESC;
    """
)

# 7. Clientes Ativos e Inativos
vn.train(
    question="Quais são os clientes ativos e inativos?",
    sql="""
    SELECT nome_cliente, 
            telefone_cliente, 
            status
    FROM clientes
    ORDER BY status DESC;
    """
)

# 8. Produtos Vendidos por Categoria
vn.train(
    question="Quais produtos foram vendidos por categoria e seus totais?",
    sql="""
    SELECT c.nome_categoria, 
            p.nome_produto, 
            SUM(pv.qtde_produto) AS total_vendido,
            SUM(pv.qtde_produto * pv.preco_unitario) AS valor_total_vendido
    FROM produtos_vendidos pv
    JOIN produtos p ON pv.id_produto = p.id_produto
    JOIN categorias c ON p.id_categoria = c.id_categoria
    GROUP BY c.nome_categoria, p.nome_produto
    ORDER BY c.nome_categoria, total_vendido DESC;
    """
)
#-----------------------------------------------------------------------------------------------------------------#

# Vendas Totais por Período
vn.train(
    question="Quais foram as vendas totais por dia?",
    sql="""
        SELECT DATE(data_compra) AS dia, 
               COUNT(id_venda) AS total_vendas, 
               SUM(valor_total) AS valor_total_vendido,
               SUM(pv.qtde_produto) AS produtos_vendidos
        FROM vendas v
        JOIN produtos_vendidos pv ON v.id_venda = pv.id_venda
        GROUP BY dia
        ORDER BY dia DESC;
    """
)

# Vendas por Produto
vn.train(
    question="Quantos produtos foram vendidos e qual o valor total por produto?",
    sql="""
        SELECT p.nome_produto, 
               SUM(pv.qtde_produto) AS total_vendido, 
               SUM(pv.qtde_produto * pv.preco_unitario) AS valor_total_vendido
        FROM produtos_vendidos pv
        JOIN produtos p ON pv.id_produto = p.id_produto
        GROUP BY p.nome_produto
        ORDER BY total_vendido DESC;
    """
)

# Vendas por Cliente
vn.train(
    question="Quais clientes fizeram mais compras e quanto gastaram?",
    sql="""
        SELECT c.nome_cliente, 
               COUNT(v.id_venda) AS total_compras, 
               SUM(v.valor_total) AS valor_total_gasto
        FROM vendas v
        JOIN clientes c ON v.id_cliente = c.id_cliente
        GROUP BY c.nome_cliente
        ORDER BY valor_total_gasto DESC;
    """
)

# Método de Pagamento Mais Usado
vn.train(
    question="Qual o método de pagamento mais utilizado e seu valor total?",
    sql="""
        SELECT metodo_pagamento, 
               COUNT(id_venda) AS total_transacoes,
               SUM(valor_total) AS valor_total
        FROM vendas
        GROUP BY metodo_pagamento
        ORDER BY total_transacoes DESC;
    """
)


# PAREI AQUI --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Vendas por Usuário/Vendedor
vn.train(
    question="Quais vendedores fizeram mais vendas e quanto venderam?",
    sql="""
        SELECT u.nome_usuario, 
               COUNT(v.id_venda) AS total_vendas, 
               SUM(v.valor_total) AS valor_total_vendido
        FROM vendas v
        JOIN usuarios u ON v.id_usuario = u.id_usuario
        GROUP BY u.nome_usuario
        ORDER BY total_vendas DESC;
    """
)

# Estoque Atual
vn.train(
    question="Como está o estoque atual dos produtos?",
    sql="""
        SELECT p.nome_produto, 
               e.qtde_atual AS estoque_atual, 
               p.estoque_minimo, 
               p.estoque_maximo
        FROM estoque e
        JOIN produtos p ON e.id_produto = p.id_produto
        ORDER BY p.nome_produto;
    """
)

# Produtos com Alerta de Estoque
# vn.train(
#     question="Quais produtos têm alertas de estoque e por quê?",
#     sql="""
#         SELECT p.nome_produto, 
#                a.mensagem, 
#                a.data_alerta
#         FROM alertas_estoque a
#         JOIN produtos p ON a.id_produto = p.id_produto
#         ORDER BY a.data_alerta DESC;
#     """
# )

# Produtos Mais Vendidos
vn.train(
    question="Quais são os produtos mais vendidos?",
    sql="""
        SELECT p.nome_produto, 
               SUM(pv.qtde_produto) AS total_vendido
        FROM produtos_vendidos pv
        JOIN produtos p ON pv.id_produto = p.id_produto
        GROUP BY p.nome_produto
        ORDER BY total_vendido DESC;
    """
)

# Produtos Menos Vendidos
vn.train(
    question="Quais são os produtos menos vendidos?",
    sql="""
        SELECT p.nome_produto, 
               SUM(pv.qtde_produto) AS total_vendido
        FROM produtos_vendidos pv
        JOIN produtos p ON pv.id_produto = p.id_produto
        GROUP BY p.nome_produto
        ORDER BY total_vendido ASC;
    """
)

# Produtos Vendidos por Categoria
vn.train(
    question="Quantos produtos foram vendidos por categoria e qual o valor total?",
    sql="""
        SELECT c.nome_categoria, 
               p.nome_produto, 
               SUM(pv.qtde_produto) AS total_vendido,
               SUM(pv.qtde_produto * pv.preco_unitario) AS valor_total_vendido
        FROM produtos_vendidos pv
        JOIN produtos p ON pv.id_produto = p.id_produto
        JOIN categorias c ON p.id_categoria = c.id_categoria
        GROUP BY c.nome_categoria, p.nome_produto
        ORDER BY c.nome_categoria, total_vendido DESC;
    """
)

# Entradas de Produtos por Período
# vn.train(
#     question="Quais foram as entradas de produtos no estoque por período?",
#     sql="""
#         SELECT p.nome_produto, 
#                e.quantidade, 
#                e.valor_unitario, 
#                e.data_entrada, 
#                u.nome_usuario AS responsavel
#         FROM entrada_produto e
#         JOIN produtos p ON e.id_produto = p.id_produto
#         JOIN usuarios u ON e.id_usuario = u.id_usuario
#         ORDER BY e.data_entrada DESC;
#     """
# )

# Saídas de Produtos por Período
# vn.train(
#     question="Quais foram as saídas de produtos no estoque por período?",
#     sql="""
#         SELECT p.nome_produto, 
#                s.quantidade, 
#                s.valor_unitario, 
#                s.data_saida, 
#                u.nome_usuario AS responsavel
#         FROM saida_produto s
#         JOIN produtos p ON s.id_produto = p.id_produto
#         JOIN usuarios u ON s.id_usuario = u.id_usuario
#         ORDER BY s.data_saida DESC;
#     """
# )

# Fluxo de Estoque (FIFO)
# vn.train(
#     question="Qual é o fluxo de estoque dos produtos usando o método FIFO?",
#     sql="""
#         SELECT p.nome_produto, 
#                e.data_entrada, 
#                e.quantidade AS quantidade_inicial,
#                (e.quantidade - e.quantidade_disponivel) AS quantidade_utilizada,
#                e.quantidade_disponivel AS quantidade_atual,
#                e.valor_unitario
#         FROM entrada_produto e
#         JOIN produtos p ON e.id_produto = p.id_produto
#         ORDER BY p.nome_produto, e.data_entrada;
#     """
# )

# Vendas Canceladas
vn.train(
    question="Quais vendas foram canceladas e por quem?",
    sql="""
        SELECT c.nome_cliente, 
               v.valor_total, 
               v.data_venda_cancelada, 
               v.metodo_pagamento, 
               u.nome_usuario AS responsavel
        FROM vendas_canceladas v
        JOIN clientes c ON v.id_cliente = c.id_cliente
        JOIN usuarios u ON v.id_usuario = u.id_usuario
        ORDER BY v.data_venda_cancelada DESC;
    """
)

# Produtos Cancelados
vn.train(
    question="Quais produtos foram cancelados e em quais vendas?",
    sql="""
        SELECT p.nome_produto, 
               pc.qtde_cancelada, 
               pc.preco_unitario, 
               vc.data_venda_cancelada, 
               u.nome_usuario AS responsavel
        FROM produtos_cancelados pc
        JOIN produtos p ON pc.id_produto = p.id_produto
        JOIN vendas_canceladas vc ON pc.id_venda_cancelada = vc.id_venda_cancelada
        JOIN usuarios u ON vc.id_usuario = u.id_usuario
        ORDER BY vc.data_venda_cancelada DESC;
    """
)

# Compras por Cliente
vn.train(
    question="Quantas compras foram feitas por cliente e quanto eles gastaram?",
    sql="""
        SELECT c.nome_cliente, 
               COUNT(v.id_venda) AS total_compras, 
               SUM(v.valor_total) AS total_gasto
        FROM vendas v
        JOIN clientes c ON v.id_cliente = c.id_cliente
        GROUP BY c.nome_cliente
        ORDER BY total_gasto DESC;
    """
)

# Clientes por Região
vn.train(
    question="Quantos clientes existem por região?",
    sql="""
        SELECT cidade, 
               uf, 
               COUNT(id_cliente) AS total_clientes
        FROM clientes
        GROUP BY cidade, uf
        ORDER BY total_clientes DESC;
    """
)

# Vendas Realizadas por Usuário
vn.train(
    question="Quantas vendas foram realizadas por cada usuário e quanto venderam?",
    sql="""
        SELECT u.nome_usuario, 
               COUNT(v.id_venda) AS total_vendas, 
               SUM(v.valor_total) AS valor_total_vendido
        FROM vendas v
        JOIN usuarios u ON v.id_usuario = u.id_usuario
        GROUP BY u.nome_usuario
        ORDER BY total_vendas DESC;
    """
)

# Produtos Vendidos por Usuário
vn.train(
    question="Quais produtos foram vendidos por cada usuário e seus valores totais?",
    sql="""
        SELECT u.nome_usuario, 
               p.nome_produto, 
               SUM(pv.qtde_produto) AS total_vendido,
               SUM(pv.qtde_produto * pv.preco_unitario) AS valor_total_vendido
        FROM vendas v
        JOIN produtos_vendidos pv ON v.id_venda = pv.id_venda
        JOIN produtos p ON pv.id_produto = p.id_produto
        JOIN usuarios u ON v.id_usuario = u.id_usuario
        GROUP BY u.nome_usuario, p.nome_produto
        ORDER BY u.nome_usuario, total_vendido DESC;
    """
)

#-----------------------------------------------------------------------------------------------------------------#

'''
## Perguntando à IA
Sempre que você fizer uma nova pergunta, ele encontrará os 10 dados de treinamento mais relevantes e os usará como parte do prompt do LLM para gerar o SQL.
'''
# res = vn.ask(question="Quais usuarios estão ativos?", allow_llm_to_see_data=True, auto_train=True) # ver funções de resposta
# print(res)

#-----------------------------------------------------------------------------------------------------------------#


# Clientes Inativos
vn.train(
    question="Quais clientes estão inativos?",
    sql="""
        SELECT nome_cliente, 
               telefone_cliente, 
               status
        FROM clientes
        WHERE status = 0
        ORDER BY status DESC;
    """
)


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
    `email_usuario` VARCHAR(255) NOT NULL,
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
    `CPF_cliente` VARCHAR(11) NULL,
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

    -- TABELA DE ALERTAS DE ESTOQUE MIN E MAX
    CREATE TABLE `banquinho`.`alertas_estoque` (
        id_alerta INT AUTO_INCREMENT PRIMARY KEY,
        id_produto INT,
        mensagem VARCHAR(255),
        data_alerta DATETIME,
        FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
    );
""")

#-----------------------------------------------------------------------------------------------------------------#

# Às vezes, você pode querer adicionar documentação sobre as definições de sua empresa.
vn.train(documentation="Our business defines OTIF score as the percentage of orders that are delivered on time and in full")

#-----------------------------------------------------------------------------------------------------------------#

# Você também pode adicionar consultas SQL aos seus dados de treinamento. Isso é útil se você já tiver algumas dúvidas.
vn.train(question="Qual é o produto mais vendido?",
        sql="SELECT p.nome_produto, SUM(pv.qtde_produto) AS total_vendido FROM produtos_vendidos pv JOIN produtos p ON pv.id_produto = p.id_produto GROUP BY pv.id_produto ORDER BY total_vendido DESC LIMIT 1;")

vn.train(question="Qual é o nome do cliente que mais comprou?",
        sql="SELECT c.nome_cliente, SUM(pv.qtde_produto) AS total_comprado FROM clientes c JOIN vendas v ON c.id_cliente = v.id_cliente JOIN produtos_vendidos pv ON v.id_venda = pv.id_venda GROUP BY c.id_cliente ORDER BY total_comprado DESC LIMIT 1;")

#-----------------------------------------------------------------------------------------------------------------#

# A qualquer momento você pode inspecionar quais dados de treinamento o pacote é capaz de referenciar.
training_data = vn.get_training_data()
print(training_data)
print("----------------------------------------------------------------------------------------------------------------------------------")

#-----------------------------------------------------------------------------------------------------------------#

# Você pode remover dados de treinamento se houver informações obsoletas/incorretas. 
# vn.remove_training_data(id='2437289-doc')
# vn.remove_training_data(id='352848-ddl')
# vn.remove_training_data(id='499273-sql')

#-----------------------------------------------------------------------------------------------------------------#

'''
## Perguntando à IA
Sempre que você fizer uma nova pergunta, ele encontrará os 10 dados de treinamento mais relevantes e os usará como parte do prompt do LLM para gerar o SQL.
'''
vn.ask(question=..., allow_llm_to_see_data=True, auto_train=True) # ver funções de resposta

#-----------------------------------------------------------------------------------------------------------------#

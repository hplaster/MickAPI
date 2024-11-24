from flask import Flask, jsonify, request
from vanna.remote import VannaDefault

# Configuração do Vanna
api_key = 'c0fd6c4f7f934137bd3b138c10fa237c'
vanna_model_name = 'premick-test'
vn = VannaDefault(model=vanna_model_name, api_key=api_key)
# pip install 'vanna[mysql]'
vn.connect_to_mysql(host='localhost', dbname='banquinho', user='root', password='SuaSenha', port=3306)

# Iniciar o Flask
app = Flask(__name__)


# Endpoint de exemplo para receber consultas e devolver respostas do chatbot
@app.route('/api/mick', methods=['POST'])
def consulta():

    dados = request.json
    pergunta = dados.get('pergunta')  # Campo com a pergunta

    # print('Tipo da Pergunta: ', type(pergunta))
    # print(pergunta)

    # Consultar o Vanna com a pergunta
    # sql, df, fig, followup_questions = vn.ask(question=pergunta, allow_llm_to_see_data=True, auto_train=True)
    sql = vn.generate_sql(question=pergunta, allow_llm_to_see_data=True)
    print('Resposta SQL: ', sql)

    df = vn.run_sql(sql)
    print("DataFrame pelo SQL: ", df)
    
    resumo = vn.generate_summary(pergunta, df)
    print("Resumo: ", resumo)

    # if not sql:
    #     return jsonify({'error': 'Não foi possível gerar uma resposta.'}), 400


    # Retornar resposta ao cliente
    # return jsonify({'resposta': f'Diretamente do Vanna, sua pergunta foi: {pergunta}'})
    return jsonify({'resposta': resumo})


# Executar a aplicação
if __name__ == '__main__':
    app.run(port=8000, host='localhost', debug=True)
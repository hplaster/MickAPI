# pip install vanna
from vanna.remote import VannaDefault

api_key = 'c0fd6c4f7f934137bd3b138c10fa237c'
vanna_model_name = 'premick-test' 

vn = VannaDefault(model=vanna_model_name, api_key=api_key)
# pip install 'vanna[mysql]'
vn.connect_to_mysql(host='localhost', dbname='banquinho', user='root', password='SuaSenha', port=3306)


# Recuperar todos os IDs dos dados de treinamento
training_data = vn.get_training_data()

# Loop para remover cada dado de treinamento individualmente
for id_data in training_data.id:
    try:
        vn.remove_training_data(id=id_data)
        print(f"Dado de treinamento com ID {id_data} removido com sucesso.")
    except Exception as e:
        print(f"Erro ao remover dado de treinamento com ID {id_data}: {e}")

print("---------- Todos os dados de treinamento foram deletados ----------")
print(training_data)
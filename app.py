# pip install vanna
from vanna.remote import VannaDefault

api_key = 'c0fd6c4f7f934137bd3b138c10fa237c'
vanna_model_name = 'premick-test' 

vn = VannaDefault(model=vanna_model_name, api_key=api_key)
# pip install 'vanna[mysql]'
vn.connect_to_mysql(host='localhost', dbname='banquinho', user='root', password='SuaSenha', port=3306)

#----------------------------------------------------------------------------------------------------#

from vanna.flask import VannaFlaskApp
VannaFlaskApp(vn=vn, allow_llm_to_see_data=True).run()

#----------------------------------------------------------------------------------------------------#

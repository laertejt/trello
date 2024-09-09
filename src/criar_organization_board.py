import pandas as pd
import os
BASE_DIR = os.path.dirname(__file__)
from bizdays import Calendar
cal = Calendar()
from utils.dataCalendario import DataCalendario
dc = DataCalendario()
key = os.environ.get('KEY')# Dados do arquivo .env
token = os.environ.get('TOKEN')# Dados do arquivo .env


# Criar Organizacao/Board
from meuTrello.trelloApi import TrelloApi
trello = TrelloApi(key, token)
trello.create_organization('Concurso Militar')#Organizacao
trello.get_organizations()
trello.create_board('Mariana Assao Takeuti', idOrganization='66dc5e4c4ef4411fd24b5072')
trello.get_boards(org_id='66dc5e4c4ef4411fd24b5072')
# Criar Listas
organizacao = "Concurso Militar"
nome="Mariana Assao Takeuti"
df_pessoas = pd.read_excel(BASE_DIR+'/data/pessoas.xlsx')
df = df_pessoas.query("organizacao==@organizacao & board==@nome")
listas = list(set(df.lists.values))
for lista in listas:
    trello.create_list(lista,idBoard="66dc5f88af9d5a615a38143f")




import pandas as pd
import re
from datetime import date, datetime, time, timedelta
import os
BASE_DIR = os.path.dirname(__file__)
from bizdays import Calendar
cal = Calendar()
from utils.dataCalendario import DataCalendario
dc = DataCalendario()
key = os.environ.get('KEY')# Dados do arquivo .env
token = os.environ.get('TOKEN')# Dados do arquivo .env
from backend.services.meuTrello.trelloCustom import TrelloCustom
tc = TrelloCustom(key, token)
# Criar cards
# Gerar atividades do MES
# Criar os cards, CheckList and CheckItems by Period ( Initial and Final date)
organizacao = "Dads School Organization"
nome="Mariana Assao Takeuti"
df_pessoas = pd.read_excel(BASE_DIR+'/data/pessoas.xlsx', sheet_name="oficial")
df = df_pessoas.query("organizacao==@organizacao & board==@nome")
initial_date = datetime(2024,10,1,8,0,0)
final_date = datetime(2024,10,31,8,0,0)
checkitem_name = "Day"
lst_lists = list(set(df.lists.values))
for list_name in lst_lists:
    df_temp = df.loc[df.lists==list_name]
    lst_cards = list(set(df_temp.cards.values))
    for card_name in lst_cards:
        df_temp1 = df_temp.loc[df.cards==card_name]
        tc.criar_card_mensal(df_temp1, initial_date, final_date, cal)



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


# Criar cards
organizacao = "Concurso Militar"
nome="Mariana Assao Takeuti"
df_pessoas = pd.read_excel(BASE_DIR+'/data/pessoas.xlsx', sheet_name="ofical")
df = df_pessoas.query("organizacao==@organizacao & board==@nome")
initial_date = datetime(2024,9,1,8,0,0)
final_date = datetime(2024,9,30,8,0,0)
checkitem_name = "Day"
lst_lists = list(set(df.lists.values))
for list_name in lst_lists:
    df_temp = df.loc[df.lists==list_name]
    lst_cards = list(set(df_temp.cards.values))
    for card_name in lst_cards:
        df_temp1 = df_temp.loc[df.cards==card_name]
        tc.criar_card_mensal(df_temp1, initial_date, final_date, cal)



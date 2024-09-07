import pandas as pd
import os
key = os.environ.get('KEY')# Dados do arquivo .env
token = os.environ.get('TOKEN')# Dados do arquivo .env
from meuTrello.trelloCustom import TrelloCustom
tc = TrelloCustom(key, token)

def gerar_df_trello(org_name, board_name, checklist_name:str = None) -> pd.DataFrame:
    checklist_name = checklist_name or 'Daily'
    #Relatorio todos
    todos = pd.DataFrame()
    df_list = tc.consultar_df_lists(org_name, board_name)
    for row in df_list.itertuples():
        list_name = row.name
        list_id =  row.id
        df_card = tc.pegar_df_cards(list_id)
        for row in df_card.itertuples():
            card_name = row.name
            df_item = tc.consultar_df_checkitems(org_name,board_name, list_name, card_name, checklist_name)
            df_item.loc[:,'list'] = list_name
            df_item.loc[:,'card'] = card_name
            todos = pd.concat([todos, df_item], ignore_index=True)
            print(row)
        df = todos.loc[:,['list','due', 'state', 'card']]
        temp = []
        temp += [i[-2:] for i in df.card.str.split().values]
        df[['month', 'year']] = temp
        # df.loc[:,'due'] = pd.to_datetime(df.loc[:,'due'])
        # df.loc[:,'month'] = df.loc[:,'due'].apply(lambda x: x.strftime('%m'))
    return df


# Porcentagem de atividade completa
def calcular_perc_total(df):
    dic = {}
    total = df.shape[0]
    complete = df.query("state=='complete'")
    complete = complete.shape[0]
    perc = complete/total
    dic['complete'] = complete
    dic['total'] = total
    dic['perc'] = perc
    return dic

def calcular_dic_perc(df) -> dict:
    dic = {}
    # Porcentagem por lista
    dic_list = {}
    for list_name in sorted(set(df.list.values)):
        df0 = df.query(" list==@list_name ")
        df1 = df0.loc[df0.state=='complete']
        if not df0.empty:
            n = df0.shape[0]
            n1 = df1.shape[0]
            dic_list[f'{list_name}_complete'] = n
            dic_list[f'{list_name}_total'] = n1
            dic_list[f'{list_name}_perc'] = n1/n
    # Porcentagem por card
    dic_card = {}
    for card_name in sorted(set(df.card.values)):
        df0 = df.query(" card==@card_name ")
        df1 = df0.loc[df0.state=='complete']
        if not df0.empty:
            n = df0.shape[0]
            n1 = df1.shape[0]
            dic_card[f'{card_name}_complete'] = n
            dic_card[f'{card_name}_total'] = n1
            dic_card[f'{card_name}_perc'] = n1/n
    dic['list'] = dic_list
    dic['card'] = dic_card
    return dic
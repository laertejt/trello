from datetime import date
import logging
logger = logging.getLogger(__name__)
import pandas as pd
import os
from bizdays import Calendar
cal = Calendar()
from backend.utils.dataCalendario import DataCalendario
dc = DataCalendario()
from dotenv import load_dotenv
load_dotenv()
key = os.environ.get('KEY')# Dados do arquivo .env
token = os.environ.get('TOKEN')# Dados do arquivo .env
from backend.services.meuTrello.trelloApi import TrelloApi
trello = TrelloApi(key, token)
from backend.services.meuTrello.trelloReport import gerar_df_trello

def gerar_df_relatorio(org_name, board_name):
    # Gerar o df
    df = gerar_df_trello(org_name, board_name)
    df.loc[:,'card'] = df.loc[:,'card'].apply(lambda x: x.split()[:-2][0] if len(x.split()[:-2])==1 else x.split()[:-2][0]+' '+x.split()[:-2][1])
    df['month'] = df.month.apply(lambda x:dc.months_in_english_to_number[x])
    # Gerar df completo e df de porcentagem(apenas)
    cards = sorted(set(df.card.values))
    months = sorted(set(df.month.values))
    # months = sorted(set(df.month.values))[:-1] # para tirar o ultimo mes
    meses = []
    df_card2 = pd.DataFrame()
    df_card3 = pd.DataFrame()
    for month in months:
        df_melt = df.melt(id_vars=['card', 'month'],value_vars=['state'])
        df_card = pd.pivot_table(df_melt[df_melt.month==month], index=['card'], columns=['month', 'value'], aggfunc='count', fill_value=0)
        # Tirar os nivels do multindex (Index e column)
        df_card.columns = df_card.columns.get_level_values(2)
        df_card.reset_index(drop=True, inplace=True)
        if 'complete' in df_card.columns:
            df_card['perc'] = df_card['complete'] / (df_card['complete'] + df_card['incomplete'] )
        else:
            df_card['perc'] = 0
        # df_card.droplevel(0, axis=0)
        df_card2 = pd.concat([df_card2, df_card],axis=1, ignore_index=True)
        df_card3 = pd.concat([df_card3, df_card['perc']],axis=1, ignore_index=True)
        mes = dc.months_in_number_to_portuguese[month]
        meses+=[mes]
        print(mes)
    df_card3.columns = meses
    df_card3.insert(0, 'cards', cards)
    # Colocar o header multiplo
    for i, month in enumerate(months):
        # Inicio do df_final
        mes = dc.months_in_number_to_portuguese[month]
        cols = pd.MultiIndex.from_tuples([(mes, 'complete'),
                                        (mes, 'incomplete'),
                                        (mes, 'porcentagem')])
        n = i*3
        cols2 = [*range(n,n+3,1)]
        data = df_card2.loc[:,cols2].values
        temp = pd.DataFrame(data, columns=cols, index=cards)
        if i==0:
            df_final=temp
        else:
            df_final = pd.merge(df_final, temp, how='inner', on=temp.index)
            df_final.drop(columns=('key_0',''), inplace=True)
        print(i,n)
    df_final.insert(0, 'cards', cards)
    # Preaparar para plotar
    graph = df_card3.copy()
    # graph.drop(['Julho'], axis=1, inplace=True)
    graph = graph.transpose().reset_index()
    graph.columns = graph.iloc[:1,:].values[0]
    graph = graph.iloc[1:,:]
    graph.rename(columns={'cards':'Mês'}, inplace=True)
    return graph, cards
    






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
from meuTrello.trelloCustom import TrelloCustom
tc = TrelloCustom(key, token)
# Dados de Entrada
nome="Mariana Assao Takeuti"
df_pessoas = pd.read_excel(BASE_DIR+'/data/pessoas.xlsx')
df = df_pessoas.query("board==@nome")
org_name = df.organizacao.values[0]
board_name = df.board.values[0]
lists  = list(set(df.lists.values))
checklist_name = 'Daily'
checkitem_name = "Day"
from meuTrello.trelloReport import gerar_df_trello, calcular_perc_total, calcular_dic_perc
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
#One Graph
import matplotlib.pyplot as plt 
import seaborn as sns
for card in cards:
    sns.lineplot(x='Mês', y=card, data=graph)
# Sub Plots
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import PercentFormatter
from math import ceil
# Define a color palette
palette = sns.color_palette("tab10")  # You can choose any other palette
fig, ax = plt.subplots(6, 2, figsize=(9, 12))
tam = ceil(len(cards))
for i in range(min(tam, 6)):  # Limit to 6 rows
    n = i * 2
    for j in range(2):  # Loop through two columns
        if n + j < len(cards):
            sns.lineplot(x='Mês', y=cards[n + j], data=graph, ax=ax[i][j], label=cards[n + j], color=palette[(n + j) % len(palette)])
            ax[i][j].tick_params(labelrotation=25, labelsize=6)
            ax[i][j].set_xlabel('')  # Remove x-axis label
            ax[i][j].set_ylabel('')
            ax[i][j].yaxis.set_major_formatter(PercentFormatter(xmax=1))
            ax[i][j].grid(color='lightgrey', linestyle='-', linewidth=0.5)  # Add light grid
            ax[i][j].legend(loc='lower center')  # Add legend in bottom right corner
            # ax[i][j].xaxis.set_visible(False)
        else:
            ax[i][j].axis('off')  # Turn off the axes if no data
# Add the title to the figure
fig.suptitle('Percentual de Atividade Realizadas', fontsize=16)
fig.tight_layout(pad=1.2)
fig.savefig(BASE_DIR + '/reports/mari.pdf')  # Adjust layout to make room for the title


# # Gerar o Dictionary completo
# dic_perc = {}
# dic_perc['total'] = calcular_perc_total(df)
# for month in months:
#     temp = df.query("month==@month")
#     dic = calcular_dic_perc(temp)
#     dic_perc[month] = dic
#     print(month)

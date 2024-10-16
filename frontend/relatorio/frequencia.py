import streamlit as st
import matplotlib.pyplot as plt 
import seaborn as sns
from matplotlib.ticker import PercentFormatter
from math import ceil
from backend.routes.urls import (botao_gerar_rel_frequencia)

st.title("Relatórios do Trello")
abas = st.tabs(["Frequência"])# Criando as abas

if "df_graph" not in st.session_state:
    st.session_state.df_graph = None
if "cards" not in st.session_state:
    st.session_state.cards = None

with abas[0]:# Primeira aba: Cadastro da Organização
    st.header("Relatório de Frenquência")
    org_name = st.text_input("Digite o nome da Organização:")
    board_name = st.text_input("Digite o nome do board:")
    if st.button("Gerar"):
        if org_name and board_name:
            if not (st.session_state.df_graph and st.session_state.cards):
                st.session_state.df_graph, st.session_state.cards = botao_gerar_rel_frequencia(org_name, board_name)
            df_graph = st.session_state.df_graph
            cards = st.session_state.cards
            palette = sns.color_palette("tab10")  # Define a color palette
            fig, ax = plt.subplots(6, 2, figsize=(9, 12))# Sub Plots
            tam = ceil(len(cards))
            for i in range(min(tam, 6)):  # Limit to 6 rows
                n = i * 2
                for j in range(2):  # Loop through two columns
                    if n + j < len(cards):
                        sns.lineplot(x='Mês', y=cards[n + j], data=df_graph, ax=ax[i][j], label=cards[n + j], color=palette[(n + j) % len(palette)])
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
            st.pyplot(fig)
        else:
            st.warning("Por favor, digite um nome da organização e do board antes de consultar.")
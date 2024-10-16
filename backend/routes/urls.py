import pandas as pd
import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()
key = os.environ.get('KEY')# Dados do arquivo .env
token = os.environ.get('TOKEN')# Dados do arquivo .env
from backend.services.meuTrello.trelloApi import TrelloApi
trello = TrelloApi(key, token)

# Menu Cadastro
@st.cache_data
def botao_cadastro_org(nome_org):
    res = trello.create_organization(nome_org)
    return res

@st.cache_data
def botao_cadastro_board(nome_org, idOrganization):
    res = trello.create_board(nome_org, idOrganization)
    return res

@st.cache_data
def botao_cadastrar_lista(nome_lista, idBoard):
    res = trello.create_list(nome_lista,idBoard)
    return res

@st.cache_data
def botao_cadastrar_card(idList, nome_card, data_ini, data_fim):
    res = trello.create_card(idList, nome_card, data_ini, data_fim)
    return res

@st.cache_data
def botao_cadastrar_checklists(idCard, name):
    res = trello.create_checklists(idCard, name)
    return res


# menu Consulta
@st.cache_data
def botao_consulta_board(idOrganization):
    res = trello.get_boards(idOrganization)
    return res

@st.cache_data
def botao_consulta_board_id(board_name):
    res = trello.get_board_id(board_name)
    return res

@st.cache_data
def botao_consulta_lista(board_id):
    res = trello.get_lists(board_id)
    return res

@st.cache_data
def botao_consulta_card(list_id):
    res = trello.get_cards(list_id)
    return res

@st.cache_data
def botao_consulta_checklist(card_id):
    res = trello.get_checklists(card_id)
    return res

# Menu Relatorios
from backend.controllers.views import gerar_df_relatorio
@st.cache_data
def botao_gerar_rel_frequencia(org_name, board_name):
    df, cards = gerar_df_relatorio(org_name, board_name)
    return df, cards

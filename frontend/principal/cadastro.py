import streamlit as st
import pandas as pd
from backend.routes.urls import (botao_cadastrar_checklists, botao_cadastro_org,
                                 botao_cadastro_board,
                                 botao_cadastrar_lista, 
                                 botao_cadastrar_card)

st.title("Cadastro do Trello")
abas = st.tabs(["Organização", "Board", "Listas", "Cards", "CheckLists"])# Criando as abas

with abas[0]:# Primeira aba: Cadastro da Organização
    st.header("Cadastro da Organização")
    nome_org = st.text_input("Digite o nome da Organização:")
    if st.button("Cadastrar Organização"):
        if nome_org:
            try:
                res = botao_cadastro_org(nome_org)
                if "id" in res:
                    st.success(f"Organização cadastrada com sucesso!: {res}")
                else:
                    st.error(f"Erro: {res}")
            except Exception as e:
                st.error(f"Erro no cadastro: {e}")    
        else:
            st.warning("Por favor, digite um nome antes de cadastrar.")

with abas[1]:# Segunda aba: Cadastro do Board
    st.header("Cadastro do Board")
    nome_board = st.text_input("Digite o nome do Board:")
    id_org = st.text_input("Digite o ID da Organização:")
    if st.button("Cadastrar Board"):
        if nome_board and id_org:
            try:
                res = botao_cadastro_board(nome_board, id_org)
                if "id" in res:
                    st.success(f"Board cadastrado com sucesso!: {res}")
                else:
                    st.error(f"Erro: {res}")
            except Exception as e:
                st.error(f"Erro no cadastro: {e}")    
        else:
            st.warning("Por favor, digite um nome e o ID antes de cadastrar.")

with abas[2]:  # Terceira aba: Cadastro de Lista
    st.header("Cadastro de Listas de Cards")
    id_org = st.text_input("Digite o ID do Board:")
    uploaded_file = st.file_uploader("Selecione o arquivo Excel que contém as listas de cards", type=["xlsx"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        if 'lists' in df.columns:
            listas = list(set(df['lists'].values))
            if st.button("Cadastrar lista"):
                for nome_lista in listas:
                    try:
                        res = botao_cadastrar_lista(nome_lista, id_org)
                        if "id" in res:
                            st.success(f"Lista de atividade cadastrada com sucesso!: {res}")
                        else:
                            st.error(f"Erro: {res}")
                    except Exception as e:
                        st.error(f"Erro no cadastro: {e}")
        else:
            st.error("O arquivo Excel não contém uma coluna 'lists'. Verifique o arquivo.")

with abas[3]:  # Quarta aba: Cadastro de Cards
    st.header("Cadastro de Cards de Atividades")
    idList = st.text_input("Digite o ID da Lista:")
    data_ini = st.date_input("Digite a Data Inicio dos Cards a serem cadastrados:")
    data_fim = st.date_input("Digite a Data Fim dos Cards a serem cadastrados:")
    uploaded_file = st.file_uploader("Selecione o arquivo Excel que contém os cards de atividades", type=["xlsx"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        if 'cards' in df.columns:
            listas = list(set(df['cards'].values))
            if st.button("Cadastrar lista"):
                for nome_card in listas:
                    try:
                        res = botao_cadastrar_card(idList, nome_card, data_ini, data_fim)
                        if "id" in res:
                            st.success(f"Cards de atividade cadastrada com sucesso!: {res}")
                        else:
                            st.error(f"Erro: {res}")
                    except Exception as e:
                        st.error(f"Erro no cadastro: {e}")
        else:
            st.error("O arquivo Excel não contém uma coluna 'cards'. Verifique o arquivo.")

with abas[4]:  # Quarta aba: Cadastro de CheckLists
    st.header("Cadastro de CheckLists")
    idCard = st.text_input("Digite o ID do Card:")
    # data_ini = st.date_input("Digite a Data Inicio dos CheckLists a serem cadastrados:")
    # data_fim = st.date_input("Digite a Data Fim dos CheckLists a serem cadastrados:")
    uploaded_file = st.file_uploader("Selecione o arquivo Excel que contém os CheckLists", type=["xlsx"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        if 'checklists' in df.columns:
            listas = list(set(df['checklists'].values))
            if st.button("Cadastrar CheckLists"):
                for nome_checklist in listas:
                    try:
                        res = botao_cadastrar_checklists(idCard, nome_checklist)
                        if "id" in res:
                            st.success(f"CheckLists cadastrada com sucesso!: {res}")
                        else:
                            st.error(f"Erro: {res}")
                    except Exception as e:
                        st.error(f"Erro no cadastro: {e}")
        else:
            st.error("O arquivo Excel não contém uma coluna 'checklists'. Verifique o arquivo.")


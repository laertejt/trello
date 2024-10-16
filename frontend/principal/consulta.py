import streamlit as st
import pandas as pd
from backend.routes.urls import (botao_consulta_board,
                                 botao_consulta_board_id,
                                 botao_consulta_card,
                                 botao_consulta_checklist,
                                 botao_consulta_lista)

st.title("Consulta do Trello")
abas = st.tabs(["Board", "Lists", "Cards", "CheckLists"])# Criando as abas
# Inicializa valores em session_state, se não estiverem definidos
if 'board_name_result' not in st.session_state:
    st.session_state.board_name_result = None
if 'id_board_result' not in st.session_state:
    st.session_state.id_board_result = None
if 'card_name_result' not in st.session_state:
    st.session_state.card_name_result = None
if 'checklist_name_result' not in st.session_state:
    st.session_state.checklist_name_result = None

with abas[0]:# Primeira aba: Consulta de Boards
    st.header("Consulta do Board")
    consulta_tipo = st.radio("Selecione o tipo de consulta:", ("Nome", "ID"))
    if consulta_tipo == "Nome":
        board_name = st.text_input("Digite o Nome do Board:")
        if st.button("Consultar Board"):
            if board_name:
                try:
                    res = botao_consulta_board_id(board_name)
                    if res:
                        st.session_state.board_name_result = f"Id do board: {res}"
                        st.success(st.session_state.board_name_result)
                    else:
                        st.error(f"Erro: {res}")
                except Exception as e:
                    st.error(f"Erro na consulta: {e}")    
            else:
                st.warning("Por favor, digite um nome antes de cadastrar.")
        if (st.session_state.board_name_result) and not (board_name):# Exibe o resultado anterior da consulta, se houver
            st.success(st.session_state.board_name_result)
    elif consulta_tipo == "ID":
        id_org = st.text_input("Digite o ID da Organização:")
        if st.button("Consultar Board"):
            if id_org:
                try:
                    res = botao_consulta_board(id_org)
                    if "id" in res:
                        st.session_state.board_name_result = f"Nome do board: {res}"
                        st.success(st.session_state.board_name_result)
                    else:
                        st.error(f"Erro: {res}")
                except Exception as e:
                    st.error(f"Erro na consulta: {e}")    
            else:
                st.warning("Por favor, digite um nome antes de cadastrar.")
        if (st.session_state.board_name_result) and not (id_org):# Exibe o resultado anterior da consulta, se houver
            st.success(st.session_state.board_name_result)

with abas[1]:# Consulta de listas
    st.header("Consulta de Listas")
    id_board = st.text_input("Digite o ID do Board:")
    if st.button("Consultar Listas"):
        if id_board:
            try:
                res = botao_consulta_lista(id_board)
                if "id" in res[0]:
                    st.session_state.id_board_result = f"Nome da Lista: {res}"
                    st.success(st.session_state.id_board_result)
                else:
                    st.error(f"Erro: {res}")
            except Exception as e:
                st.error(f"Erro na consulta: {e}")    
        else:
            st.warning("Por favor, digite um nome antes de cadastrar.")
    if (st.session_state.id_board_result) and not (id_board):# Exibe o resultado anterior da consulta, se houver
        st.success(st.session_state.id_board_result)

with abas[2]:# Consulta de Cards
    st.header("Consulta de Cards")
    id_lista = st.text_input("Digite o ID da Lista:")
    if st.button("Consultar Card"):
        if id_lista:
            try:
                res = botao_consulta_card(id_lista)
                if "id" in res[0]:
                    st.session_state.card_name_result = f"Card: {res}"
                    st.success(st.session_state.card_name_result)
                else:
                    st.error(f"Erro: {res}")
            except Exception as e:
                st.error(f"Erro na consulta: {e}")    
        else:
            st.warning("Por favor, digite um nome antes de cadastrar.")
    if (st.session_state.card_name_result) and not (id_lista):# Exibe o resultado anterior da consulta, se houver
        st.success(st.session_state.card_name_result)

with abas[3]:# Consulta de CheckLists
    st.header("Consulta de CheckLists")
    id_card = st.text_input("Digite o ID do Card:")
    if st.button("Consultar CheckLists"):
        if id_card:
            try:
                res = botao_consulta_checklist(id_card)
                if "id" in res[0]:
                    st.session_state.checklist_name_result = f"CheckLists: {res}"
                    st.success(st.session_state.checklist_name_result)
                else:
                    st.error(f"Erro: {res}")
            except Exception as e:
                st.error(f"Erro na consulta: {e}")    
        else:
            st.warning("Por favor, digite um nome antes de cadastrar.")
    if (st.session_state.checklist_name_result) and not (id_card):# Exibe o resultado anterior da consulta, se houver
        st.success(st.session_state.checklist_name_result)
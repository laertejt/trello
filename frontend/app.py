import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent# Definindo os diretórios base
sys.path.append(str(BASE_DIR))
import setup_paths
import streamlit as st
from frontend.conta.login import login
from frontend.conta.logout import logout
# Colocar o status do Login/out
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
#Inicio da configuração dos menus
login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
cadastro_page = st.Page("principal/cadastro.py", title="Cadastro", icon=":material/forms_add_on:", default=True)
consulta_page = st.Page("principal/consulta.py", title="Consulta", icon=":material/manage_search:")
frequencia_page = st.Page("relatorio/frequencia.py", title="Gráfico de Frequencia", icon=":material/bar_chart:")
if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Conta": [logout_page],
            "Principal": [cadastro_page, consulta_page],
            "Relatório": [frequencia_page],
        }
    )
else:
    pg = st.navigation([login_page])
pg.run()
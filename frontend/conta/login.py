import streamlit as st

def login():
    if st.button("Log in"):
        st.session_state.logged_in = True
        st.rerun()
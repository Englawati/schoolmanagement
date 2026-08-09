import streamlit as st


def init_session_state():

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "user" not in st.session_state:
        st.session_state.user = None

    if "role" not in st.session_state:
        st.session_state.role = None


def login_session(user):

    st.session_state.authenticated = True
    st.session_state.user = user
    st.session_state.role = user.get("role")


def clear_session():

    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.role = None
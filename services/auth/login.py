import streamlit as st
from services.persistence.exercise_repository import get_or_create_user


st.set_page_config(
    page_title="AI Gym Assistant",
    page_icon="", 
    layout="wide")


def render_login_page():
    if st.session_state.get("user_id") is not None:
        st.success("You are already logged in.")
        return True
    st.title("AI Gym Assistant")
    st.markdown("### Please log in to access the AI Gym Assistant.")
    st.markdown("Please enter your credentials to log in.")

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username")
        submit_button = st.form_submit_button("Login")


    if submit_button:
     
        if not username:
            st.error("Please enter a Unique username.")
            return False
        
        else:
            user = get_or_create_user(username)
            st.session_state["user_id"] = user["id"]
            st.session_state["username"] = user["username"]
            st.success("Login successful!")
            return True
        
    return False
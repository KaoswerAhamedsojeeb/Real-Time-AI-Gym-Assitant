import streamlit as st
st.set_page_config(
    page_title="AI Gym Assistant",
    page_icon="", 
    layout="wide")


def render_login_page():
    if st.session_state.get("user_id") is not None:
        st.success("You are already logged in.")
        return True
    st.title("AI Gym Assistant - Login")
    st.markdown("### please enter your credentials to log in.")

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")


    if submit_button:
     
        if not username:
            st.error("Please enter a username.")
            return False
        elif not password:
            st.error("Please enter a password.")
            return False

        elif username == "admin" and password == "password":
            st.session_state["user_id"] = 1
            st.session_state["username"] = username
            st.success("Login successful!")
            return True
        else:
            st.session_state["user_id"] = 1
            st.session_state["username"] = username
            st.success("Login successful!")
            return True
     
        
    st.rerun()
    return False
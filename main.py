import streamlit as st
from services.auth.login import render_login_page


def main():
    st.set_page_config(
        page_title="AI Gym Assistant",
        page_icon="", 
        layout="wide")

    if not render_login_page():
        
        return
    
    st.write("Welcome to the AI Gym Assistant!")

if __name__ == "__main__":
    main()
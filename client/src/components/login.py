import streamlit as st
from src.services.auth import AuthClient
from src.services.graphql_client import GraphQLClient
from src.services.api_client import RESTAPIClient

def login_page():
    """Login page interface"""

    st.markdown("<h1>Forum Login</h1>", unsafe_allow_html=True)
    
    username = st.text_input("Username", key="login_username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
    
    if st.button("Login"):
        # Initialize authentication clients
        auth_client = AuthClient()
        if auth_client.login(username, password):
            # Store clients in session state
            st.session_state.auth_client = auth_client
            st.session_state.graphql_client = GraphQLClient(auth_client=auth_client)
            st.session_state.api_client = RESTAPIClient(auth_client=auth_client)
            
            # Update page state
            st.session_state.page = 'dashboard'
            st.rerun()  # Force rerun to navigate to the dashboard
        else:
            st.error("Invalid login credentials")
    
    st.markdown("<div class='register-link'>New User? <span>Register Here</span></div>", unsafe_allow_html=True)
    if st.button("Register"):
        st.session_state.page = 'register'
        st.rerun()  # Force rerun to navigate to the register page
    st.markdown("</div>", unsafe_allow_html=True)
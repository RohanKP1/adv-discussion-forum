import streamlit as st
import time
from src.services.api_client import RESTAPIClient

def register_page():
    """User registration page"""
    # Custom CSS for modern styling

    st.title("Create New Account")
    
    st.markdown("### Fill in the details below to register:")
    
    username = st.text_input("Choose Username")
    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    st.markdown("---")
    
    reg_col1, reg_col2 = st.columns(2)
    
    with reg_col1:
        if st.button("Register"):
            if password != confirm_password:
                st.error("❌ Passwords do not match")
            elif not (username and email and password):
                st.error("❌ Please fill all fields")
            else:
                # Use REST API client for registration
                rest_client = RESTAPIClient()
                result = rest_client.register_user(username, email, password)
                
                if result:
                    st.success("Registration successful! Please login.")
                    time.sleep(2)
                    st.session_state.page = 'login'
                    st.rerun()  # Force rerun to navigate to the login page
                else:
                    st.error("❌ Registration failed")
    
    with reg_col2:
        if st.button("Back to Login"):
            st.session_state.page = 'login'
            st.rerun()  # Force rerun to navigate to the login page
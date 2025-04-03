import streamlit as st
from src.components.pages.home_page import home_page
from src.components.pages.notifications import notifications
from src.components.pages.create_topic import create_topic
from src.components.pages.search_topics import search_topics
from src.components.pages.user_profile import user_profile
from src.components.pages.content_hub import content_hub

def dashboard_page():
    """Main dashboard with topics and interactions"""

    # Sidebar for navigation
    with st.sidebar:
        st.title(f"Welcome, {st.session_state.auth_client.user_data.get('username', 'User')}")
        st.header("Navigation")
        nav_option = st.radio("Go to", ["Home", "Search Topics", "Create Topic", "Content Hub", "My Profile", "Notifications"])
        
        if st.button("Logout", use_container_width=True):
            st.session_state.auth_client.logout()
            st.session_state.page = 'login'
            st.rerun()  # Force rerun to navigate to the login page
    
    # Main content based on navigation
    if nav_option == "Home":
        home_page()
    elif nav_option == "Search Topics":
        search_topics()
    elif nav_option == "Create Topic":
        create_topic()
    elif nav_option == "Content Hub":
        content_hub()
    elif nav_option == "My Profile":
        user_profile()
    elif nav_option == "Notifications":
        notifications()
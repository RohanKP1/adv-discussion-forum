import streamlit as st
from src.components.login import login_page
from src.components.register import register_page
from src.components.dashboard import dashboard_page

# Set Streamlit page configuration
st.set_page_config(page_title="Forum App", page_icon="💬")

class ForumApp:
    def __init__(self):
        """Initialize session state variables."""
        self.initialize_session_state()

    def initialize_session_state(self):
        """Ensure required session state variables are initialized."""
        if 'page' not in st.session_state:
            st.session_state.page = 'login'

    def run(self):
        """Main application run method with routing logic."""
        # Route to the appropriate page based on session state
        if st.session_state.page == 'login':
            login_page()
        elif st.session_state.page == 'register':
            register_page()
        elif st.session_state.page == 'dashboard':
            dashboard_page()
        else:
            # Default to login page if an invalid state is encountered
            st.session_state.page = 'login'
            login_page()

def main():
    """Entry point for the application."""
    app = ForumApp()
    app.run()

if __name__ == "__main__":
    main()
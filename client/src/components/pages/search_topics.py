from datetime import datetime
import streamlit as st
from src.components.pages.display_comments import display_comments

def search_topics():
    """Search for topics by title or content"""
    st.header("Search Topics")
    st.markdown("---")  # Add a horizontal line for separation

    # Search input
    if "search_query" not in st.session_state:
        st.session_state.search_query = ""
    search_query = st.text_input("Search for topics", placeholder="Enter keywords to search...", value=st.session_state.search_query)

    if search_query:
        # Perform search using GraphQL client
        search_results = st.session_state.graphql_client.search_topics(search_query)

        if search_results:
            st.subheader(f"Search Results for '{search_query}'")
            for topic in search_results:
                author_name = st.session_state.graphql_client.hello(user_id=topic['userId'])
                with st.container():
                    st.markdown("---")
                    st.markdown(f"### {topic['title']}")
                    st.markdown(f"**Description:** {topic['content']}")
                    created_at = datetime.strptime(topic['createdAt'], "%Y-%m-%dT%H:%M:%S.%f")
                    formatted_created_at = created_at.strftime("%B %d, %Y at %I:%M %p")
                    st.markdown(f"**Author:** {author_name} | **Created At:** {formatted_created_at}")

                    display_comments(topic['id'], key=f"search_{topic['id']}_", is_locked=topic['isLocked'])

        else:
            st.warning(f"No topics found for '{search_query}'")
    else:
        st.info("Enter a keyword to search for topics.")
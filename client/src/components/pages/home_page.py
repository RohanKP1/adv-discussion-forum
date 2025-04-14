import streamlit as st
from src.components.pages.display_comments import display_comments
from datetime import datetime

def home_page():
    """Display home page with trending topics and all topics"""

    # Trending Topics Section
    st.header("Trending Topics")
    trending_topics = st.session_state.graphql_client.get_trending_topics()
    if trending_topics:
        for topic in trending_topics[:3]:  # Show only the first 3 trending topics
            author_name = st.session_state.graphql_client.hello(user_id=topic['userId'])
            with st.container():
                st.markdown("---")
                st.markdown("### " + topic['title'])
                st.markdown(f"**Description:** {topic['content']}")
                try:
                    created_at = datetime.strptime(topic['createdAt'], "%Y-%m-%dT%H:%M:%S.%f")
                    formatted_created_at = created_at.strftime("%B %d, %Y at %I:%M %p")
                except ValueError:
                    # Handle the case where the date format doesn't match
                    formatted_created_at = topic['createdAt']    
                st.markdown(f"**Author:** {author_name} | **Created At:** {formatted_created_at}")

                # Display comments under the topic
                display_comments(topic['id'], key=f"trending_{topic['id']}_", is_locked=topic['isLocked'])
    else:
        st.info("No trending topics found.")

    st.markdown("---")

    # All Topics Section
    st.header("All Topics")
    all_topics = st.session_state.graphql_client.get_all_topics()

    if all_topics:
        topics_to_display = 4  # Number of topics to show by default
        if "all_topics_limit" not in st.session_state:
            st.session_state.all_topics_limit = topics_to_display

        for topic in all_topics[:st.session_state.all_topics_limit]:  # Show limited topics
            author_name = st.session_state.graphql_client.hello(user_id=topic['userId'])
            with st.container():
                st.markdown("### " + topic['title'])
                st.markdown(f"**Description:** {topic['content']}")
                try:
                    created_at = datetime.strptime(topic['createdAt'], "%Y-%m-%d %H:%M:%S.%f")
                    formatted_created_at = created_at.strftime("%B %d, %Y at %I:%M %p")
                except ValueError:
                    formatted_created_at = topic['createdAt']
                st.markdown(f"**Author:** {author_name} | **Created At:** {formatted_created_at}")

                # Display comments under the topic
                display_comments(topic['id'], key=f"all_{topic['id']}_", is_locked=topic['isLocked'])

                st.markdown("---")

        if st.session_state.all_topics_limit < len(all_topics):
            if st.button("Show More Topics"):
                st.session_state.all_topics_limit += topics_to_display
    else:
        st.info("No topics found.")

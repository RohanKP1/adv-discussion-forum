from datetime import datetime
import streamlit as st

def display_comments(topic_id, key, is_locked=False):
    """Display comments for a specific topic with an expander and add comment functionality"""
    # Fetch comments for the topic
    comments = st.session_state.graphql_client.get_comments_by_topic_id(topic_id)

    # Expander to show comments and add new comment
    with st.expander("View Comments"):
        # Check if the topic is locked
        if is_locked:
            st.error("This topic is locked. You cannot add new comments.")
        else:    
            if comments:
                for comment in comments:
                    user_name = st.session_state.graphql_client.hello(user_id=comment['userId'])
                    created_at = datetime.strptime(comment['createdAt'], "%Y-%m-%d %H:%M:%S.%f")
                    formatted_created_at = created_at.strftime("%B %d, %Y at %I:%M %p")
                    st.markdown(f"- **{comment['content']}** (by {user_name} on {formatted_created_at})")
            else:
                st.info("No comments yet. Be the first to comment!")

            # Add comment functionality under the expander
            new_comment = st.text_area("Add your comment:", key=f"{key}_{topic_id}")
            if st.button("Submit Comment", key=f"submit_{key}_{topic_id}"):
                new_comment = new_comment.strip()
                if new_comment:
                    st.session_state.graphql_client.create_comment(topic_id, new_comment)
                    st.success("Comment added successfully!")
                else:
                    st.warning("Comment cannot be empty.")

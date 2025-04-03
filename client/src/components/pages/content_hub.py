from datetime import datetime
import streamlit as st
from src.components.pages.display_comments import display_comments

def content_hub():
    """Display and manage topics and comments created by the logged-in user"""
    st.header("Your Topics")
    st.markdown("---")  # Add a horizontal line for separation

    # Fetch topics created by the user
    user_topics = st.session_state.graphql_client.get_topics_by_user()

    if user_topics:
        for topic in user_topics:
            with st.container():
                st.markdown("### " + topic['title'])
                st.markdown(f"**Description:** {topic['content']}")
                created_at = datetime.strptime(topic['createdAt'], "%Y-%m-%d %H:%M:%S.%f")
                formatted_created_at = created_at.strftime("%B %d, %Y at %I:%M %p")
                st.markdown(f"**Created At:** {formatted_created_at}")

                # Display comments under the topic
                display_comments(topic['id'], key=f"all_{topic['id']}_", is_locked=topic['isLocked'])

                # Use an expander for editing the topic
                with st.expander(f"Edit Topic"):
                    with st.form(key=f"edit_form_{topic['id']}"):
                        new_title = st.text_input("Edit Title", value=topic['title'])
                        new_content = st.text_area("Edit Description", value=topic['content'])
                        submit_button = st.form_submit_button("Update")

                        if submit_button:
                            result = st.session_state.graphql_client.update_topic(
                                topic_id=topic['id'],
                                title=new_title,
                                content=new_content
                            )
                            if result:
                                st.success(f"Topic '{new_title}' updated successfully!")
                                st.rerun()  # Refresh the page to update the list of topics
                            else:
                                st.error(f"Failed to update topic '{topic['title']}'.")

                # Add a delete button for each topic
                if st.button(f"Delete Topic", key=f"delete_{topic['id']}"):
                    result = st.session_state.graphql_client.delete_topic(topic['id'])
                    if result:
                        st.success(f"Topic '{topic['title']}' deleted successfully!")
                        st.rerun()  # Refresh the page to update the list of topics
                    else:
                        st.error(f"Failed to delete topic '{topic['title']}'.")

                st.markdown("---")
    else:
        st.info("You haven't created any topics yet.")

    # Section for managing user-created comments
    st.header("Your Comments")
    st.markdown("---")

    # Fetch comments created by the user
    user_id = st.session_state.auth_client.user_data.get("id")
    user_comments = st.session_state.graphql_client.get_comments_by_user_id(user_id)

    if user_comments:
        for comment in user_comments:
            with st.container():
                st.markdown(f"**Comment:** {comment['content']}")
                created_at = datetime.strptime(comment['createdAt'], "%Y-%m-%d %H:%M:%S.%f")
                formatted_created_at = created_at.strftime("%B %d, %Y at %I:%M %p")
                st.markdown(f"**Created At:** {formatted_created_at}")
                st.markdown(f"**Topic ID:** {comment['topicId']}")

                # Use an expander for editing the comment
                with st.expander(f"Edit Comment"):
                    with st.form(key=f"edit_comment_form_{comment['id']}"):
                        new_comment_content = st.text_area("Edit Comment", value=comment['content'])
                        submit_button = st.form_submit_button("Update Comment")

                        if submit_button:
                            result = st.session_state.graphql_client.update_comment(
                                comment_id=comment['id'],
                                content=new_comment_content
                            )
                            if result:
                                st.success("Comment updated successfully!")
                                st.rerun()  # Refresh the page to update the list of comments
                            else:
                                st.error("Failed to update comment.")

                # Add a delete button for each comment
                if st.button(f"Delete Comment", key=f"delete_comment_{comment['id']}"):
                    result = st.session_state.graphql_client.delete_comment(comment['id'])
                    if result:
                        st.success("Comment deleted successfully!")
                        st.rerun()  # Refresh the page to update the list of comments
                    else:
                        st.error("Failed to delete comment.")

                st.markdown("---")
    else:
        st.info("You haven't created any comments yet.")

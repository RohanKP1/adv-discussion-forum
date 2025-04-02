from datetime import datetime
import streamlit as st
from src.components.pages.display_comments import display_comments

def display_user_topics():
    """Display and manage topics created by the logged-in user"""
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

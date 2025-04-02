import streamlit as st

def create_topic():
    """Create a new topic"""
    st.header("Create New Topic")
    st.markdown("---")  # Add a horizontal line for separation

    title = st.text_input("Topic Title", placeholder="Enter the topic title")
    content = st.text_area("Topic Content", placeholder="Write the content here...")
    is_locked = st.checkbox("Lock Topic")

    if st.button("Submit Topic", use_container_width=True):
        if title and content:
            result = st.session_state.graphql_client.create_topic(
                title, content, is_locked
            )
            if result:
                st.session_state.topic_created = True  # Set the success flag
                st.rerun()
            else:
                st.error("Failed to create topic")
        else:
            st.warning("Please fill all fields")

    # Display success message at the bottom
    if "topic_created" in st.session_state and st.session_state.topic_created:
        st.success("Topic created successfully!")
        st.session_state.topic_created = False  # Reset the flag
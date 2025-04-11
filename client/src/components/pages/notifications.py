import streamlit as st

def notifications():
    """Display user notifications"""
    st.header("Notifications")
    st.markdown("---")  # Add a horizontal line for separation

    # Query GraphQL for notifications
    notifications = st.session_state.graphql_client.get_user_notifications()

    if notifications:
        # Add a toggle to switch between "Unread" and "Read" notifications
        view_option = st.radio("View Notifications:", ["Unread", "Read"], horizontal=True)

        if view_option == "Unread":
            filtered_notifications = [n for n in notifications if not n['isRead']]
        else:
            filtered_notifications = [n for n in notifications if n['isRead']]

        if filtered_notifications:
            # Initialize session state for pagination
            if "notification_limit" not in st.session_state:
                st.session_state.notification_limit = 5

            # Display notifications up to the current limit
            for notification in filtered_notifications[:st.session_state.notification_limit]:
                st.info(f"{notification['content']} at {notification['createdAt']}")

            # Show "Show More" button if there are more notifications to display
            if len(filtered_notifications) > st.session_state.notification_limit:
                if st.button("Show More", use_container_width=True):
                    st.session_state.notification_limit += 5
                    st.rerun()  # Refresh the page to load more notifications

            if view_option == "Unread":
                # Add a button to clear notifications
                if st.button("Clear Notifications", use_container_width=True):
                    result = st.session_state.graphql_client.mark_all_notifications_read()
                    if result:
                        st.success("All notifications cleared!")
                        st.rerun()  # Refresh the page to update the notifications list
                    else:
                        st.error("Failed to clear notifications")
        else:
            st.success(f"No {view_option.lower()} notifications")
    else:
        st.success("No new notifications")
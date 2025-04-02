import streamlit as st
def user_profile():
    """Display and edit user profile"""
    st.header("My Profile")
    st.markdown("---")  # Add a horizontal line for separation

    # Fetch user profile
    profile = st.session_state.api_client.get_user_profile()

    if profile:
        avatar_url = profile.get('avatar_url')
        col1, col2 = st.columns([1, 3])
        with col1:
            if avatar_url:
                st.image(avatar_url, caption="Avatar", width=150)
        with col2:
            st.markdown(f"**Username:** {profile.get('username')}")
            st.markdown(f"**Email:** {profile.get('email')}")
            st.markdown(f"**Bio:** {profile.get('bio')}")

        # Edit user details
        st.markdown("### Edit Profile")
        new_username = st.text_input("Username", value=profile.get('username'))
        new_email = st.text_input("Email", value=profile.get('email'))
        new_bio = st.text_area("Bio", value=profile.get('bio'))
        new_avatar_url = st.text_input("Avatar URL", value=avatar_url)

        if st.button("Save Changes"):
            updated_profile = {
                "username": new_username,
                "email": new_email,
                "bio": new_bio,
                "avatar_url": new_avatar_url
            }
            success = st.session_state.api_client.update_user_profile(updated_profile)
            if success:
                st.success("Profile updated successfully!")
            else:
                st.error("Failed to update profile.")

        # Change password section
        st.markdown("### Change Password")
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")

        if st.button("Change Password"):
            if new_password != confirm_password:
                st.error("New password and confirmation do not match.")
            else:
                success = st.session_state.api_client.change_password(
                    current_password, new_password
                )
                if success:
                    st.success("Password changed successfully!")
                else:
                    st.error("Failed to change password. Please check your current password.")
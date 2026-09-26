import streamlit as st
from app.ui.components import page_header, section_header
from app.core.firestore import get_document, update_document, create_document

def render():
    page_header(
        eyebrow="SYSTEM",
        title="Settings",
        description="Manage your account, organization, and application preferences."
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("""
            <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                <div style="padding: 1rem; background-color: var(--ep-surface-2); border-left: 3px solid var(--ep-accent); font-weight: 500; cursor: pointer;">Profile</div>
                <div style="padding: 1rem; color: var(--ep-muted); cursor: pointer;">Organization</div>
                <div style="padding: 1rem; color: var(--ep-muted); cursor: pointer;">Notifications</div>
                <div style="padding: 1rem; color: var(--ep-muted); cursor: pointer;">API Keys</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        user = st.session_state.user
        uid = user["uid"]
        id_token = user["id_token"]
        collection_path = f"users/{uid}/settings"

        # Load settings
        if 'settings_loaded' not in st.session_state:
            try:
                prefs = get_document(id_token, collection_path, "preferences")
                if prefs:
                    st.session_state['user_preferences'] = prefs
                else:
                    st.session_state['user_preferences'] = {}
                st.session_state['settings_loaded'] = True
            except Exception:
                st.session_state['user_preferences'] = {}

        prefs = st.session_state.get('user_preferences', {})

        st.markdown('<div class="ep-card">', unsafe_allow_html=True)
        st.markdown('<div class="ep-card-header" style="margin-bottom: 1.5rem;">Profile Settings</div>', unsafe_allow_html=True)

        new_name = st.text_input("Full Name", value=prefs.get("fullName", user.get("display_name", "")))
        st.text_input("Email Address", value=user.get("email", ""), disabled=True)
        new_company = st.text_input("Company Name", value=prefs.get("companyName", ""))

        report_email = st.text_input("Report Email Destination", value=prefs.get("reportEmail", user.get("email", "")))

        st.write("")
        if st.button("Save Changes", type="primary"):
            updates = {
                "fullName": new_name,
                "companyName": new_company,
                "reportEmail": report_email
            }
            try:
                # If document exists, update. Otherwise create.
                # Since get_document doesn't easily distinguish between "no collection" and "no doc",
                # we'll just try to create_document first (which will overwrite) or use update.
                create_document(id_token, collection_path, "preferences", updates)
                st.session_state['user_preferences'].update(updates)
                st.success("Settings saved successfully!")
            except Exception as e:
                st.error(f"Failed to save settings: {str(e)}")

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="ep-card" style="margin-top: 2rem;">', unsafe_allow_html=True)
        st.markdown('<div class="ep-card-header" style="margin-bottom: 1.5rem; color: var(--ep-error);">Danger Zone</div>', unsafe_allow_html=True)
        st.markdown('<p style="color: var(--ep-muted); font-size: 0.9rem;">Once you delete your account, there is no going back. Please be certain.</p>', unsafe_allow_html=True)
        st.button("Delete Account")
        st.markdown('</div>', unsafe_allow_html=True)

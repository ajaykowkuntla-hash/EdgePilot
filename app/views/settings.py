import streamlit as st
from app.ui.components import page_header, section_header

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
        st.markdown('<div class="ep-card">', unsafe_allow_html=True)
        
        st.markdown('<div class="ep-card-header" style="margin-bottom: 1.5rem;">Profile Settings</div>', unsafe_allow_html=True)
        
        st.text_input("Full Name", value="Admin User")
        st.text_input("Email Address", value="admin@example.com", disabled=True)
        st.text_input("Role", value="System Administrator", disabled=True)
        
        st.write("")
        st.button("Save Changes", type="primary")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="ep-card" style="margin-top: 2rem;">', unsafe_allow_html=True)
        st.markdown('<div class="ep-card-header" style="margin-bottom: 1.5rem; color: var(--ep-error);">Danger Zone</div>', unsafe_allow_html=True)
        st.markdown('<p style="color: var(--ep-muted); font-size: 0.9rem;">Once you delete your account, there is no going back. Please be certain.</p>', unsafe_allow_html=True)
        st.button("Delete Account")
        st.markdown('</div>', unsafe_allow_html=True)

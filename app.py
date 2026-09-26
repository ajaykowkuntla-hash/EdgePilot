import streamlit as st
import time

# Configure the Streamlit page
st.set_page_config(
    page_title="EdgePilot",
    page_icon="✈️",
    layout="wide"
)

from app.ui.styles import apply_global_styles
apply_global_styles()

from app.core.auth import exchange_google_code_for_firebase_token
from app.views import login

# Initialize session state for auth and navigation
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if 'user' not in st.session_state:
    st.session_state['user'] = None

if 'current_view' not in st.session_state:
    st.session_state['current_view'] = 'Dashboard'

def set_view(view_name):
    st.session_state['current_view'] = view_name

# Check for Google OAuth code in query params
if not st.session_state['authenticated']:
    query_params = st.query_params
    if 'code' in query_params:
        code = query_params['code']
        # Clear query params to prevent re-triggering
        st.query_params.clear()

        try:
            with st.spinner("Authenticating with Google..."):
                fb_result = exchange_google_code_for_firebase_token(code)
                st.session_state['authenticated'] = True
                st.session_state['user'] = {
                    "uid": fb_result["localId"],
                    "email": fb_result.get("email", ""),
                    "display_name": fb_result.get("displayName", ""),
                    "photo_url": fb_result.get("photoUrl", ""),
                    "id_token": fb_result["idToken"],
                    "refresh_token": fb_result["refreshToken"]
                }
            st.rerun()
        except Exception as e:
            st.error(f"Google Authentication failed: {str(e)}")

# Auth gate
if not st.session_state['authenticated'] or not st.session_state['user']:
    login.render()
    st.stop()

# Only import protected views after authentication is confirmed
from app.views import dashboard, inspection, dataset, model, inference, reports, task_detail, settings, live_inspection

# Define the navigation structure
VIEWS = {
    "Dashboard": dashboard.render,
    "Inspections": inspection.render,
    "Live Inspection": live_inspection.render,
    "Reports": reports.render,
    "Settings": settings.render,

    # Internal mappings
    "Task Detail": task_detail.render,
    "Inference": inference.render,
    "Dataset": dataset.render,
    "Model": model.render
}

# Sidebar Navigation
with st.sidebar:
    st.markdown('<div style="font-weight: 800; font-size: 1.5rem; letter-spacing: -0.05em; color: var(--ep-text); margin-bottom: 0.25rem;">EDGE PILOT</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: var(--ep-muted); font-size: 0.8rem; margin-bottom: 2rem;">Business Automation</div>', unsafe_allow_html=True)

    st.markdown('<div style="font-size: 0.75rem; font-weight: 600; color: var(--ep-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; margin-top: 1rem;">Main</div>', unsafe_allow_html=True)
    for view_name in ["Dashboard", "Inspections", "Live Inspection", "Reports"]:
        if st.button(view_name, use_container_width=True,
                     type="primary" if st.session_state['current_view'] == view_name else "secondary"):
            set_view(view_name)
            st.rerun()

    st.markdown('<div style="font-size: 0.75rem; font-weight: 600; color: var(--ep-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; margin-top: 2rem;">System</div>', unsafe_allow_html=True)
    for view_name in ["Settings"]:
        if st.button(view_name, use_container_width=True,
                     type="primary" if st.session_state['current_view'] == view_name else "secondary"):
            set_view(view_name)
            st.rerun()

    if st.button("Help", use_container_width=True, type="secondary"):
        st.info("Documentation coming soon.")

    if st.button("Sign Out", use_container_width=True, type="secondary"):
        st.session_state['authenticated'] = False
        st.session_state['user'] = None
        st.session_state['current_view'] = 'Dashboard'
        st.rerun()

    # User profile section
    user_email = st.session_state.user.get('email', 'User')
    display_name = st.session_state.user.get('display_name', '')

    name_display = display_name if display_name else user_email.split('@')[0]

    st.markdown(f"""
        <div style="margin-top: auto; padding-top: 4rem; border-top: 1px solid var(--ep-border); margin-top: 2rem;">
            <div style="font-size: 0.75rem; font-weight: 600; color: var(--ep-text); margin-bottom: 0.25rem;">{name_display}</div>
            <div style="font-size: 0.7rem; color: var(--ep-muted); word-break: break-all;">{user_email}</div>
        </div>
    """, unsafe_allow_html=True)

# Render the active view
active_view = st.session_state['current_view']
if active_view in VIEWS:
    VIEWS[active_view]()
else:
    # Handle older state names if any
    if 'Dashboard' in active_view: VIEWS['Dashboard']()
    elif 'Inspection' in active_view: VIEWS['Inspections']()
    else: VIEWS['Dashboard']()

import streamlit as st

# Configure the Streamlit page
st.set_page_config(
    page_title="EdgePilot",
    page_icon="✈️",
    layout="wide"
)

from app.ui.styles import apply_global_styles
apply_global_styles()

# Import the views
from app.views import dashboard, inspection, dataset, model, inference, performance, task_detail, evidence

# Initialize session state for navigation if not exists
if 'current_view' not in st.session_state:
    st.session_state['current_view'] = '⌂ Dashboard'

def set_view(view_name):
    st.session_state['current_view'] = view_name

# Define the navigation structure
VIEWS = {
    "⌂ Dashboard": dashboard.render,
    "＋ Create Inspection": inspection.render,
    "▣ Validated Tasks": dashboard.render, # Maps to Dashboard where tasks are listed
    "Task Detail": task_detail.render, # Hidden from sidebar, accessible via buttons
    "◉ Inference": inference.render,
    "⌁ Performance": performance.render,
    "✓ Evidence": evidence.render,

    # Internal mappings
    "Dataset": dataset.render,
    "Model": model.render
}

# Sidebar Navigation
with st.sidebar:
    st.markdown('<div style="font-weight: 800; font-size: 1.5rem; letter-spacing: -0.05em; color: var(--ep-text); margin-bottom: 0.25rem;">EDGE PILOT</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: var(--ep-muted); font-size: 0.8rem; margin-bottom: 2rem;">AI Automation, Built for the Edge.</div>', unsafe_allow_html=True)

    for view_name in ["⌂ Dashboard", "＋ Create Inspection", "▣ Validated Tasks", "◉ Inference", "⌁ Performance", "✓ Evidence"]:
        if st.button(view_name, use_container_width=True,
                     type="primary" if st.session_state['current_view'] == view_name else "secondary"):
            set_view(view_name)
            st.rerun()

    st.markdown("""
        <div style="margin-top: auto; padding-top: 4rem; border-top: 1px solid var(--ep-border); margin-top: 2rem;">
            <div style="font-family: var(--ep-mono); font-size: 0.7rem; color: var(--ep-muted); letter-spacing: 0.05em; margin-bottom: 0.25rem;">EDGE PILOT MVP</div>
            <div style="font-family: var(--ep-mono); font-size: 0.7rem; color: var(--ep-accent); letter-spacing: 0.05em; font-weight: 600;">QUALCOMM AI HUB VALIDATED</div>
        </div>
    """, unsafe_allow_html=True)

# Render the active view
active_view = st.session_state['current_view']
if active_view in VIEWS:
    VIEWS[active_view]()
else:
    # Handle older state names if any
    if active_view == 'Dashboard': VIEWS['⌂ Dashboard']()
    elif active_view == 'Create AI Inspection': VIEWS['＋ Create Inspection']()
    elif active_view == 'Validated Tasks': VIEWS['▣ Validated Tasks']()
    else: st.error(f"View {active_view} not found.")

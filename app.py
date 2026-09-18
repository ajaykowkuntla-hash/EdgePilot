import streamlit as st

# Configure the Streamlit page
st.set_page_config(
    page_title="EdgePilot",
    page_icon="✈️",
    layout="wide"
)

# Import the views
from app.views import dashboard, inspection, dataset, model, inference, performance, task_detail

# Initialize session state for navigation if not exists
if 'current_view' not in st.session_state:
    st.session_state['current_view'] = 'Dashboard'

def set_view(view_name):
    st.session_state['current_view'] = view_name

# Define the navigation structure
VIEWS = {
    "Dashboard": dashboard.render,
    "Create AI Inspection": inspection.render,
    "Validated Tasks": dashboard.render, # Maps to Dashboard where tasks are listed
    "Task Detail": task_detail.render, # Hidden from sidebar, accessible via buttons
    "Inference": inference.render,
    "Performance": performance.render,
    "Dataset": dataset.render,
    "Model": model.render
}

# Sidebar Navigation
with st.sidebar:
    st.title("EdgePilot")
    st.caption("A Configurable Edge-AI Automation Platform for MSMEs")
    st.markdown("---")
    
    for view_name in VIEWS.keys():
        if view_name == "Task Detail":
            continue
            
        if st.button(view_name, use_container_width=True, 
                     type="primary" if st.session_state['current_view'] == view_name else "secondary"):
            set_view(view_name)
            st.rerun()

    st.markdown("---")
    st.caption("AI Automation, Built for the Edge.")

# Render the active view
active_view = st.session_state['current_view']
if active_view in VIEWS:
    VIEWS[active_view]()
else:
    st.error("View not found.")

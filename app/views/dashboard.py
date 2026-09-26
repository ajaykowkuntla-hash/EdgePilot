import streamlit as st
from app.ui.components import metric_card, section_header

def render():
    st.markdown("""
        <div style="margin-bottom: 2rem;">
            <h1 style="font-size: 2.5rem; font-weight: 800; margin: 0; padding: 0; color: var(--ep-text);">Good morning</h1>
            <p style="color: var(--ep-muted); font-size: 1.1rem; margin-top: 0.5rem;">Here's today's inspection summary.</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("ITEMS INSPECTED", "0")
    with col2:
        metric_card("PASSED", "0")
    with col3:
        metric_card("ISSUES FOUND", "0")
    with col4:
        metric_card("AVG PROCESSING TIME", "0.0 sec")

    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

    col_cta1, col_cta2, col_cta3 = st.columns([1, 1, 2])
    with col_cta1:
        if st.button("＋ Start Inspection", type="primary", use_container_width=True):
            st.session_state['current_view'] = 'Inspections'
            st.session_state['wizard_step'] = 1
            st.rerun()

    st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)

    section_header("Deployment Candidate")

    st.markdown("""
        <div class="ep-card" style="padding: 1.5rem; border-left: 4px solid var(--ep-primary); margin-bottom: 2rem;">
            <h3 style="margin-top: 0;">PRODUCT DEFECT INSPECTION</h3>
            <p><strong>Model:</strong> YOLOv8-N</p>
            <p><strong>Validation:</strong> More examples recommended</p>
            <p><strong>Snapdragon:</strong> NPU validated</p>
            <p><strong>Latency:</strong> 5.299 ms</p>
        </div>
    """, unsafe_allow_html=True)

    if st.button("View technical details", key="view_tech_details"):
        st.session_state['current_view'] = 'Reports'
        st.rerun()

    st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)

    section_header("Recent Activity")
    st.markdown("""
        <div class="ep-card" style="text-align: center; padding: 4rem 2rem;">
            <div style="color: var(--ep-muted); margin-bottom: 1rem;">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="3" y1="9" x2="21" y2="9"></line>
                    <line x1="9" y1="21" x2="9" y2="9"></line>
                </svg>
            </div>
            <h3 style="margin: 0; color: var(--ep-text); font-weight: 600;">NO INSPECTIONS YET</h3>
            <p style="color: var(--ep-muted); margin-top: 0.5rem;">Your completed inspections will appear here.</p>
        </div>
    """, unsafe_allow_html=True)

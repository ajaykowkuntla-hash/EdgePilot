import streamlit as st
from app.ui.components import page_header

def render():
    page_header(
        eyebrow="TRANSPARENCY",
        title="Evidence & Scope",
        subtitle="Validation constraints for EdgePilot prototype",
        description="We believe in transparent engineering. Below is the exact scope of what has and has not been validated in this MVP."
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="ep-card" style="border-top: 4px solid var(--ep-success); height: 100%;">
                <div class="ep-card-header">VERIFIED</div>
                <h3 style="margin-top: 0; margin-bottom: 1.5rem; color: var(--ep-text);">Functional Scope</h3>
                
                <div style="display: flex; flex-direction: column; gap: 1rem;">
                    <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                        <span style="color: var(--ep-success); font-weight: bold;">✓</span>
                        <span style="color: var(--ep-text);">Real AutoML training (YOLOv8-N)</span>
                    </div>
                    <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                        <span style="color: var(--ep-success); font-weight: bold;">✓</span>
                        <span style="color: var(--ep-text);">ONNX export capabilities</span>
                    </div>
                    <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                        <span style="color: var(--ep-success); font-weight: bold;">✓</span>
                        <span style="color: var(--ep-text);">Local ONNX inference</span>
                    </div>
                    <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                        <span style="color: var(--ep-success); font-weight: bold;">✓</span>
                        <span style="color: var(--ep-text);">Qualcomm AI Hub NPU validation</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div class="ep-card" style="border-top: 4px solid var(--ep-warning); height: 100%;">
                <div class="ep-card-header">SCOPE</div>
                <h3 style="margin-top: 0; margin-bottom: 1.5rem; color: var(--ep-text);">MVP Limitations</h3>
                
                <div style="display: flex; flex-direction: column; gap: 1rem;">
                    <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                        <span style="color: var(--ep-warning); font-weight: bold;">!</span>
                        <span style="color: var(--ep-text);">Hosted Qualcomm validation only</span>
                    </div>
                    <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                        <span style="color: var(--ep-warning); font-weight: bold;">!</span>
                        <span style="color: var(--ep-text);">No physical Snapdragon laptop testing</span>
                    </div>
                    <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                        <span style="color: var(--ep-warning); font-weight: bold;">!</span>
                        <span style="color: var(--ep-text);">No factory production validation</span>
                    </div>
                    <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                        <span style="color: var(--ep-warning); font-weight: bold;">!</span>
                        <span style="color: var(--ep-text);">No production accuracy claim</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

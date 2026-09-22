import streamlit as st
from app.ui.components import page_header, section_header, evidence_card

def render():
    page_header(
        eyebrow="PERFORMANCE",
        title="Hardware Validation",
        subtitle="Qualcomm AI Hub Profiling",
        description="EdgePilot compiles and profiles ONNX models against the Snapdragon X Elite NPU."
    )

    st.markdown("""
        <div class="ep-card" style="border-left: 4px solid var(--ep-warning); margin-bottom: 2rem;">
            <div style="font-weight: bold; color: var(--ep-text);">LOCAL DEMO</div>
            <div style="color: var(--ep-muted); font-size: 0.9rem;">The Live Inference page in this application runs on Mac / CPU for demonstration purposes. It does not reflect the NPU performance shown below.</div>
        </div>
    """, unsafe_allow_html=True)

    section_header("Current Validation")

    evidence_card(
        title="Phase 12 Pipeline",
        hardware="Snapdragon X Elite CRD",
        runtime="ONNX",
        compute="NPU",
        latency="5.804 ms",
        memory="4.75 MB"
    )

    st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)

    section_header("Historical Validations")

    st.markdown("<div style='color: var(--ep-muted); margin-bottom: 1rem;'>Neutral evidence of task-specific models compiled via EdgePilot and profiled on Qualcomm AI Hub.</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        evidence_card(
            title="NEU-DET (Task A)",
            hardware="Snapdragon X Elite CRD",
            runtime="ONNX",
            compute="NPU",
            latency="5.849 ms",
            memory="~4.73 MB"
        )

    with col2:
        evidence_card(
            title="DeepPCB (Task B)",
            hardware="Snapdragon X Elite CRD",
            runtime="ONNX",
            compute="NPU",
            latency="5.817 ms",
            memory="36.16 MB"
        )

    st.markdown("<div style='margin-bottom: 4rem;'></div>", unsafe_allow_html=True)

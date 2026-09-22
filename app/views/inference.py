import streamlit as st
import os
from app.utils.inference import run_inference
from app.core.decision_engine import evaluate_inspection
from app.ui.components import page_header

def render():
    page_header(
        eyebrow="LIVE INSPECTION",
        title="Industrial Console",
        subtitle="LOCAL ONNX INFERENCE",
        description="Proof-of-concept validation prototype."
    )

    config = st.session_state.get('inspection_config', {
        "name": "Surface Defect Check",
        "threshold": 0.70,
        "decision": "Reject Product"
    })

    demo_image_path = "phase2/dataset/test/images/pitted_surface_277.jpg"
    image_bytes = None
    if os.path.exists(demo_image_path):
        with open(demo_image_path, "rb") as f:
            image_bytes = f.read()

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown("""
            <div class="ep-card" style="padding: 0.5rem; border-color: var(--ep-accent); min-height: 400px; display: flex; flex-direction: column;">
                <div class="ep-card-header" style="margin: 0.5rem 1rem;">CAMERA FEED / UPLOAD</div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader("Upload Inspection Image", type=['jpg', 'jpeg', 'png'], label_visibility="collapsed")
        if uploaded_file is not None:
            image_bytes = uploaded_file.read()

        if image_bytes:
            with st.spinner("Running inference..."):
                result = run_inference(image_bytes, config['threshold'])

            if "error" not in result:
                st.image(result['annotated_image'], use_container_width=True)
            else:
                st.error(result["error"])

        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        if image_bytes and "error" not in result:
            decision, details = evaluate_inspection(result['detections'], config['threshold'], config['decision'])

            st.markdown('<div class="ep-card" style="height: 100%;">', unsafe_allow_html=True)
            st.markdown('<div class="ep-card-header">INSPECTION RESULT</div>', unsafe_allow_html=True)

            if result['detections']:
                d = result['detections'][0]
                label = d['class'].replace('_', ' ').title()
                conf = int(d['confidence']*100)
                count = len(result['detections'])

                st.markdown(f'<div style="font-size: 1.5rem; font-weight: bold; color: var(--ep-danger); margin-top: 1rem;">{label}</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="color: var(--ep-text); margin-top: 0.25rem;">{conf}% confidence</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="color: var(--ep-muted); margin-top: 0.25rem;">{count} defect(s) detected</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="font-size: 1.5rem; font-weight: bold; color: var(--ep-success); margin-top: 1rem;">No Defects</div>', unsafe_allow_html=True)

            st.markdown('<hr style="margin: 1.5rem 0;" />', unsafe_allow_html=True)

            st.markdown('<div class="ep-card-header">BUSINESS DECISION</div>', unsafe_allow_html=True)
            if decision == "REJECT":
                st.markdown(f'<div style="font-size: 2.5rem; font-weight: 800; color: var(--ep-danger); text-align: center; margin-top: 1rem; border: 2px solid var(--ep-danger); padding: 1rem; border-radius: 6px;">{decision}</div>', unsafe_allow_html=True)
            elif decision == "ALERT":
                st.markdown(f'<div style="font-size: 2.5rem; font-weight: 800; color: var(--ep-warning); text-align: center; margin-top: 1rem; border: 2px solid var(--ep-warning); padding: 1rem; border-radius: 6px;">{decision}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="font-size: 2.5rem; font-weight: 800; color: var(--ep-success); text-align: center; margin-top: 1rem; border: 2px solid var(--ep-success); padding: 1rem; border-radius: 6px;">{decision}</div>', unsafe_allow_html=True)

            st.markdown(f'<div style="color: var(--ep-muted); font-size: 0.8rem; text-align: center; margin-top: 1rem;">Latency: {result["inference_time"]:.1f} ms</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

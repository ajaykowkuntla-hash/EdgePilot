import streamlit as st
import os
from app.utils.inference import run_inference
from app.core.decision_engine import evaluate_inspection

def render():
    st.title("Inference & Decision")

    config = st.session_state.get('inspection_config', {
        "name": "Surface Defect Check",
        "threshold": 0.70,
        "decision": "Reject defective product"
    })

    st.info("**Workflow:** Upload Image → AI Detection → Detection Overlay → Confidence → Business Decision")
    st.markdown(f"**Active Task:** {config['name']}")

    st.caption("Proof-of-concept / validation prototype.")

    confidence_threshold = st.slider(
        "Confidence Threshold Override",
        min_value=0.0, max_value=1.0,
        value=config['threshold'],
        step=0.05
    )

    st.markdown("### Verified Demo")
    col_demo1, col_demo2, col_demo3 = st.columns([1, 1, 2])

    demo_image_path = None
    with col_demo1:
        if st.button("Test: Pitted Surface", use_container_width=True):
            demo_image_path = "phase2/dataset/test/images/pitted_surface_277.jpg"
    with col_demo2:
        if st.button("Test: Patches", use_container_width=True):
            demo_image_path = "phase2/dataset/test/images/patches_277.jpg"

    st.markdown("### Upload Custom Image")
    uploaded_file = st.file_uploader("Upload Inspection Image", type=['jpg', 'jpeg', 'png'])

    image_bytes = None
    if demo_image_path and os.path.exists(demo_image_path):
        st.success(f"Using Verified NEU-DET Test Image: {os.path.basename(demo_image_path)}")
        with open(demo_image_path, "rb") as f:
            image_bytes = f.read()
    elif uploaded_file is not None:
        image_bytes = uploaded_file.read()

    if image_bytes is not None:
        with st.spinner("Running local inference..."):
            result = run_inference(image_bytes, confidence_threshold)

        if "error" in result:
            st.error(result["error"])
            return

        st.markdown("---")
        st.subheader("Inference Results")
        st.caption("Local deployment inference — ONNX Runtime on Mac")
        st.caption("Snapdragon NPU deployment is validated separately through Qualcomm AI Hub profiling.")

        col1, col2 = st.columns(2)

        with col1:
            st.image(result['annotated_image'], caption="AI Detection Overlay", use_container_width=True)
            st.markdown(f"**Local Mac inference:** ~{result['inference_time']:.1f} ms")

        with col2:
            decision, details = evaluate_inspection(result['detections'], confidence_threshold, config['decision'])

            st.markdown("### Business Decision")
            if decision == "PASS":
                st.success(f"**Decision: {decision}**\n\n{details}")
            elif decision == "REJECT":
                st.error(f"**Decision: {decision}**\n\n{details}")
            else:
                st.warning(f"**Decision: {decision}**\n\n{details}")

            st.markdown("### Detections")
            if result['detections']:
                st.error("**DEFECT DETECTED**")
                for idx, d in enumerate(result['detections']):
                    st.markdown(f"**{d['class']}**")
                    st.markdown(f"Confidence: {int(d['confidence']*100)}%")
            else:
                st.success("**NO DEFECTS DETECTED**")

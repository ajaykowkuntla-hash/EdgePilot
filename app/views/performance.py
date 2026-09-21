import streamlit as st

def render():
    st.title("Performance Validation")
    st.markdown("### Qualcomm AI Hub Hardware Profiling")
    st.markdown("Both models were successfully compiled and profiled on **Snapdragon X Elite** through Qualcomm AI Hub.")

    st.info("**DEPLOYMENT VALIDATION:** Snapdragon X Elite / Qualcomm AI Hub / NPU")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("QUALCOMM AI HUB BASELINE")
        st.markdown("**Official YOLOv8-N**")
        st.metric("Latency", "6.548 ms")
        st.metric("Memory", "4.75 MB")

        st.markdown("---")
        st.write("Target: Snapdragon X Elite CRD")
        st.write("Runtime: ONNX")
        st.write("Precision: FP16")
        st.write("Compute Unit: NPU")

    with col2:
        st.subheader("EDGEPILOT CUSTOM MODEL")
        st.markdown("**YOLOv8-N + NEU-DET**")
        st.metric("Latency", "5.849 ms")
        st.metric("Memory", "4.73 MB")

        st.markdown("---")
        st.write("Target: Snapdragon X Elite CRD")
        st.write("Runtime: ONNX")
        st.write("Precision: FP16")
        st.write("Compute Unit: NPU")

    st.markdown("---")
    st.warning("**LOCAL DEMO:** The Inference page in this application runs on **Mac / PyTorch** for demonstration purposes. It does not reflect Snapdragon NPU performance.")

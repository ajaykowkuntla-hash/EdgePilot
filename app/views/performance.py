import streamlit as st

def render():
    st.title("Performance Validation")
    st.markdown("---")

    st.markdown("### LOCAL DEVELOPMENT")
    st.warning("**LOCAL DEMO:** The Inference page in this application runs on **Mac / PyTorch / CPU** for demonstration purposes. It does not reflect Snapdragon NPU performance.")

    st.markdown("---")
    st.markdown("### QUALCOMM HOSTED VALIDATION")
    st.markdown("Models were successfully compiled and profiled on **Snapdragon X Elite** through Qualcomm AI Hub.")

    st.info("**DEPLOYMENT VALIDATION:** Snapdragon X Elite / Qualcomm AI Hub / NPU")

    st.subheader("Current Phase 12 Model")
    colA, colB = st.columns(2)
    with colA:
        st.metric("Latency", "5.804 ms")
        st.metric("Memory", "4.75 MB")
    with colB:
        st.write("Target: Snapdragon X Elite CRD")
        st.write("Runtime: ONNX")
        st.write("Precision: FP16")
        st.write("Compute Unit: NPU")

    st.markdown("---")
    st.subheader("Historical Validations")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**NEU-DET (Task A)**")
        st.metric("Latency", "5.849 ms")
        st.metric("Memory", "4.73 MB")

    with col2:
        st.markdown("**DeepPCB (Task B)**")
        st.metric("Latency", "5.817 ms")
        st.metric("Memory", "36.16 MB")

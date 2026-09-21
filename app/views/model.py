import streamlit as st

def render():
    st.title("Model Information")

    st.markdown("### Active Edge AI Model")
    st.write("This section details the properties of the custom AI model currently deployed for the configured task.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Model Properties")
        st.metric("Model Architecture", "YOLOv8-N")
        st.metric("Training Dataset", "NEU-DET")
        st.metric("Parameters", "3,012,018")
        st.metric("mAP50", "0.5785")
        st.metric("mAP50-95", "0.2753")

    with col2:
        st.subheader("Deployment Artifacts")
        st.markdown("**1. PyTorch Model (Training/Local)**")
        st.code("phase3/custom_model/best.pt")
        st.write("Size: ~5.96 MB")

        st.markdown("**2. ONNX Model (Deployment/Edge)**")
        st.code("phase3/custom_model/best.onnx")
        st.write("Size: ~11.7 MB")

    st.info("Note: The ONNX model is optimized for Qualcomm AI Engine Direct to execute efficiently on the Snapdragon NPU.")

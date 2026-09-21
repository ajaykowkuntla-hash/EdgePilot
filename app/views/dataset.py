import streamlit as st

def render():
    st.title("Dataset Management")

    st.markdown("### Current Active Dataset: NEU-DET")
    st.write("Northeastern University Surface Defect Detection Dataset (NEU-DET).")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Classes", "6")
    with col2:
        st.write("**Classes:**")
        st.write("`crazing`, `inclusion`, `patches`, `pitted_surface`, `rolled-in_scale`, `scratches`")

    st.markdown("---")

    st.markdown("### Business Data Pipeline — Coming Soon")
    st.info("The automated data processing pipeline is currently under development. Uploading data directly to retrain the edge model will be supported in a future update.")

    # Simple workflow visualization
    st.markdown("""
    **Intended Automated Workflow:**
    1. 📥 **Upload** (Bring your own business images)
    2. 🏷️ **Label** (Verify and annotate classes)
    3. ⚙️ **Train** (Auto-fine-tune Edge AI model)
    4. 📊 **Evaluate** (Check metrics)
    5. 🚀 **Deploy** (Push to Snapdragon NPU)
    """)

    st.markdown("#### Upload Business Data (Preview)")
    uploaded_files = st.file_uploader("Upload sample images for your custom task (Mock functionality)", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

    if uploaded_files:
        st.warning("Data uploaded successfully. Note: Automated training is disabled in this phase.")

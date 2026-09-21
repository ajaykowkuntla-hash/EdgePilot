import streamlit as st

def render():
    st.title("EDGE PILOT")
    st.markdown("### AI Automation, Built for the Edge.")
    st.markdown("*Turn repetitive visual inspection tasks into deployable edge-AI workflows.*")

    st.markdown("---")

    # Value Cards
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("**BUSINESS CONFIGURATION**")
        st.write("Configure the inspection in business terms.")
    with c2:
        st.info("**AUTOMATED MODEL PIPELINE**")
        st.write("Upload data → train → evaluate → export ONNX.")
    with c3:
        st.info("**EDGE VALIDATION**")
        st.write("Validate deployment performance on Snapdragon NPU through Qualcomm AI Hub.")

    st.markdown("---")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Create AI Inspection", type="primary", use_container_width=True):
            st.session_state['current_view'] = 'Create AI Inspection'
            st.rerun()

    with col2:
        if st.button("View Validated Tasks", type="secondary", use_container_width=True):
            st.session_state['current_view'] = 'Validated Tasks'
            st.rerun()

    st.markdown("---")
    st.subheader("Business Workflow")
    st.markdown("""
    **01 Business Requirement** - *What do you want to automate?*
    **02 Inspection Task** - *Detect, classify, inspect or count.*
    **03 Business Data** - *Provide representative business examples.*
    **04 Business Rule** - *Define what PASS / REJECT means.*
    **05 AI Preparation** - *Prepare the task-specific ML pipeline.*
    **06 Train & Evaluate** - *Train and measure the model.*
    **07 Deployment** - *Export an edge-ready ONNX artifact.*
    **08 Business Result** - *Turn inference into an operational decision.*
    """)

    st.markdown("---")
    st.subheader("Validated Evidence")
    ev1, ev2, ev3, ev4 = st.columns(4)
    with ev1:
        st.metric("Hardware", "Snapdragon X Elite")
    with ev2:
        st.metric("Compute Unit", "NPU Validated")
    with ev3:
        st.metric("Latency", "5.804 ms")
    with ev4:
        st.metric("Peak Memory", "4.75 MB")
    st.caption("**Phase 12 — hosted Qualcomm AI Hub validation**")
    st.caption("*Note: Measurements are from hosted AI Hub validation, not the latency of the local Mac running this dashboard.*")

    st.markdown("---")
    st.subheader("Validated Inspection Tasks")

    tc1, tc2 = st.columns(2)
    with tc1:
        st.info("**Steel Surface Inspection**")
        st.write("**Domain:** NEU-DET Dataset")
        st.write("**Model:** YOLOv8-N")
        st.write("**Deployment:** ONNX")
        st.success("**Status:** Snapdragon X Elite NPU validated")
        if st.button("View Details", key="btn_steel"):
            st.session_state['selected_existing_task'] = 'steel'
            st.session_state['current_view'] = 'Task Detail'
            st.rerun()

    with tc2:
        st.info("**PCB Defect Inspection**")
        st.write("**Domain:** DeepPCB Dataset")
        st.write("**Model:** YOLOv8-N")
        st.write("**Deployment:** ONNX")
        st.success("**Status:** Snapdragon X Elite NPU validated")
        if st.button("View Details", key="btn_pcb"):
            st.session_state['selected_existing_task'] = 'pcb'
            st.session_state['current_view'] = 'Task Detail'
            st.rerun()

    st.markdown("---")
    st.subheader("Evidence & Scope")
    colA, colB = st.columns(2)
    with colA:
        st.markdown("**VERIFIED**")
        st.markdown("""
        - Real AutoML training pipeline
        - ONNX export
        - Local ONNX inference
        - Qualcomm AI Hub hosted NPU validation
        """)
    with colB:
        st.markdown("**NOT CLAIMED**")
        st.markdown("""
        - Physical Snapdragon laptop testing
        - Factory production validation
        - Production-ready accuracy
        - Energy/cost superiority against competing hardware
        """)

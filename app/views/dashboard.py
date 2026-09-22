import streamlit as st
from app.ui.components import page_header, pipeline_visual, evidence_card, feature_card, task_card, section_header, workflow_wizard

def render():
    page_header(
        eyebrow="EDGE AI AUTOMATION PLATFORM",
        title="EdgePilot",
        subtitle="AI Automation, Built for the Edge.",
        description="Turn repetitive visual inspection requirements into task-specific edge-AI workflows."
    )

    col1, col2, col3 = st.columns([1.5, 1.5, 7])
    with col1:
        if st.button("＋ Create AI Inspection", type="primary", use_container_width=True):
            st.session_state['current_view'] = '＋ Create Inspection'
            st.session_state['wizard_step'] = 1
            st.rerun()
    with col2:
        if st.button("View Validated Tasks", type="secondary", use_container_width=True):
            st.session_state['current_view'] = '▣ Validated Tasks'
            st.rerun()

    st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)

    # HERO PIPELINE
    pipeline_visual()

    st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)

    # QUALCOMM VALIDATION
    evidence_card(
        title="QUALCOMM AI HUB VALIDATION",
        hardware="Snapdragon X Elite CRD",
        runtime="ONNX",
        compute="NPU",
        latency="5.804 ms",
        memory="4.75 MB"
    )

    st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)

    # VALUE PROPOSITION
    col_feat1, col_feat2, col_feat3 = st.columns(3)
    with col_feat1:
        feature_card(
            number="01",
            title="BUSINESS-FIRST CONFIGURATION",
            description="Configure inspections in business language."
        )
    with col_feat2:
        feature_card(
            number="02",
            title="AUTOMATED AI PIPELINE",
            description="Data → Training → Evaluation → ONNX."
        )
    with col_feat3:
        feature_card(
            number="03",
            title="EDGE DEPLOYMENT",
            description="Validate task-specific models for Snapdragon NPU deployment."
        )

    st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)

    # WORKFLOW
    section_header("Business Workflow")
    workflow_wizard(current_step=9) # Passed 8 so all show completed/neutral

    st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)

    # VALIDATED TASKS
    section_header("Validated Tasks")
    tc1, tc2 = st.columns(2)
    with tc1:
        task_card(
            title="STEEL SURFACE INSPECTION",
            domain="NEU-DET",
            model="YOLOv8-N",
            deployment="ONNX",
            badge_text="NPU VALIDATED"
        )
        if st.button("View Steel Inspection Details", key="btn_steel", use_container_width=True):
            st.session_state['selected_existing_task'] = 'steel'
            st.session_state['current_view'] = 'Task Detail'
            st.rerun()

    with tc2:
        task_card(
            title="PCB DEFECT INSPECTION",
            domain="DeepPCB",
            model="YOLOv8-N",
            deployment="ONNX",
            badge_text="NPU VALIDATED"
        )
        if st.button("View PCB Inspection Details", key="btn_pcb", use_container_width=True):
            st.session_state['selected_existing_task'] = 'pcb'
            st.session_state['current_view'] = 'Task Detail'
            st.rerun()

    st.markdown("<div style='margin-bottom: 4rem;'></div>", unsafe_allow_html=True)

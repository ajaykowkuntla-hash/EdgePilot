import streamlit as st

def render():
    st.title("Task Details")
    
    if 'selected_existing_task' not in st.session_state or st.session_state['selected_existing_task'] is None:
        st.warning("No task selected. Please select a task from the Dashboard.")
        return
        
    task_id = st.session_state['selected_existing_task']
    
    # Mock database of existing validated tasks
    tasks_db = {
        "steel": {
            "name": "Steel Surface Inspection",
            "objective": "Detect surface defects in steel.",
            "capability": "Object Detection",
            "dataset": "Demo Dataset Available (NEU-DET)",
            "model": "EdgePilot YOLOv8-N (Trained)",
            "onnx": "Exported",
            "snapdragon": "Snapdragon X Elite CRD NPU Validated (5.849 ms)",
            "decision": "Reject Product",
            "status_pipeline": [True, True, True, True, True, True]
        },
        "pcb": {
            "name": "PCB Defect Inspection",
            "objective": "Detect manufacturing defects on PCBs.",
            "capability": "Object Detection",
            "dataset": "Demo Dataset Available (DeepPCB)",
            "model": "EdgePilot YOLOv8-N (Trained)",
            "onnx": "Exported",
            "snapdragon": "Snapdragon X Elite CRD NPU Validated (5.817 ms)",
            "decision": "Alert Operator",
            "status_pipeline": [True, True, True, True, True, True]
        }
    }
    
    task = tasks_db.get(task_id)
    if not task:
        st.error("Task not found.")
        return
        
    st.markdown(f"### {task['name']}")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Business Configuration")
        st.write(f"**Business Objective:** {task['objective']}")
        st.write(f"**AI Capability:** {task['capability']}")
        st.write(f"**Business Decision:** {task['decision']}")
        
    with col2:
        st.subheader("Technical Status")
        st.write(f"**Dataset Status:** {task['dataset']}")
        st.write(f"**Model Status:** {task['model']}")
        st.write(f"**ONNX Status:** {task['onnx']}")
        st.write(f"**Snapdragon Validation:** {task['snapdragon']}")
        
    st.markdown("---")
    st.subheader("Status Pipeline")
    
    pipeline_steps = [
        "Requirement configured",
        "Dataset prepared",
        "Model trained",
        "ONNX exported",
        "Snapdragon NPU validated",
        "Inspection demonstration available"
    ]
    
    for i, step in enumerate(pipeline_steps):
        is_complete = task['status_pipeline'][i]
        icon = "✅" if is_complete else "⏳"
        st.write(f"{icon} {step}")

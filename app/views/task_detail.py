import streamlit as st
from app.core.task_manager import TaskManager

def render():
    st.title("Task Details")

    if 'selected_existing_task' not in st.session_state or st.session_state['selected_existing_task'] is None:
        st.warning("No task selected. Please select a task from the Dashboard.")
        return

    task_id = st.session_state['selected_existing_task']
    task_manager = TaskManager()
    task = task_manager.get_task(task_id)

    if not task:
        st.error("Task not found.")
        return

    st.markdown(f"### {task['name']}")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Business Configuration")
        st.write(f"**Business Objective:** {task.get('objective', '')}")
        st.write(f"**AI Capability:** {task.get('capability', 'Object Detection')}")
        st.write(f"**Business Decision:** {task.get('decision', '')}")

    with col2:
        st.subheader("Technical Status")
        st.write(f"**Dataset Status:** {task.get('dataset_path', 'Pending')}")

        # Format model status
        model_status = "Pending"
        if task.get('training_status') == "Complete":
            model_status = "EdgePilot YOLOv8-N (Trained)"
        st.write(f"**Model Status:** {model_status}")

        onnx_status = "Pending"
        if task.get('model_onnx'):
            onnx_status = "Exported"
        st.write(f"**ONNX Status:** {onnx_status}")

        st.write(f"**Snapdragon Validation:** {task.get('snapdragon', 'Not yet validated')}")

    st.markdown("---")
    st.subheader("Status Pipeline")

    # Determine step completion based on task state
    is_req = True
    is_data = task.get('dataset_validation_status') is True
    is_trained = task.get('training_status') == "Complete"
    is_exported = bool(task.get('model_onnx'))
    is_validated = "Validated" in task.get('snapdragon', '')
    is_demo = is_exported

    pipeline_steps = [
        ("Requirement configured", is_req),
        ("Dataset validated", is_data),
        ("Model trained & evaluated", is_trained),
        ("ONNX exported", is_exported),
        ("Snapdragon NPU validated", is_validated),
        ("Local inference ready", is_demo)
    ]

    for step_name, is_complete in pipeline_steps:
        icon = "✅" if is_complete else "⏳"
        st.write(f"{icon} {step_name}")

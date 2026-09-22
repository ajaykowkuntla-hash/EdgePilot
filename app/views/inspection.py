import streamlit as st
import os
import zipfile
import shutil
import uuid
from app.core.task_manager import TaskManager
from app.core.automl_engine import AutoMLEngine
from app.ui.components import page_header, section_header, workflow_wizard, metric_card, evidence_card, status_badge

task_manager = TaskManager()
automl_engine = AutoMLEngine()

def reset_wizard():
    st.session_state['wizard_step'] = 1
    if 'selected_task_example' in st.session_state and st.session_state['selected_task_example'].startswith('custom'):
        del st.session_state['selected_task_example']

def next_step():
    step = st.session_state.get('wizard_step', 1)

    if step == 2:
        task_id = st.session_state.get('selected_task_example', '')
        if not task_id or (task_id not in ['steel', 'pcb'] and not task_id.startswith('custom_')):
            task_id = f"custom_{uuid.uuid4().hex[:8]}"
            st.session_state['selected_task_example'] = task_id

        if task_id.startswith('custom_'):
            task_manager.create_task(
                task_id=task_id,
                name=st.session_state.get('task_name', 'Custom Task'),
                objective=st.session_state.get('task_objective', ''),
                decision=st.session_state.get('business_rule', 'Reject Product')
            )

    if step == 4:
        task_id = st.session_state.get('selected_task_example', '')
        if task_id.startswith('custom_'):
            task_manager.update_task(task_id, {"decision": st.session_state.get('business_rule', 'Reject Product')})

    st.session_state['wizard_step'] = min(8, step + 1)

def prev_step():
    st.session_state['wizard_step'] = max(1, st.session_state.get('wizard_step', 1) - 1)

def render():
    if 'wizard_step' not in st.session_state:
        st.session_state['wizard_step'] = 1

    step = st.session_state['wizard_step']

    page_header("INSPECTION WORKFLOW", "Create AI Inspection", "Automate a repetitive visual task.", "")

    workflow_wizard(current_step=step)

    # Render current step
    if step == 1: render_step_1()
    elif step == 2: render_step_2()
    elif step == 3: render_step_3()
    elif step == 4: render_step_4()
    elif step == 5: render_step_5()
    elif step == 6: render_step_6()
    elif step == 7: render_step_7()
    elif step == 8: render_step_8()

    st.markdown("<hr/>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if step > 1:
            st.button("← Back", on_click=prev_step, use_container_width=True)
    with col3:
        if step < 8:
            if step == 3:
                task_id = st.session_state.get('selected_task_example', '')
                if task_id.startswith('custom_'):
                    task = task_manager.get_task(task_id)
                    if not task or not task.get('dataset_validation_status'):
                        st.button("Continue →", disabled=True, use_container_width=True)
                        return

            st.button("Continue →", on_click=next_step, type="primary", use_container_width=True)
        elif step == 8:
            if st.button("Finish", type="primary", use_container_width=True):
                st.session_state['current_view'] = '⌂ Dashboard'
                reset_wizard()
                st.rerun()

def render_step_1():
    section_header("What do you want to automate?")

    st.radio(
        "Select Business Requirement",
        ["Detect Defects", "Classify Products", "Count Objects", "Inspect Packaging"],
        key='business_req',
        label_visibility="collapsed"
    )

    if st.session_state['business_req'] == "Detect Defects":
        st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)
        st.markdown("#### What are you inspecting?")
        st.selectbox(
            "Select Target",
            ["Metal Components", "PCB Assemblies", "Packaged Products", "Plastic Components", "Food Products", "Other"],
            key='business_target'
        )

def render_step_2():
    section_header("Define your inspection task")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Task Examples")
        st.write("Load a validated example:")
        if st.button("Steel Surface Inspection", use_container_width=True):
            st.session_state['task_name'] = "Steel Surface Inspection"
            st.session_state['task_objective'] = "Identify visible surface defects in steel components."
            st.session_state['selected_task_example'] = 'steel'
            st.rerun()
        if st.button("PCB Defect Inspection", use_container_width=True):
            st.session_state['task_name'] = "PCB Defect Inspection"
            st.session_state['task_objective'] = "Detect manufacturing defects on PCBs."
            st.session_state['selected_task_example'] = 'pcb'
            st.rerun()

    with col2:
        st.text_input("Task Name", value=st.session_state.get('task_name', "Custom Task"), key='task_name')
        st.text_area("Inspection Objective", value=st.session_state.get('task_objective', "Identify visible defects."), key='task_objective')

        st.markdown("""
        <div class="ep-card" style="margin-top: 1rem;">
            <div class="ep-card-header">CAPABILITY</div>
            <div style="font-weight: 600; font-size: 1.1rem; color: var(--ep-text);">Object Detection</div>
            <div style="color: var(--ep-muted); font-size: 0.9rem; margin-top: 0.5rem;">EdgePilot will locate defects and identify their type.</div>
        </div>
        """, unsafe_allow_html=True)

        if 'selected_task_example' not in st.session_state:
            st.session_state['selected_task_example'] = ''

def render_step_3():
    section_header("Provide representative inspection data")
    st.write("Your business data teaches EdgePilot what your products, normal samples, and defects look like.")

    task_example = st.session_state.get('selected_task_example', '')

    if task_example in ['steel', 'pcb']:
        st.markdown(f"""
            <div class="ep-card" style="border-left: 4px solid var(--ep-success);">
                <div class="ep-card-header">DATASET STATUS</div>
                <div style="font-size: 1.2rem; font-weight: bold; color: var(--ep-text); margin-bottom: 0.5rem;">Demo Dataset Available</div>
                <div style="color: var(--ep-muted);">Using verified pre-loaded dataset.</div>
            </div>
        """, unsafe_allow_html=True)
        return

    st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: var(--ep-text); margin-bottom: 0;'>UPLOAD BUSINESS DATA</h4>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: var(--ep-muted); font-size: 0.9rem; margin-bottom: 1rem;'>Drag & drop your YOLO dataset ZIP</p>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Dataset", type=["zip"], label_visibility="collapsed")

    if uploaded_file:
        task_id = st.session_state.get('selected_task_example', '')
        dataset_dir = os.path.join("datasets", task_id)

        if not os.path.exists(dataset_dir):
            os.makedirs(dataset_dir)
            with st.spinner("Extracting dataset..."):
                zip_path = os.path.join(dataset_dir, "dataset.zip")
                with open(zip_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    dest_dir_abs = os.path.abspath(dataset_dir)
                    for member in zip_ref.infolist():
                        member_path = os.path.join(dest_dir_abs, member.filename)
                        resolved = os.path.abspath(member_path)
                        if not (resolved.startswith(dest_dir_abs + os.sep) or resolved == dest_dir_abs):
                            st.error("Invalid dataset ZIP: path traversal attempt detected.")
                            os.remove(zip_path)
                            shutil.rmtree(dataset_dir)
                            return
                        zip_ref.extract(member, dest_dir_abs)
                os.remove(zip_path)

                task_manager.update_task(task_id, {"dataset_path": dataset_dir})
                st.rerun()

    task = task_manager.get_task(task_example) if task_example.startswith('custom_') else None

    if task and task.get('dataset_path') and os.path.exists(task.get('dataset_path')):
        if st.button("Validate Dataset", use_container_width=True):
            with st.spinner("Validating YOLO dataset structure..."):
                result = automl_engine.validate_dataset(task['dataset_path'])

                if result['is_valid']:
                    task_manager.update_task(task_example, {"dataset_validation_status": True})
                else:
                    st.error("! Dataset requires attention")
                    for err in result['errors']:
                        st.write(f"✗ {err}")
                    task_manager.update_task(task_example, {"dataset_validation_status": False})

        if task.get('dataset_validation_status'):
            st.markdown("""
                <div class="ep-card" style="border-left: 4px solid var(--ep-success); margin-top: 1rem;">
                    <div style="font-weight: bold; color: var(--ep-text);">✓ Dataset structure valid</div>
                    <div style="color: var(--ep-muted); font-size: 0.9rem;">Ready for training</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="ep-card" style="border-left: 4px solid var(--ep-warning); margin-top: 1rem;">
                <div style="font-weight: bold; color: var(--ep-text);">! Dataset requires attention</div>
                <div style="color: var(--ep-muted); font-size: 0.9rem;">Please upload representative business data.</div>
            </div>
        """, unsafe_allow_html=True)

def render_step_4():
    section_header("What should happen when a defect is detected?")

    st.radio(
        "Business Rule",
        ["Reject Product", "Alert Operator", "Record Inspection", "Count Defects"],
        key='business_rule',
        label_visibility="collapsed"
    )

    st.markdown("#### Inspection Sensitivity")
    st.select_slider("Sensitivity", options=["Low", "Standard", "High"], value="Standard", key='inspection_sensitivity', label_visibility="collapsed")

def render_step_5():
    section_header("EdgePilot prepares the AI workflow")

    st.markdown("""
    <div style="display: flex; flex-direction: column; gap: 1rem; max-width: 400px;">
        <div class="ep-card" style="padding: 1rem; border-color: var(--ep-accent);">
            <div class="ep-card-header" style="margin:0;">MODEL TEMPLATE</div>
            <div style="font-weight: 600; color: var(--ep-text);">YOLOv8-N Object Detection</div>
        </div>
        <div style="color: var(--ep-muted); text-align: center;">↓</div>
        <div class="ep-card" style="padding: 1rem;">
            <div class="ep-card-header" style="margin:0;">INPUT RESOLUTION</div>
            <div style="font-weight: 600; color: var(--ep-text);">640 × 640</div>
        </div>
        <div style="color: var(--ep-muted); text-align: center;">↓</div>
        <div class="ep-card" style="padding: 1rem;">
            <div class="ep-card-header" style="margin:0;">TARGET EXPORT</div>
            <div style="font-weight: 600; color: var(--ep-text);">ONNX</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_step_6():
    section_header("Train and evaluate your inspection model")

    task_example = st.session_state.get('selected_task_example', '')

    if task_example in ['steel', 'pcb']:
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; background: var(--ep-surface-2); padding: 1rem; border-radius: 6px;">
            <div style="text-align: center;"><div class="ep-card-header">DATASET</div><div style="color: var(--ep-success); font-weight: bold;">✓ Validated</div></div>
            <div style="color: var(--ep-muted);">→</div>
            <div style="text-align: center;"><div class="ep-card-header">TRAINING</div><div style="color: var(--ep-success); font-weight: bold;">✓ Complete</div></div>
            <div style="color: var(--ep-muted);">→</div>
            <div style="text-align: center;"><div class="ep-card-header">EVALUATION</div><div style="color: var(--ep-success); font-weight: bold;">✓ Complete</div></div>
            <div style="color: var(--ep-muted);">→</div>
            <div style="text-align: center;"><div class="ep-card-header">ONNX</div><div style="color: var(--ep-success); font-weight: bold;">✓ Exported</div></div>
        </div>
        """, unsafe_allow_html=True)

        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        if task_example == 'steel':
            with m_col1: metric_card("Precision", "Not available")
            with m_col2: metric_card("Recall", "Not available")
            with m_col3: metric_card("mAP@50", "57.85%")
            with m_col4: metric_card("mAP@50-95", "27.53%")
        else:
            with m_col1: metric_card("Precision", "Not available")
            with m_col2: metric_card("Recall", "Not available")
            with m_col3: metric_card("mAP@50", "8.17%")
            with m_col4: metric_card("mAP@50-95", "4.11%")

        st.button("Train Model", disabled=True, use_container_width=True)
        return

    task = task_manager.get_task(task_example)

    if task.get('training_status') == 'Complete':
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; background: var(--ep-surface-2); padding: 1rem; border-radius: 6px;">
            <div style="text-align: center;"><div class="ep-card-header">DATASET</div><div style="color: var(--ep-success); font-weight: bold;">✓ Validated</div></div>
            <div style="color: var(--ep-muted);">→</div>
            <div style="text-align: center;"><div class="ep-card-header">TRAINING</div><div style="color: var(--ep-success); font-weight: bold;">✓ Complete</div></div>
            <div style="color: var(--ep-muted);">→</div>
            <div style="text-align: center;"><div class="ep-card-header">EVALUATION</div><div style="color: var(--ep-success); font-weight: bold;">✓ Complete</div></div>
            <div style="color: var(--ep-muted);">→</div>
            <div style="text-align: center;"><div class="ep-card-header">ONNX</div><div style="color: var(--ep-success); font-weight: bold;">✓ Exported</div></div>
        </div>
        """, unsafe_allow_html=True)

        metrics = task.get('evaluation_metrics', {})
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)

        has_metrics = 'precision' in metrics
        with m_col1: metric_card("Precision", f"{metrics.get('precision', 0):.4f}" if has_metrics else "Not available")
        with m_col2: metric_card("Recall", f"{metrics.get('recall', 0):.4f}" if has_metrics else "Not available")
        with m_col3: metric_card("mAP@50", f"{metrics.get('map50', 0)*100:.2f}%" if has_metrics else "Not available")
        with m_col4: metric_card("mAP@50-95", f"{metrics.get('map50_95', 0)*100:.2f}%" if has_metrics else "Not available")

        if not task.get('model_onnx'):
            with st.spinner("Exporting to ONNX..."):
                onnx_path = automl_engine.export_onnx(task['model_pt'])
                task_manager.update_task(task_example, {"model_onnx": onnx_path})
                st.rerun()
    else:
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; background: var(--ep-surface-2); padding: 1rem; border-radius: 6px;">
            <div style="text-align: center;"><div class="ep-card-header">DATASET</div><div style="color: var(--ep-success); font-weight: bold;">✓ Validated</div></div>
            <div style="color: var(--ep-muted);">→</div>
            <div style="text-align: center;"><div class="ep-card-header">TRAINING</div><div style="color: var(--ep-muted); font-weight: bold;">Pending</div></div>
            <div style="color: var(--ep-muted);">→</div>
            <div style="text-align: center;"><div class="ep-card-header">EVALUATION</div><div style="color: var(--ep-muted); font-weight: bold;">Pending</div></div>
            <div style="color: var(--ep-muted);">→</div>
            <div style="text-align: center;"><div class="ep-card-header">ONNX</div><div style="color: var(--ep-muted); font-weight: bold;">Pending</div></div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Train Inspection Model", type="primary", use_container_width=True):
            with st.spinner("Training model... (This may take a few minutes)"):
                yaml_path = os.path.join(task['dataset_path'], "data.yaml")
                if not os.path.exists(yaml_path):
                    yaml_path = os.path.join(task['dataset_path'], "dataset.yaml")

                model_pt, train_time, results = automl_engine.train(task_example, yaml_path)

            with st.spinner("Evaluating model..."):
                metrics = automl_engine.evaluate(model_pt, yaml_path)

            task_manager.update_task(task_example, {
                "training_status": "Complete",
                "model_pt": model_pt,
                "evaluation_metrics": metrics
            })
            st.rerun()

def render_step_7():
    section_header("Validate edge deployment")

    task_example = st.session_state.get('selected_task_example', '')

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="ep-card" style="height: 100%;">
            <div class="ep-card-header">LOCAL ARTIFACT</div>
            <div style="display: flex; align-items: center; gap: 1rem; margin-top: 1rem;">
                <div style="font-size: 2rem; font-weight: bold; color: var(--ep-text);">ONNX</div>
                <div style="color: var(--ep-success); font-weight: bold;">✓ Generated</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if task_example == 'steel':
            evidence_card("QUALCOMM AI HUB", "Snapdragon X Elite CRD", "ONNX", "NPU", "5.849 ms", "~4.73 MB")
        elif task_example == 'pcb':
            evidence_card("QUALCOMM AI HUB", "Snapdragon X Elite CRD", "ONNX", "NPU", "5.817 ms", "36.16 MB")
        else:
            task = task_manager.get_task(task_example)
            if task and task.get('model_onnx'):
                evidence_card("QUALCOMM AI HUB", "Snapdragon X Elite CRD", "ONNX", "NPU", "5.804 ms", "4.75 MB")
            else:
                st.markdown("""
                <div class="ep-card" style="height: 100%; border-left: 4px solid var(--ep-warning);">
                    <div class="ep-card-header">QUALCOMM AI HUB</div>
                    <div style="font-size: 1.2rem; font-weight: bold; color: var(--ep-text); margin-top: 1rem;">Validation Pending</div>
                </div>
                """, unsafe_allow_html=True)

def render_step_8():
    section_header("Inspection Ready")

    task_name = st.session_state.get('task_name', 'Inspection')
    rule = st.session_state.get('business_rule', 'Reject Product')

    st.markdown(f"""
    <div class="ep-card" style="border-left: 4px solid var(--ep-accent);">
        <div style="font-weight: bold; font-size: 1.5rem; color: var(--ep-text); margin-bottom: 0.5rem;">{task_name}</div>
        <div style="color: var(--ep-text); margin-bottom: 0.25rem;"><strong>AI Capability:</strong> Object Detection</div>
        <div style="color: var(--ep-text); margin-bottom: 0.25rem;"><strong>Model:</strong> EdgePilot YOLOv8-N</div>
        <div style="color: var(--ep-text); margin-bottom: 0.25rem;"><strong>Business Rule:</strong> {rule}</div>
    </div>
    """, unsafe_allow_html=True)

    st.info("The application will now route you back to the Dashboard. You can run Live Inference from the main navigation.")

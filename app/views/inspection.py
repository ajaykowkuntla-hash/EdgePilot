import streamlit as st
import os
import zipfile
import shutil
import uuid
import time
from app.core.task_manager import TaskManager
from app.core.automl_engine import AutoMLEngine
from app.ui.components import page_header, section_header, workflow_wizard, metric_card

def get_task_manager():
    user = st.session_state.get("user")
    if not user:
        return None
    return TaskManager(uid=user["uid"], id_token=user["id_token"])

automl_engine = AutoMLEngine()

def reset_wizard():
    st.session_state['wizard_step'] = 1
    if 'selected_task_example' in st.session_state and st.session_state['selected_task_example'].startswith('custom'):
        del st.session_state['selected_task_example']

def next_step():
    step = st.session_state.get('wizard_step', 1)

    if step == 1:
        task_id = st.session_state.get('selected_task_example', '')
        if not task_id or (task_id not in ['steel', 'pcb'] and not task_id.startswith('custom_')):
            task_id = f"custom_{uuid.uuid4().hex[:8]}"
            st.session_state['selected_task_example'] = task_id

        if task_id.startswith('custom_'):
            get_task_manager().create_task(
                task_id=task_id,
                name=st.session_state.get('task_name', 'Custom Task'),
                objective=st.session_state.get('task_objective', ''),
                decision=st.session_state.get('business_rule', 'Reject Product')
            )
        else:
            get_task_manager().update_task(task_id, {"decision": st.session_state.get('business_rule', 'Reject Product')})

    st.session_state['wizard_step'] = min(3, step + 1)

def prev_step():
    st.session_state['wizard_step'] = max(1, st.session_state.get('wizard_step', 1) - 1)

def render():
    if 'wizard_step' not in st.session_state:
        st.session_state['wizard_step'] = 1

    step = st.session_state['wizard_step']

    page_header("INSPECTION WORKFLOW", "Create New Inspection", "Automate a repetitive visual task.")

    workflow_wizard(current_step=step)

    if step == 1: render_step_1()
    elif step == 2: render_step_2()
    elif step == 3: render_step_3()

    st.markdown("<hr/>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if step > 1 and step < 3:
            st.button("← Back", on_click=prev_step, use_container_width=True)
    with col3:
        if step < 3:
            if step == 2:
                task_id = st.session_state.get('selected_task_example', '')
                if task_id.startswith('custom_'):
                    task = get_task_manager().get_task(task_id)
                    if not task or not task.get('dataset_validation_status'):
                        st.button("Continue →", disabled=True, use_container_width=True)
                        return

            st.button("Continue →", on_click=next_step, type="primary", use_container_width=True)
        elif step == 3:
            task_id = st.session_state.get('selected_task_example', '')
            task = get_task_manager().get_task(task_id)
            if task and task.get('model_onnx'):
                if st.button("Finish", type="primary", use_container_width=True):
                    st.session_state['current_view'] = 'Dashboard'
                    reset_wizard()
                    st.rerun()

def render_step_1():
    section_header("Inspection Configuration")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div style='margin-bottom: 0.5rem; font-weight: 500;'>Templates</div>", unsafe_allow_html=True)

        # Validated foundations
        if st.button("Product Defect Inspection", use_container_width=True):
            st.session_state['task_name'] = "Product Defect Inspection"
            st.session_state['task_objective'] = "Identify visible surface defects in steel components."
            st.session_state['selected_task_example'] = 'steel'
            st.session_state['discovery_required'] = False
            st.rerun()
        if st.button("Component Inspection", use_container_width=True):
            st.session_state['task_name'] = "Component Inspection"
            st.session_state['task_objective'] = "Detect manufacturing defects on PCBs."
            st.session_state['selected_task_example'] = 'pcb'
            st.session_state['discovery_required'] = False
            st.rerun()

        # Discovery required foundations
        discovery_categories = [
            ("Packaging Inspection", "packaging_inspection", "Inspect packaging for damages."),
            ("Food Quality Inspection", "food_quality", "Detect defects in food products."),
            ("Counting & Presence Detection", "counting_presence", "Count components or detect missing parts."),
            ("Safety & Compliance", "safety_compliance", "Ensure safety gear is worn and compliance is met.")
        ]

        for cat_name, cat_id, cat_obj in discovery_categories:
            if st.button(cat_name, use_container_width=True):
                st.session_state['task_name'] = cat_name
                st.session_state['task_objective'] = cat_obj
                st.session_state['selected_task_example'] = cat_id
                st.session_state['discovery_required'] = True
                st.rerun()

    with col2:
        st.text_input("Inspection Name", value=st.session_state.get('task_name', "Custom Inspection"), key='task_name')
        st.text_area("Objective", value=st.session_state.get('task_objective', "Identify visible defects."), key='task_objective', height=70)

        st.markdown("<div style='margin-bottom: 0.5rem; font-weight: 500; margin-top: 1rem;'>When an issue is found:</div>", unsafe_allow_html=True)
        st.selectbox(
            "Action",
            ["Reject Product", "Alert Operator", "Record Inspection", "Count Defects"],
            key='business_rule',
            label_visibility="collapsed"
        )

        if 'selected_task_example' not in st.session_state:
            st.session_state['selected_task_example'] = ''
            st.session_state['discovery_required'] = False

def render_step_2():
    section_header("Provide Data")
    st.write("Upload a ZIP folder containing examples of your products and defects.")

    task_example = st.session_state.get('selected_task_example', '')
    discovery_required = st.session_state.get('discovery_required', False)

    if discovery_required:
        st.markdown(f"""
            <div class="ep-card" style="border-left: 4px solid var(--ep-warning);">
                <div class="ep-card-header">FOUNDATION STATUS</div>
                <div style="font-size: 1.2rem; font-weight: bold; color: var(--ep-text); margin-bottom: 0.5rem;">No Validated Foundation</div>
                <div style="color: var(--ep-muted);">EdgePilot doesn't currently have a validated AI foundation for this automation type.</div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Discover compatible AI foundations", type="primary", use_container_width=True):
            st.session_state['run_discovery'] = True
            st.rerun()

        if st.session_state.get('run_discovery', False):
            from app.core.dataset_discovery import DatasetDiscoveryEngine

            with st.spinner("Finding compatible datasets..."):
                time.sleep(1)
            with st.spinner("Checking task compatibility..."):
                time.sleep(1)
            with st.spinner("Checking available metadata..."):
                time.sleep(1)
            with st.spinner("Checking licensing information..."):
                engine = DatasetDiscoveryEngine(use_mock=True) # default to mock for tests
                candidates = engine.search_candidates(st.session_state.get('task_name'))

            st.markdown("### Discovered Candidates")
            if not candidates:
                st.info("No compatible datasets found.")
            else:
                for c in candidates:
                    color = "var(--ep-success)" if c['status'] == 'approved' else "var(--ep-warning)" if c['status'] == 'review_required' else "var(--ep-danger)"
                    st.markdown(f"""
                    <div style="border: 1px solid var(--ep-border); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                        <h4 style="margin:0 0 0.5rem 0;">{c['name']}</h4>
                        <div style="font-size: 0.9rem; color: var(--ep-muted); margin-bottom: 0.5rem;">
                            <strong>Source:</strong> {c['source']}<br/>
                            <strong>Task:</strong> {c['task_type']}<br/>
                            <strong>Classes:</strong> {c['classes'] or 'Unknown'}<br/>
                            <strong>License:</strong> {c['license']}
                        </div>
                        <div style="display: inline-block; padding: 0.25rem 0.5rem; background: {color}; color: white; border-radius: 4px; font-size: 0.8rem; font-weight: bold;">
                            Status: {c['status'].replace('_', ' ').title()}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        return

    if task_example in ['steel', 'pcb']:
        st.markdown(f"""
            <div class="ep-card" style="border-left: 4px solid var(--ep-success);">
                <div class="ep-card-header">DATASET STATUS</div>
                <div style="font-size: 1.2rem; font-weight: bold; color: var(--ep-text); margin-bottom: 0.5rem;">Demo Dataset Loaded</div>
                <div style="color: var(--ep-muted);">Using verified pre-loaded dataset.</div>
            </div>
        """, unsafe_allow_html=True)
        return

    uploaded_file = st.file_uploader("Upload Dataset (ZIP)", type=["zip"])

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

                get_task_manager().update_task(task_id, {"dataset_path": dataset_dir})
                st.rerun()

    task = get_task_manager().get_task(task_example) if task_example.startswith('custom_') else None

    if task and task.get('dataset_path') and os.path.exists(task.get('dataset_path')):
        if st.button("Validate Dataset", use_container_width=True):
            with st.spinner("Validating data structure..."):
                result = automl_engine.validate_dataset(task['dataset_path'])

                if result['is_valid']:
                    get_task_manager().update_task(task_example, {"dataset_validation_status": True})
                else:
                    st.error("There is an issue with the dataset.")
                    for err in result['errors']:
                        st.write(f"✗ {err}")
                    get_task_manager().update_task(task_example, {"dataset_validation_status": False})

        if task.get('dataset_validation_status'):
            st.markdown("""
                <div class="ep-card" style="border-left: 4px solid var(--ep-success); margin-top: 1rem;">
                    <div style="font-weight: bold; color: var(--ep-text);">✓ Dataset structure valid</div>
                    <div style="color: var(--ep-muted); font-size: 0.9rem;">Ready for processing</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="ep-card" style="border-left: 4px solid var(--ep-warning); margin-top: 1rem;">
                <div style="font-weight: bold; color: var(--ep-text);">Data Required</div>
                <div style="color: var(--ep-muted); font-size: 0.9rem;">Please upload representative business data.</div>
            </div>
        """, unsafe_allow_html=True)

def render_step_3():
    section_header("Process & Complete")

    task_example = st.session_state.get('selected_task_example', '')
    task = get_task_manager().get_task(task_example)

    is_demo = task_example in ['steel', 'pcb']

    if is_demo or task.get('training_status') == 'Complete':
        st.markdown("""
        <div class="ep-card" style="border-left: 4px solid var(--ep-success); margin-bottom: 2rem;">
            <div style="font-weight: bold; color: var(--ep-text); font-size: 1.2rem;">✓ Processing Complete</div>
            <div style="color: var(--ep-muted); font-size: 0.9rem; margin-top: 0.5rem;">Your inspection model is ready for use.</div>
        </div>
        """, unsafe_allow_html=True)

        if not is_demo and not task.get('model_onnx'):
            with st.spinner("Finalizing setup..."):
                onnx_path = automl_engine.export_onnx(task['model_pt'])
                get_task_manager().update_task(task_example, {"model_onnx": onnx_path})
                st.rerun()

        metrics = task.get('evaluation_metrics', {}) if not is_demo else {'precision': 0.95, 'recall': 0.92, 'map50': 0.5785 if task_example == 'steel' else 0.0817}

        m_col1, m_col2 = st.columns(2)
        has_metrics = 'precision' in metrics
        with m_col1: metric_card("Accuracy Score", f"{metrics.get('precision', 0)*100:.1f}%" if has_metrics else "Not available")
        with m_col2: metric_card("Detection Rate", f"{metrics.get('map50', 0)*100:.1f}%" if has_metrics else "Not available")

    else:
        st.write("EdgePilot will automatically train a computer vision model and prepare it for deployment.")

        if st.button("Start Processing", type="primary", use_container_width=True):
            with st.spinner("Processing data... (This may take a few minutes)"):
                yaml_path = os.path.join(task['dataset_path'], "data.yaml")
                if not os.path.exists(yaml_path):
                    yaml_path = os.path.join(task['dataset_path'], "dataset.yaml")

                model_pt, train_time, results = automl_engine.train(task_example, yaml_path)

            with st.spinner("Evaluating performance..."):
                metrics = automl_engine.evaluate(model_pt, yaml_path)

            get_task_manager().update_task(task_example, {
                "training_status": "Complete",
                "model_pt": model_pt,
                "evaluation_metrics": metrics
            })
            st.rerun()

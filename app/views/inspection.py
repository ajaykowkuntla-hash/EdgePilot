import streamlit as st
import os
import zipfile
import shutil
import uuid
import glob
from app.core.task_manager import TaskManager
from app.core.registry import ModelRegistry
from app.core.adaptation_engine import AdaptationEngine
from app.ui.components import page_header, section_header, workflow_wizard

def get_task_manager():
    user = st.session_state.get("user")
    if not user:
        return None
    return TaskManager(uid=user["uid"], id_token=user["id_token"])

def reset_wizard():
    for key in ['wizard_step', 'selected_category', 'selected_task_example', 'business_examples_dir', 'adaptation_result']:
        if key in st.session_state:
            del st.session_state[key]

def next_step():
    st.session_state['wizard_step'] = min(6, st.session_state.get('wizard_step', 1) + 1)

def prev_step():
    st.session_state['wizard_step'] = max(1, st.session_state.get('wizard_step', 1) - 1)

def render():
    if 'wizard_step' not in st.session_state:
        st.session_state['wizard_step'] = 1

    step = st.session_state['wizard_step']

    page_header("INSPECTION WORKFLOW", "Create New Inspection", "Automate a repetitive visual task.")
    steps = ["Task", "Foundation", "Examples", "Adapt", "Evaluate", "Next Action"]
    workflow_wizard(current_step=step, steps=steps)

    if step == 1: render_step_1()
    elif step == 2: render_step_2()
    elif step == 3: render_step_3()
    elif step == 4: render_step_4()
    elif step == 5: render_step_5()
    elif step == 6: render_step_6()

    st.markdown("<hr/>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if 1 < step < 6:
            st.button("← Back", on_click=prev_step, use_container_width=True)
    with col3:
        if step == 2:
            st.button("Continue →", on_click=next_step, type="primary", use_container_width=True)
        elif step == 3:
            disabled = 'business_examples_dir' not in st.session_state
            st.button("Continue →", on_click=next_step, type="primary", disabled=disabled, use_container_width=True)
        elif step == 5:
            st.button("Continue →", on_click=next_step, type="primary", use_container_width=True)
        elif step == 6:
            if st.button("Finish", type="primary", use_container_width=True):
                st.session_state['current_view'] = 'Dashboard'
                reset_wizard()
                st.rerun()

def render_step_1():
    section_header("What do you want to automate?")
    registry = ModelRegistry()
    categories = registry.registry.get("categories", {})

    col1, col2 = st.columns(2)
    with col1:
        for cat_id, cat_info in categories.items():
            if st.button(cat_info.get("name"), use_container_width=True):
                st.session_state['selected_category'] = cat_id
                st.session_state['selected_task_example'] = f"custom_{uuid.uuid4().hex[:8]}"
                next_step()
                st.rerun()

def render_step_2():
    section_header("Foundation Workflow")
    st.write("EdgePilot selected a foundation workflow for this task.")

    cat_id = st.session_state.get('selected_category')
    registry = ModelRegistry()
    cat_info = registry.registry.get("categories", {}).get(cat_id, {})

    with st.expander("Technical Details"):
        st.write(f"**Model:** {cat_info.get('model', 'N/A')}")
        st.write(f"**Dataset:** {cat_info.get('dataset', 'N/A')}")
        st.write(f"**Input Size:** {cat_info.get('input_size', 'N/A')}")
        st.write(f"**Export Format:** {cat_info.get('export_format', 'N/A')}")

def render_step_3():
    section_header("Provide Examples")
    st.write("Provide representative examples. EdgePilot will evaluate whether the available examples are sufficient for adaptation.")

    uploaded_file = st.file_uploader("Upload Examples (ZIP)", type=["zip"])
    if uploaded_file:
        task_id = st.session_state.get('selected_task_example', '')
        dataset_dir = os.path.join("datasets", task_id, "business_examples")
        if not os.path.exists(dataset_dir):
            os.makedirs(dataset_dir)
            with st.spinner("Extracting..."):
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
                st.session_state['business_examples_dir'] = dataset_dir
                st.rerun()

    if 'business_examples_dir' in st.session_state:
        st.success("Business examples loaded successfully.")

def render_step_4():
    section_header("Adaptation")
    st.write("Train lightweight model using your examples combined with the foundation.")
    st.info("Note: Training and evaluation may take several minutes. Please do not close this window.")

    if st.button("Start Adaptation", type="primary", use_container_width=True, disabled=st.session_state.get('is_adapting', False)):
        st.session_state['is_adapting'] = True
        st.rerun()

    if st.session_state.get('is_adapting', False):
        task_id = st.session_state.get('selected_task_example')
        biz_dir = st.session_state.get('business_examples_dir')

        # Build business examples dict
        images = glob.glob(f"{biz_dir}/**/*.jpg", recursive=True) + glob.glob(f"{biz_dir}/**/*.png", recursive=True) if biz_dir else []
        labels = glob.glob(f"{biz_dir}/**/*.txt", recursive=True) if biz_dir else []

        biz_dict = {"images": images, "labels": labels}

        # Determine foundation yaml
        foundation_yaml = st.session_state.get('test_foundation_yaml', "datasets/NEU-DET_baseline/dataset.yaml")
        if not os.path.exists(foundation_yaml):
            st.error("Foundation dataset is unavailable for this task.")
            st.session_state['is_adapting'] = False
            return

        with st.spinner("Adapting model... (This may take several minutes)"):
            engine = AdaptationEngine(task_id)
            # Use validated Phase 22 baseline mapping
            baseline = {"map50": 0.6521}
            result = engine.adapt_and_evaluate(foundation_yaml, biz_dict, baseline)
            st.session_state['adaptation_result'] = result

        st.session_state['is_adapting'] = False
        next_step()
        st.rerun()

def render_step_5():
    section_header("Evaluation")
    res = st.session_state.get('adaptation_result', {})
    decision = res.get('decision', 'UNKNOWN')

    if decision == "ADAPTATION_SUPPORTED":
        st.markdown('<div class="ep-card" style="border-left: 4px solid var(--ep-success); font-weight: bold; font-size: 1.2rem;">ADAPTATION SUPPORTED</div>', unsafe_allow_html=True)
    elif decision == "MORE_DATA_RECOMMENDED":
        st.markdown('<div class="ep-card" style="border-left: 4px solid var(--ep-warning); font-weight: bold; font-size: 1.2rem;">MORE EXAMPLES RECOMMENDED</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="ep-card" style="border-left: 4px solid var(--ep-danger); font-weight: bold; font-size: 1.2rem;">ADAPTATION NOT SUPPORTED</div>', unsafe_allow_html=True)

    with st.expander("Technical Details"):
        metrics = res.get('metrics', {})
        st.write("**Validation Status:** Complete")
        st.write(f"**mAP50:** {metrics.get('map50', 0):.4f}")
        st.write(f"**Precision:** {metrics.get('precision', 0):.4f}")
        st.write(f"**Recall:** {metrics.get('recall', 0):.4f}")

        biz_dir = st.session_state.get('business_examples_dir', '')
        images = glob.glob(f"{biz_dir}/**/*.jpg", recursive=True) + glob.glob(f"{biz_dir}/**/*.png", recursive=True) if biz_dir else []
        st.write(f"**Examples Used:** {len(images)}")
        st.write(f"**Model Size:** {res.get('model_size_mb', 0):.2f} MB")

def render_step_6():
    section_header("Next Action")
    res = st.session_state.get('adaptation_result', {})
    decision = res.get('decision', 'UNKNOWN')

    if decision == "ADAPTATION_SUPPORTED":
        st.success("Model ready for deployment validation.")
    elif decision == "MORE_DATA_RECOMMENDED":
        st.info("Provide more representative examples and evaluate again.")
    else:
        st.error("Provide more representative examples and evaluate again.")

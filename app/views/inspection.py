import streamlit as st

def reset_wizard():
    st.session_state['wizard_step'] = 1

def next_step():
    st.session_state['wizard_step'] = min(8, st.session_state.get('wizard_step', 1) + 1)

def prev_step():
    st.session_state['wizard_step'] = max(1, st.session_state.get('wizard_step', 1) - 1)

def render():
    if 'wizard_step' not in st.session_state:
        st.session_state['wizard_step'] = 1
        
    step = st.session_state['wizard_step']
    
    st.title("Create AI Inspection")
    st.progress(step / 8.0, text=f"STEP {step} OF 8")
    
    # Render current step
    if step == 1:
        render_step_1()
    elif step == 2:
        render_step_2()
    elif step == 3:
        render_step_3()
    elif step == 4:
        render_step_4()
    elif step == 5:
        render_step_5()
    elif step == 6:
        render_step_6()
    elif step == 7:
        render_step_7()
    elif step == 8:
        render_step_8()

    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if step > 1:
            st.button("← Back", on_click=prev_step, use_container_width=True)
    with col3:
        if step < 8:
            st.button("Continue →", on_click=next_step, type="primary", use_container_width=True)
        elif step == 8:
            if st.button("Finish", type="primary", use_container_width=True):
                st.session_state['current_view'] = 'Dashboard'
                reset_wizard()
                st.rerun()

def render_step_1():
    st.subheader("What do you want to automate?")
    
    st.radio(
        "Select Business Requirement",
        ["Detect Defects", "Inspect Products (Coming Soon)", "Count Objects (Preview)", "Classify Products (Coming Soon)", "Monitor Quality (Preview)"],
        key='business_req'
    )
    
    if st.session_state['business_req'] == "Detect Defects":
        st.markdown("---")
        st.subheader("What are you inspecting?")
        st.selectbox(
            "Select Target",
            ["Metal Components", "PCB Assemblies", "Packaged Products", "Plastic Components", "Food Products", "Other"],
            key='business_target'
        )
        st.info("EdgePilot uses your inspection requirement to configure an appropriate AI workflow.")
        
def render_step_2():
    st.subheader("Define your inspection task")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Task Examples")
        st.write("Load a validated example:")
        if st.button("Steel Surface Inspection"):
            st.session_state['task_name'] = "Steel Surface Inspection"
            st.session_state['task_objective'] = "Identify visible surface defects in steel components."
            st.session_state['selected_task_example'] = 'steel'
        if st.button("PCB Defect Inspection"):
            st.session_state['task_name'] = "PCB Defect Inspection"
            st.session_state['task_objective'] = "Detect manufacturing defects on PCBs."
            st.session_state['selected_task_example'] = 'pcb'
            
    with col2:
        st.text_input("Task Name", value=st.session_state.get('task_name', "Steel Surface Inspection"), key='task_name')
        st.text_area("Inspection Objective", value=st.session_state.get('task_objective', "Identify visible surface defects in steel components."), key='task_objective')
        
        st.write("**Capability:** Object Detection")
        st.caption("EdgePilot will locate defects and identify their type.")
        
    st.markdown("---")
    st.info("Different businesses require different AI models. EdgePilot provides a common workflow for preparing and deploying task-specific models.")

def render_step_3():
    st.subheader("Provide representative inspection data")
    st.write("Your business data teaches EdgePilot what your products, normal samples, and defects look like.")
    
    uploaded_files = st.file_uploader("Upload Images (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    
    st.markdown("#### Why business data is required")
    c1, c2, c3 = st.columns(3)
    c1.info("Different products")
    c2.info("Camera setups vary")
    c3.info("Defect appearance varies")
    
    st.write("*Public datasets can demonstrate the workflow, but business-specific data is required for a model tailored to a specific production environment.*")
    
    st.markdown("---")
    st.markdown("#### Dataset Status")
    
    task_example = st.session_state.get('selected_task_example', '')
    if task_example in ['steel', 'pcb']:
        st.success("Demo Dataset Available")
    elif uploaded_files:
        st.success("Uploaded Data Available")
    else:
        st.warning("Business Data Required")
        
    st.markdown("---")
    st.markdown("#### AI-Assisted Labeling (Preview / Planned)")
    st.info("EdgePilot can assist users by suggesting labels that humans verify and correct before training.")

def render_step_4():
    st.subheader("What should happen when a defect is detected?")
    
    st.radio(
        "Business Rule",
        ["Reject Product", "Alert Operator", "Record Inspection", "Count Defects"],
        key='business_rule'
    )
    
    st.markdown("#### Inspection Sensitivity")
    st.select_slider("Sensitivity", options=["Low", "Standard", "High"], value="Standard", key='inspection_sensitivity')
    
    st.markdown("---")
    st.subheader("Business Decision:")
    rule = st.session_state['business_rule']
    if rule == "Reject Product":
        st.error("REJECT")
    elif rule == "Alert Operator":
        st.warning("ALERT")
    elif rule == "Count Defects":
        st.info("COUNT")
    else:
        st.success("PASS")
        
def render_step_5():
    st.subheader("EdgePilot prepares the AI workflow")
    
    st.markdown("""
    **Business Requirement**  
    ↓  
    **Task Configuration**  
    ↓  
    **Dataset Preparation**  
    ↓  
    **Model Template**  
    ↓  
    **Training Configuration**  
    ↓  
    **Evaluation**  
    ↓  
    **ONNX Export**  
    """)
    
    with st.expander("Advanced technical details"):
        st.write("**Model Template:** YOLOv8-N Object Detection")
        st.write("**Input:** 640 × 640")
        st.write("**Export:** ONNX")
        st.write("**Training:** Fixed MVP configuration")
        st.caption("EdgePilot currently supports a constrained set of predefined AI templates rather than arbitrary AutoML.")

def render_step_6():
    st.subheader("Train and evaluate your inspection model")
    
    task_example = st.session_state.get('selected_task_example', '')
    
    if task_example == 'steel':
        st.info("**Steel Surface Inspection**")
        st.write("**Dataset:** NEU-DET")
        st.write("**Classes:** 6")
        st.write("**Training:** 5 epoch development baseline")
        st.write("**mAP@50:** 57.85%")
        st.write("**mAP@50-95:** 27.53%")
        st.caption("Development Baseline - These metrics demonstrate the development pipeline and are not production validation.")
        
        st.button("Train Model", disabled=True)
        
    elif task_example == 'pcb':
        st.info("**PCB Defect Inspection**")
        st.write("**Dataset:** DeepPCB")
        st.write("**Classes:** 6")
        st.write("**Training:** 5 epoch miniature validation")
        st.write("**mAP@50:** 8.17%")
        st.write("**mAP@50-95:** 4.11%")
        st.caption("Miniature Pipeline Validation - This experiment validates cross-domain pipeline execution; accuracy is not production-ready.")
        
        st.button("Train Model", disabled=True)
    else:
        st.warning("Representative business data is required before training.")
        st.write("Upload representative business data to train a new task.")
        st.button("Train Model", disabled=True)

def render_step_7():
    st.subheader("Validate edge deployment")
    
    st.markdown("""
    **Trained Model**  
    ↓  
    **ONNX**  
    ↓  
    **Qualcomm AI Hub**  
    ↓  
    **Snapdragon X Elite**  
    ↓  
    **NPU**  
    """)
    
    task_example = st.session_state.get('selected_task_example', '')
    
    st.markdown("---")
    
    if task_example == 'steel':
        st.info("**Steel Surface Inspection**")
        st.write("**Device:** Snapdragon X Elite CRD")
        st.write("**Runtime:** ONNX")
        st.write("**Precision:** FP16")
        st.write("**Compute:** NPU")
        st.write("**Latency:** 5.849 ms")
        st.write("**Memory:** ~4.73 MB")
        st.success("✓ Snapdragon NPU Validated")
    elif task_example == 'pcb':
        st.info("**PCB Defect Inspection**")
        st.write("**Device:** Snapdragon X Elite CRD")
        st.write("**Runtime:** ONNX")
        st.write("**Precision:** FP16")
        st.write("**Compute:** NPU")
        st.write("**Latency:** 5.817 ms")
        st.write("**Memory:** 36.16 MB")
        st.success("✓ Snapdragon NPU Validated")
    else:
        st.warning("No model available to validate yet.")
        
    st.markdown("---")
    st.error("Qualcomm AI Hub hosted-device validation")
    st.caption("Physical Snapdragon hardware validation has not been performed in this prototype.")

def render_step_8():
    st.subheader("Inspection Ready — Development Demonstration")
    
    task_name = st.session_state.get('task_name', 'Inspection')
    rule = st.session_state.get('business_rule', 'Reject Product')
    
    st.write(f"**Task:** {task_name}")
    st.write("**AI Capability:** Object Detection")
    st.write("**Model:** EdgePilot YOLOv8-N")
    st.write("**Deployment:** Snapdragon X Elite NPU deployment path validated through Qualcomm AI Hub.")
    st.write(f"**Business Rule:** {rule}")
    
    st.markdown("---")
    
    task_example = st.session_state.get('selected_task_example', '')
    if task_example == 'steel':
        st.info("Demo Result (using pitted_surface_277.jpg)")
        
        import os
        from app.utils.inference import run_inference
        from app.core.decision_engine import evaluate_inspection
        
        demo_image_path = "phase2/dataset/test/images/pitted_surface_277.jpg"
        if os.path.exists(demo_image_path):
            with open(demo_image_path, "rb") as f:
                image_bytes = f.read()
            with st.spinner("Running local inference..."):
                result = run_inference(image_bytes, 0.70)
            
            if "error" not in result:
                decision, details = evaluate_inspection(result['detections'], 0.70, rule)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.image(result['annotated_image'], caption="AI Detection Overlay", use_container_width=True)
                with col2:
                    if result['detections']:
                        d = result['detections'][0]
                        st.write(f"**Detected:** {d['class'].replace('_', ' ').title()}")
                        st.write(f"**Confidence:** approximately {int(d['confidence']*100)}%")
                        st.write(f"**Detection:** {len(result['detections'])}")
                    
                    if decision == "REJECT":
                        st.error("**Decision:** REJECT")
                    else:
                        st.success(f"**Decision:** {decision}")
        else:
            st.warning("Demo image not found.")
            
        st.caption("Development demonstration")
        st.caption("Local ONNX inference on the development machine; Snapdragon NPU deployment separately validated through Qualcomm AI Hub.")
        st.caption("Physical Snapdragon hardware validation has not been performed in this prototype.")
    else:
        st.info("Simulation mode for task without real demo images.")

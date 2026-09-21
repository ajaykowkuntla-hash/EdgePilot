import streamlit as st

def render():
    st.title("EDGE PILOT")
    st.markdown("### AI Automation, Built for the Edge.")
    st.markdown("Configure task-specific AI inspection workflows, prepare models, and validate edge deployment on Snapdragon-powered systems.")
    
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
    st.subheader("Active Tasks")
    
    c1, c2 = st.columns(2)
    with c1:
        st.info("**Steel Surface Inspection**")
        st.write("**Objective:** Detect surface defects in steel.")
        st.write("**Capability:** Object Detection")
        st.success("**Status:** Snapdragon Validated")
        if st.button("View Details", key="btn_steel"):
            st.session_state['selected_existing_task'] = 'steel'
            st.session_state['current_view'] = 'Task Detail'
            st.rerun()
            
    with c2:
        st.info("**PCB Defect Inspection**")
        st.write("**Objective:** Detect manufacturing defects on PCBs.")
        st.write("**Capability:** Object Detection")
        st.success("**Status:** Snapdragon Validated")
        if st.button("View Details", key="btn_pcb"):
            st.session_state['selected_existing_task'] = 'pcb'
            st.session_state['current_view'] = 'Task Detail'
            st.rerun()
            
    st.caption("*Note: These are Validated Examples (Development Validation), not production deployments.*")

    st.markdown("---")
    st.subheader("How EdgePilot Works")
    st.markdown("""
    **1.** Define business requirement  
    **2.** Provide representative data  
    **3.** Configure inspection rule  
    **4.** EdgePilot prepares the AI workflow  
    **5.** Train and evaluate  
    **6.** Export ONNX  
    **7.** Validate Snapdragon deployment  
    **8.** Execute business decision  
    """)

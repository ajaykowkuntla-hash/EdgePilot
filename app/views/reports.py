import streamlit as st
from app.ui.components import page_header, section_header, evidence_card, metric_card

def render():
    page_header(
        eyebrow="REPORTS",
        title="Inspection Reports",
        description="Review historical inspection data and detailed technical performance."
    )

    # Time filter mock
    st.markdown("""
        <div style="display: flex; gap: 1rem; margin-bottom: 2rem;">
            <button style="background-color: var(--ep-surface); border: 1px solid var(--ep-accent); color: var(--ep-accent); padding: 0.5rem 1rem; border-radius: 8px; font-weight: 500;">Today</button>
            <button style="background-color: var(--ep-surface-2); border: 1px solid var(--ep-border); color: var(--ep-muted); padding: 0.5rem 1rem; border-radius: 8px;">This Week</button>
            <button style="background-color: var(--ep-surface-2); border: 1px solid var(--ep-border); color: var(--ep-muted); padding: 0.5rem 1rem; border-radius: 8px;">This Month</button>
            <button style="background-color: var(--ep-surface-2); border: 1px solid var(--ep-border); color: var(--ep-muted); padding: 0.5rem 1rem; border-radius: 8px;">Custom</button>
        </div>
    """, unsafe_allow_html=True)

    section_header("Summary")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("ITEMS INSPECTED", "1,248")
    with col2:
        metric_card("PASS RATE", "96.2%")
    with col3:
        metric_card("ISSUES FOUND", "47")
    with col4:
        metric_card("AVG PROCESSING TIME", "3.2 sec")

    section_header("Inspection History")

    from app.core.task_manager import TaskManager
    task_manager = TaskManager(
        uid=st.session_state.user["uid"],
        id_token=st.session_state.user["id_token"]
    )

    tasks = task_manager.list_tasks()
    deployed_tasks = [t for t in tasks if t.get("status") == "deployed"]

    st.markdown('<div class="ep-card" style="padding: 0; overflow: hidden;">', unsafe_allow_html=True)
    st.markdown("""
        <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.9rem;">
            <thead>
                <tr style="border-bottom: 1px solid var(--ep-border); color: var(--ep-muted); background-color: var(--ep-surface-2);">
                    <th style="padding: 1rem;">Task ID</th>
                    <th style="padding: 1rem;">Name</th>
                    <th style="padding: 1rem;">Status</th>
                    <th style="padding: 1rem;">Validation</th>
                </tr>
            </thead>
            <tbody style="color: var(--ep-text);">
    """, unsafe_allow_html=True)

    if deployed_tasks:
        for t in deployed_tasks:
            t_id = t.get("id", "")
            t_name = t.get("name", "Unknown")
            status = '<span class="ep-badge success">✓ Complete</span>'
            val = t.get("snapdragon", "Unknown")

            st.markdown(f"""
                <tr style="border-bottom: 1px solid var(--ep-border);">
                    <td style="padding: 1rem;">{t_id}</td>
                    <td style="padding: 1rem;">{t_name}</td>
                    <td style="padding: 1rem;">{status}</td>
                    <td style="padding: 1rem;">{val}</td>
                </tr>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <tr>
                <td colspan="4" style="padding: 1rem; text-align: center; color: var(--ep-muted);">No deployed inspections found.</td>
            </tr>
        """, unsafe_allow_html=True)

    st.markdown("""
            </tbody>
        </table>
        <div style="padding: 1rem; text-align: center; font-size: 0.8rem; color: var(--ep-muted); border-top: 1px solid var(--ep-border); background-color: var(--ep-bg);">
            Synced from Cloud
        </div>
    </div>
    """, unsafe_allow_html=True)

    section_header("Live Inspection Results")
    reports = task_manager.list_reports()
    
    st.markdown('<div class="ep-card" style="padding: 0; overflow: hidden;">', unsafe_allow_html=True)
    st.markdown("""
        <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.9rem;">
            <thead>
                <tr style="border-bottom: 1px solid var(--ep-border); color: var(--ep-muted); background-color: var(--ep-surface-2);">
                    <th style="padding: 1rem;">Date</th>
                    <th style="padding: 1rem;">Task</th>
                    <th style="padding: 1rem;">Input Type</th>
                    <th style="padding: 1rem;">Result</th>
                </tr>
            </thead>
            <tbody style="color: var(--ep-text);">
    """, unsafe_allow_html=True)
    
    if reports:
        for r in reports:
            st.markdown(f"""
                <tr style="border-bottom: 1px solid var(--ep-border);">
                    <td style="padding: 1rem;">{r.get('date_time', 'Unknown')}</td>
                    <td style="padding: 1rem;">{r.get('task', 'Unknown')}</td>
                    <td style="padding: 1rem;">{r.get('input_type', 'Unknown')}</td>
                    <td style="padding: 1rem;">{r.get('result', 'Unknown')}</td>
                </tr>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <tr>
                <td colspan="4" style="padding: 1rem; text-align: center; color: var(--ep-muted);">No live inspection reports found.</td>
            </tr>
        """, unsafe_allow_html=True)
        
    st.markdown("""
            </tbody>
        </table>
        <div style="padding: 1rem; text-align: center; font-size: 0.8rem; color: var(--ep-muted); border-top: 1px solid var(--ep-border); background-color: var(--ep-bg);">
            Synced from Cloud
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("TECHNICAL DETAILS"):
        st.markdown("<h3 style='margin-top: 1rem;'>Hardware Validation & Scope</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: var(--ep-muted);'>EdgePilot compiles and profiles ONNX models against the Snapdragon X Elite NPU.</p>", unsafe_allow_html=True)

        # Evidence.py contents
        ecol1, ecol2 = st.columns(2)
        with ecol1:
            st.markdown("""
                <div class="ep-card" style="border-top: 4px solid var(--ep-success); height: 100%;">
                    <div class="ep-card-header">VERIFIED</div>
                    <h4 style="margin-top: 0; margin-bottom: 1.5rem; color: var(--ep-text);">Functional Scope</h4>
                    <div style="display: flex; flex-direction: column; gap: 1rem;">
                        <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                            <span style="color: var(--ep-success); font-weight: bold;">✓</span>
                            <span style="color: var(--ep-text);">Real AutoML training (YOLOv8-N)</span>
                        </div>
                        <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                            <span style="color: var(--ep-success); font-weight: bold;">✓</span>
                            <span style="color: var(--ep-text);">ONNX export capabilities</span>
                        </div>
                        <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                            <span style="color: var(--ep-success); font-weight: bold;">✓</span>
                            <span style="color: var(--ep-text);">Local ONNX inference</span>
                        </div>
                        <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                            <span style="color: var(--ep-success); font-weight: bold;">✓</span>
                            <span style="color: var(--ep-text);">Qualcomm AI Hub NPU validation</span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with ecol2:
            st.markdown("""
                <div class="ep-card" style="border-top: 4px solid var(--ep-warning); height: 100%;">
                    <div class="ep-card-header">SCOPE</div>
                    <h4 style="margin-top: 0; margin-bottom: 1.5rem; color: var(--ep-text);">MVP Limitations</h4>
                    <div style="display: flex; flex-direction: column; gap: 1rem;">
                        <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                            <span style="color: var(--ep-warning); font-weight: bold;">!</span>
                            <span style="color: var(--ep-text);">Hosted Qualcomm validation only</span>
                        </div>
                        <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                            <span style="color: var(--ep-warning); font-weight: bold;">!</span>
                            <span style="color: var(--ep-text);">No physical Snapdragon laptop testing</span>
                        </div>
                        <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                            <span style="color: var(--ep-warning); font-weight: bold;">!</span>
                            <span style="color: var(--ep-text);">No factory production validation</span>
                        </div>
                        <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                            <span style="color: var(--ep-warning); font-weight: bold;">!</span>
                            <span style="color: var(--ep-text);">No production accuracy claim</span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr/>", unsafe_allow_html=True)
        st.markdown("<h4>Current Validation</h4>", unsafe_allow_html=True)

        evidence_card(
            title="Phase 12 Pipeline",
            hardware="Snapdragon X Elite CRD",
            runtime="ONNX",
            compute="NPU",
            latency="5.804 ms",
            memory="4.75 MB"
        )

        st.markdown("<h4>Historical Validations</h4>", unsafe_allow_html=True)

        vcol1, vcol2 = st.columns(2)
        with vcol1:
            evidence_card(
                title="NEU-DET (Task A)",
                hardware="Snapdragon X Elite CRD",
                runtime="ONNX",
                compute="NPU",
                latency="5.849 ms",
                memory="~4.73 MB"
            )
        with vcol2:
            evidence_card(
                title="DeepPCB (Task B)",
                hardware="Snapdragon X Elite CRD",
                runtime="ONNX",
                compute="NPU",
                latency="5.817 ms",
                memory="36.16 MB"
            )

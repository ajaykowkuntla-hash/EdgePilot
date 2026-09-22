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

    st.markdown("""
        <div class="ep-card" style="padding: 0; overflow: hidden;">
            <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.9rem;">
                <thead>
                    <tr style="border-bottom: 1px solid var(--ep-border); color: var(--ep-muted); background-color: var(--ep-surface-2);">
                        <th style="padding: 1rem;">Time</th>
                        <th style="padding: 1rem;">Inspection</th>
                        <th style="padding: 1rem;">Items</th>
                        <th style="padding: 1rem;">Result</th>
                        <th style="padding: 1rem;">Duration</th>
                    </tr>
                </thead>
                <tbody style="color: var(--ep-text);">
                    <tr style="border-bottom: 1px solid var(--ep-border);">
                        <td style="padding: 1rem;">10:42 AM</td>
                        <td style="padding: 1rem;">Batch #1042</td>
                        <td style="padding: 1rem;">240</td>
                        <td style="padding: 1rem;"><span class="ep-badge success">✓ Complete</span></td>
                        <td style="padding: 1rem;">03:12</td>
                    </tr>
                    <tr style="border-bottom: 1px solid var(--ep-border);">
                        <td style="padding: 1rem;">10:35 AM</td>
                        <td style="padding: 1rem;">Batch #1041</td>
                        <td style="padding: 1rem;">180</td>
                        <td style="padding: 1rem;"><span class="ep-badge success">✓ Complete</span></td>
                        <td style="padding: 1rem;">02:41</td>
                    </tr>
                    <tr>
                        <td style="padding: 1rem;">10:21 AM</td>
                        <td style="padding: 1rem;">Batch #1040</td>
                        <td style="padding: 1rem;">195</td>
                        <td style="padding: 1rem;"><span class="ep-badge warning">⚠ 3 Issues</span></td>
                        <td style="padding: 1rem;">02:58</td>
                    </tr>
                </tbody>
            </table>
            <div style="padding: 1rem; text-align: center; font-size: 0.8rem; color: var(--ep-muted); border-top: 1px solid var(--ep-border); background-color: var(--ep-bg);">
                DEMO DATA
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

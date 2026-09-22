import streamlit as st

def page_header(eyebrow, title, subtitle="", description=""):
    sub = f'<h3 style="color: var(--ep-text); font-weight: 400; margin-top: 0.5rem;">{subtitle}</h3>' if subtitle else ''
    desc = f'<p style="color: var(--ep-muted); font-size: 1.1rem; max-width: 600px; margin-top: 1rem;">{description}</p>' if description else ''
    html = f'<div style="margin-bottom: 2rem;"><div class="ep-card-header" style="color: var(--ep-accent);">{eyebrow}</div><h1 style="font-size: 3rem; font-weight: 800; margin: 0; padding: 0; line-height: 1.1;">{title}</h1>{sub}{desc}</div>'
    st.markdown(html, unsafe_allow_html=True)

def section_header(title):
    html = f'<h4 style="margin-top: 2rem; margin-bottom: 1rem; font-weight: 600; color: var(--ep-text); border-bottom: 1px solid var(--ep-border); padding-bottom: 0.5rem;">{title}</h4>'
    st.markdown(html, unsafe_allow_html=True)

def status_badge(text, status="success"):
    return f'<span class="ep-badge {status}">{text}</span>'

def feature_card(number, title, description):
    html = f'<div class="ep-card"><div class="ep-card-header" style="color: var(--ep-muted); font-size: 1.2rem; margin-bottom: 0.5rem;">{number}</div><div style="font-weight: 600; font-size: 1.1rem; margin-bottom: 0.5rem; color: var(--ep-text);">{title}</div><div style="color: var(--ep-muted); font-size: 0.9rem;">{description}</div></div>'
    st.markdown(html, unsafe_allow_html=True)

def task_card(title, domain, model, deployment, badge_text):
    html = f'<div class="ep-card" style="border-top: 4px solid var(--ep-accent);"><div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;"><div style="font-weight: bold; font-size: 1.2rem; color: var(--ep-text);">{title}</div><span class="ep-badge success">{badge_text}</span></div><div style="display: flex; gap: 1rem; color: var(--ep-muted); font-size: 0.9rem; margin-bottom: 1rem;"><div><strong>Domain:</strong> {domain}</div><div><strong>Model:</strong> {model}</div><div><strong>Target:</strong> {deployment}</div></div></div>'
    st.markdown(html, unsafe_allow_html=True)

def metric_card(label, value):
    html = f'<div class="ep-card" style="text-align: center;"><div class="ep-card-header">{label}</div><div style="font-size: 1.5rem; font-weight: bold; color: var(--ep-text); margin-top: 0.5rem;">{value}</div></div>'
    st.markdown(html, unsafe_allow_html=True)

def workflow_wizard(current_step):
    steps = ["Req", "Task", "Data", "Rule", "AI", "Train", "ONNX", "Ready"]
    html = '<div style="display: flex; align-items: center; justify-content: space-between; margin: 2rem 0; padding: 1rem; background-color: var(--ep-surface-2); border-radius: 6px;">'
    for i, step in enumerate(steps):
        step_num = i + 1
        status = "success" if step_num < current_step else "active" if step_num == current_step else "neutral"
        icon = "✓" if step_num < current_step else str(step_num)
        html += f'<div class="ep-wizard-step {status}"><span style="font-family: var(--ep-mono);">{icon}</span> {step}</div>'
        if i < len(steps) - 1:
            html += '<div class="ep-step-separator">›</div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

def pipeline_visual(nodes=None):
    if not nodes:
        nodes = ["BUSINESS REQUIREMENT", "TASK-SPECIFIC AI", "ONNX", "SNAPDRAGON NPU", "BUSINESS DECISION"]
    html = '<div style="display: flex; flex-direction: row; align-items: center; justify-content: space-between; flex-wrap: nowrap; overflow-x: auto; padding: 1rem 0; gap: 0.5rem; margin-bottom: 2rem;">'
    for i, node in enumerate(nodes):
        html += f'<div style="background-color: var(--ep-surface-2); border: 1px solid var(--ep-accent); color: var(--ep-accent); padding: 0.75rem 1rem; border-radius: 4px; font-size: 0.8rem; font-weight: 600; text-align: center; white-space: nowrap; flex: 1;">{node}</div>'
        if i < len(nodes) - 1:
            html += '<div style="color: var(--ep-muted); font-size: 1.2rem; display: flex; align-items: center;">→</div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

def evidence_card(title, hardware, runtime, compute, latency, memory):
    html = f'<div class="ep-card"><div class="ep-card-header">{title}</div><div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: 1rem;"><div style="display: flex; flex-direction: column; gap: 0.5rem;"><div style="color: var(--ep-text);"><strong>HW:</strong> {hardware}</div><div style="color: var(--ep-text);"><strong>RT:</strong> {runtime}</div><div style="color: var(--ep-text);"><strong>COMPUTE:</strong> {compute}</div></div><div style="text-align: right;"><div style="color: var(--ep-success); font-size: 2rem; font-weight: bold; line-height: 1;">{latency}</div><div style="color: var(--ep-muted); font-size: 0.9rem; margin-top: 0.25rem;">Latency</div><div style="color: var(--ep-accent); font-size: 1.5rem; font-weight: bold; line-height: 1; margin-top: 1rem;">{memory}</div><div style="color: var(--ep-muted); font-size: 0.9rem; margin-top: 0.25rem;">Peak Memory</div></div></div></div>'
    st.markdown(html, unsafe_allow_html=True)

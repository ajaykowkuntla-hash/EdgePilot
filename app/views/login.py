import streamlit as st

def render():
    st.markdown("""
        <div style="text-align: center; margin-top: 4rem; margin-bottom: 2rem;">
            <h1 style="font-weight: 800; font-size: 2.5rem; letter-spacing: -0.05em; color: var(--ep-text);">EDGE PILOT</h1>
            <p style="color: var(--ep-muted); font-size: 1.1rem;">AI automation made simple.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="ep-card">', unsafe_allow_html=True)
        
        st.markdown('<div class="ep-card-header" style="text-align: center; margin-bottom: 1.5rem;">Log in to your account</div>', unsafe_allow_html=True)
        
        st.text_input("Email", placeholder="name@company.com", key="login_email")
        st.text_input("Password", placeholder="••••••••", type="password", key="login_password")
        
        st.write("")
        
        if st.button("Sign in", use_container_width=True, type="primary"):
            st.session_state['authenticated'] = True
            st.rerun()
            
        st.markdown("""
            <div style="text-align: center; margin: 1.5rem 0;">
                <span style="color: var(--ep-muted); font-size: 0.85rem; background-color: var(--ep-surface); padding: 0 10px; position: relative; z-index: 1;">or</span>
                <hr style="margin-top: -15px; border-top: 1px solid var(--ep-border);">
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div style="background-color: rgba(245, 158, 11, 0.1); border-left: 4px solid var(--ep-warning); padding: 1rem; border-radius: 4px; margin-bottom: 1rem;">
                <p style="margin: 0; font-size: 0.85rem; color: var(--ep-text); font-weight: 500;">Prototype authentication</p>
                <p style="margin: 0; font-size: 0.75rem; color: var(--ep-muted);">Firebase authentication not configured</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Continue with Google", use_container_width=True):
            st.session_state['authenticated'] = True
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("""
            <div style="text-align: center; margin-top: 1rem;">
                <p style="font-size: 0.85rem; color: var(--ep-muted);">Don't have an account? <span style="color: var(--ep-accent); font-weight: 500; cursor: pointer;">Create account</span></p>
            </div>
        """, unsafe_allow_html=True)

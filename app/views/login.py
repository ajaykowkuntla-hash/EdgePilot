import streamlit as st
from app.core.auth import sign_in_with_email_password, sign_up_with_email_password, send_password_reset_email, get_google_auth_url

def render():
    if 'auth_mode' not in st.session_state:
        st.session_state['auth_mode'] = 'Sign in'
    if 'auth_msg' not in st.session_state:
        st.session_state['auth_msg'] = None
    if 'auth_msg_type' not in st.session_state:
        st.session_state['auth_msg_type'] = None

    st.markdown("""
<style>
/* Base and Background */
.stApp {
    background-color: #f8fafc;
    background-image: radial-gradient(circle at 100% 0%, #e0e7ff 0%, transparent 40%), radial-gradient(circle at 0% 100%, #e0e7ff 0%, transparent 40%);
    background-attachment: fixed;
}
.block-container {
    max-width: 1000px !important;
    padding-top: 5rem;
    padding-bottom: 2rem;
}
* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

/* Left Panel */
.left-panel {
    padding: 1rem 3rem 1rem 0;
    display: flex;
    flex-direction: column;
    justify-content: center;
    height: 100%;
}
.brand-logo {
    font-weight: 800;
    font-size: 1.5rem;
    letter-spacing: -0.02em;
    margin-bottom: 2rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.brand-logo .edge { color: #111827; }
.brand-logo .pilot { color: #2563eb; }
.hero-headline {
    font-weight: 800;
    font-size: 2.8rem;
    line-height: 1.1;
    letter-spacing: -0.03em;
    color: #111827;
    margin-bottom: 1.2rem;
    margin-top: 0;
}
.hero-sub {
    color: #4b5563;
    font-size: 1.05rem;
    line-height: 1.6;
    margin-bottom: 3rem;
    max-width: 95%;
}
.benefit-item {
    display: flex;
    align-items: flex-start;
    margin-bottom: 1.75rem;
    gap: 1rem;
}
.benefit-icon {
    width: 24px;
    height: 24px;
    color: #3b82f6;
    margin-top: 2px;
}
.benefit-text h4 {
    margin: 0 0 0.25rem 0;
    font-weight: 700;
    color: #111827;
    font-size: 0.95rem;
}
.benefit-text p {
    margin: 0;
    color: #6b7280;
    font-size: 0.85rem;
    line-height: 1.4;
}

/* Auth Card Wrapper */
div[data-testid="column"]:nth-child(2) {
    background-color: #ffffff !important;
    border-radius: 16px !important;
    padding: 2.5rem !important;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01) !important;
    border: 1px solid #f1f5f9 !important;
}

/* Auth Headings */
.auth-title {
    font-size: 1.5rem;
    font-weight: 800;
    color: #111827;
    margin-bottom: 0.25rem;
    margin-top: 0rem;
    letter-spacing: -0.02em;
}
.auth-subtitle {
    font-size: 0.9rem;
    color: #6b7280;
    margin-bottom: 2rem;
}

/* Inputs */
div[data-baseweb="input"] {
    border-radius: 8px !important;
    border: 1px solid #e2e8f0 !important;
    background-color: #ffffff !important;
    transition: all 0.2s;
}
div[data-baseweb="input"]:focus-within {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 1px #3b82f6 !important;
}
.stTextInput label {
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    color: #334155 !important;
    margin-bottom: 0.25rem !important;
}

/* Primary Button overriding */
div[data-testid="stButton"] button[kind="primary"] {
    background-color: #2563eb !important;
    color: white !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 0.6rem !important;
    border: none !important;
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
    width: 100% !important;
    transition: background-color 0.2s;
}
div[data-testid="stButton"] button[kind="primary"]:hover {
    background-color: #1d4ed8 !important;
}

/* Link-style Buttons */
div[data-testid="stButton"] button[kind="secondary"] {
    background: transparent !important;
    border: none !important;
    color: #4b5563 !important;
    padding: 0 !important;
    box-shadow: none !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    display: flex !important;
    justify-content: center !important;
    width: 100% !important;
}
div[data-testid="stButton"] button[kind="secondary"]:hover {
    color: #2563eb !important;
}

/* Forgot Password specific targeting */
div[data-testid="column"]:nth-child(2) div[data-testid="stHorizontalBlock"] div[data-testid="column"]:nth-child(2) div[data-testid="stButton"] button[kind="secondary"] {
    justify-content: flex-end !important;
    color: #2563eb !important;
}

/* Divider */
.auth-divider {
    text-align: center;
    margin: 1.5rem 0;
    position: relative;
}
.auth-divider span {
    color: #94a3b8;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0 12px;
    background-color: #ffffff;
    position: relative;
    z-index: 1;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.auth-divider hr {
    margin-top: -0.65rem;
    border: 0;
    border-top: 1px solid #e2e8f0;
}

/* Inline alerts */
.inline-alert {
    padding: 0.75rem 1rem;
    border-radius: 8px;
    font-size: 0.85rem;
    margin-bottom: 1.2rem;
    font-weight: 500;
}
.inline-alert-error { background-color: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }
.inline-alert-success { background-color: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; }

/* Responsive Adjustments */
@media (max-width: 768px) {
    div[data-testid="column"]:nth-child(1) {
        display: none !important; /* Hide left panel on mobile to keep login centered */
    }
    div[data-testid="column"]:nth-child(2) {
        margin: 0 auto !important;
        width: 100% !important;
        padding: 1.5rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        # Strict single line HTML to completely prevent Streamlit Markdown interference
        st.markdown("""<div class="left-panel"><div class="brand-logo"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 2L2 22H22L12 2Z" fill="#3b82f6" fill-opacity="0.2"/><path d="M12 2L2 22H12V2Z" fill="#3b82f6"/></svg><span><span class="edge">EDGE</span><span class="pilot">PILOT</span></span></div><h1 class="hero-headline">AI automation made simple.</h1><p class="hero-sub">EdgePilot helps you run industrial inspections, analyse data and generate insights — all in one simple platform.</p><div class="benefit-item"><div class="benefit-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg></div><div class="benefit-text"><h4>Smart inspections</h4><p>AI-powered analysis for industrial inspection tasks</p></div></div><div class="benefit-item"><div class="benefit-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg></div><div class="benefit-text"><h4>Organised reports</h4><p>Keep inspections and results in one place</p></div></div><div class="benefit-item"><div class="benefit-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg></div><div class="benefit-text"><h4>Secure by design</h4><p>Your business data stays safely associated with your account</p></div></div></div>""", unsafe_allow_html=True)

    with col_right:
        mode = st.session_state['auth_mode']

        def show_msg():
            if st.session_state.get('auth_msg'):
                msg = st.session_state['auth_msg']
                mtype = st.session_state['auth_msg_type']
                st.markdown(f'<div class="inline-alert inline-alert-{mtype}">{msg}</div>', unsafe_allow_html=True)
                st.session_state['auth_msg'] = None

        if mode == 'Sign in':
            st.markdown('<div class="auth-title">Welcome back</div>', unsafe_allow_html=True)
            st.markdown('<div class="auth-subtitle">Sign in to your EdgePilot account</div>', unsafe_allow_html=True)

            show_msg()

            email = st.text_input("Email", placeholder="you@example.com", key="login_email")
            password = st.text_input("Password", placeholder="Enter your password", type="password", key="login_password")

            st.write("")
            fcol1, fcol2 = st.columns([1, 1])
            with fcol2:
                if st.button("Forgot password?", use_container_width=True, type="secondary"):
                    st.session_state['auth_mode'] = 'reset'
                    st.rerun()

            st.write("")
            if st.button("Sign in →", type="primary"):
                if email and password:
                    try:
                        with st.spinner("Signing in..."):
                            result = sign_in_with_email_password(email, password)
                            st.session_state['authenticated'] = True
                            st.session_state['user'] = {
                                "uid": result["localId"],
                                "email": result.get("email", ""),
                                "display_name": result.get("displayName", ""),
                                "id_token": result["idToken"],
                                "refresh_token": result["refreshToken"]
                            }
                        st.rerun()
                    except Exception as e:
                        err_str = str(e)
                        if "INVALID_LOGIN_CREDENTIALS" in err_str or "INVALID_PASSWORD" in err_str or "EMAIL_NOT_FOUND" in err_str:
                            st.session_state['auth_msg'] = "Incorrect email or password."
                        else:
                            st.session_state['auth_msg'] = "Network or authentication error occurred."
                        st.session_state['auth_msg_type'] = "error"
                        st.rerun()
                else:
                    st.session_state['auth_msg'] = "Please enter email and password."
                    st.session_state['auth_msg_type'] = "error"
                    st.rerun()

        elif mode == 'Create account':
            st.markdown('<div class="auth-title">Create your account</div>', unsafe_allow_html=True)
            st.markdown('<div class="auth-subtitle">Set up your EdgePilot workspace</div>', unsafe_allow_html=True)

            show_msg()

            name = st.text_input("Name", placeholder="Jane Doe", key="signup_name")
            email = st.text_input("Email", placeholder="you@example.com", key="signup_email")
            password = st.text_input("Password", placeholder="Create a password", type="password", key="signup_password")
            confirm = st.text_input("Confirm password", placeholder="Confirm your password", type="password", key="signup_confirm")

            st.write("")
            if st.button("Create account", type="primary"):
                if not email or not password or not name:
                    st.session_state['auth_msg'] = "Please fill all required fields."
                    st.session_state['auth_msg_type'] = "error"
                    st.rerun()
                elif password != confirm:
                    st.session_state['auth_msg'] = "Passwords do not match."
                    st.session_state['auth_msg_type'] = "error"
                    st.rerun()
                elif len(password) < 6:
                    st.session_state['auth_msg'] = "Password should be at least 6 characters."
                    st.session_state['auth_msg_type'] = "error"
                    st.rerun()
                else:
                    try:
                        with st.spinner("Creating account..."):
                            result = sign_up_with_email_password(email, password, display_name=name)
                            st.session_state['authenticated'] = True
                            st.session_state['user'] = {
                                "uid": result["localId"],
                                "email": result.get("email", ""),
                                "display_name": result.get("displayName", ""),
                                "id_token": result["idToken"],
                                "refresh_token": result["refreshToken"]
                            }
                        st.session_state['auth_msg'] = "Account created successfully!"
                        st.session_state['auth_msg_type'] = "success"
                        st.rerun()
                    except Exception as e:
                        err_str = str(e)
                        if "EMAIL_EXISTS" in err_str:
                            st.session_state['auth_msg'] = "This email is already registered. Try signing in instead."
                        elif "WEAK_PASSWORD" in err_str:
                            st.session_state['auth_msg'] = "Weak password. Please choose a stronger password."
                        else:
                            st.session_state['auth_msg'] = "Network or authentication error occurred."
                        st.session_state['auth_msg_type'] = "error"
                        st.rerun()

        elif mode == 'reset':
            st.markdown('<div class="auth-title">Reset your password</div>', unsafe_allow_html=True)
            st.markdown('<div class="auth-subtitle">Enter your email and we\'ll send you a reset link.</div>', unsafe_allow_html=True)

            show_msg()

            email = st.text_input("Email", placeholder="you@example.com", key="reset_email")

            st.write("")
            if st.button("Send reset link", type="primary"):
                if email:
                    try:
                        with st.spinner("Sending reset link..."):
                            send_password_reset_email(email)
                        st.session_state['auth_msg'] = "Password reset email sent. Check your inbox."
                        st.session_state['auth_msg_type'] = "success"
                        st.rerun()
                    except Exception as e:
                        err_str = str(e)
                        if "EMAIL_NOT_FOUND" in err_str:
                            st.session_state['auth_msg'] = "Email not found."
                        else:
                            st.session_state['auth_msg'] = "Failed to send reset link."
                        st.session_state['auth_msg_type'] = "error"
                        st.rerun()
                else:
                    st.session_state['auth_msg'] = "Please enter your email."
                    st.session_state['auth_msg_type'] = "error"
                    st.rerun()

        if mode in ['Sign in', 'Create account']:
            st.markdown("""<div class="auth-divider"><span>OR</span><hr></div>""", unsafe_allow_html=True)

            google_url = get_google_auth_url()
            if google_url:
                st.markdown(f'''<a href="{google_url}" style="text-decoration: none;" target="_self"><button style="width:100%; padding: 0.6rem; border-radius: 8px; border: 1px solid #e2e8f0; background-color: #ffffff; color: #334155; font-weight: 600; font-size: 0.95rem; display: flex; align-items: center; justify-content: center; gap: 10px; cursor: pointer; box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05); font-family: inherit; transition: background-color 0.2s;"><svg width="18" height="18" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/></svg>Continue with Google</button></a>''', unsafe_allow_html=True)
            else:
                st.markdown('<div class="inline-alert inline-alert-error">Google authentication is not configured.</div>', unsafe_allow_html=True)

            st.write("")
            st.write("")
            if mode == 'Sign in':
                if st.button("Don't have an account? Create account", type="secondary", use_container_width=True):
                    st.session_state['auth_mode'] = 'Create account'
                    st.rerun()
            else:
                if st.button("Already have an account? Sign in", type="secondary", use_container_width=True):
                    st.session_state['auth_mode'] = 'Sign in'
                    st.rerun()

        elif mode == 'reset':
            st.write("")
            st.write("")
            if st.button("Back to sign in", type="secondary", use_container_width=True):
                st.session_state['auth_mode'] = 'Sign in'
                st.session_state['auth_msg'] = None
                st.rerun()

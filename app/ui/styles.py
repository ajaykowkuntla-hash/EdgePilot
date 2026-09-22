import streamlit as st

def apply_global_styles():
    st.markdown("""
        <style>
            :root {
                /* Light theme minimalist palette */
                --ep-bg: #F8FAFC;
                --ep-surface: #FFFFFF;
                --ep-surface-2: #F1F5F9;
                --ep-border: #E2E8F0;
                --ep-text: #0F172A;
                --ep-muted: #64748B;
                
                /* Accent colors */
                --ep-accent: #0284C7; /* Restrained blue */
                --ep-accent-hover: #0369A1;
                --ep-success: #10B981;
                --ep-warning: #F59E0B;
                --ep-danger: #EF4444;
                
                --ep-font: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                --ep-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            }
            
            /* Base Streamlit App */
            .stApp {
                background-color: var(--ep-bg);
                color: var(--ep-text);
                font-family: var(--ep-font);
            }
            
            /* Typography */
            h1, h2, h3, h4, h5, h6, p, span, div {
                font-family: var(--ep-font);
                color: var(--ep-text);
            }
            
            .stMarkdown p {
                color: var(--ep-text);
            }
            
            /* Headers */
            header[data-testid="stHeader"] {
                background-color: transparent !important;
            }
            
            /* Sidebar */
            section[data-testid="stSidebar"] {
                background-color: var(--ep-surface);
                border-right: 1px solid var(--ep-border);
            }
            
            section[data-testid="stSidebar"] .stMarkdown p {
                color: var(--ep-text);
            }
            
            section[data-testid="stSidebar"] hr {
                border-color: var(--ep-border);
            }

            /* Main Content Container */
            .main .block-container {
                padding-top: 2rem !important;
                padding-bottom: 2rem !important;
                max-width: 1200px !important;
            }
            
            /* Buttons */
            div.stButton > button:first-child {
                background-color: var(--ep-surface);
                color: var(--ep-text);
                border: 1px solid var(--ep-border);
                border-radius: 8px;
                padding: 0.5rem 1rem;
                font-family: var(--ep-font);
                font-weight: 500;
                transition: all 0.2s ease-in-out;
                box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
            }
            
            div.stButton > button:first-child:hover {
                border-color: var(--ep-muted);
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            }
            
            /* Primary Button */
            div.stButton > button[kind="primary"] {
                background-color: var(--ep-accent);
                color: #FFFFFF;
                border: 1px solid var(--ep-accent);
                box-shadow: 0 1px 3px rgba(2, 132, 199, 0.3);
            }
            
            div.stButton > button[kind="primary"] p {
                color: #FFFFFF;
            }
            
            div.stButton > button[kind="primary"]:hover {
                background-color: var(--ep-accent-hover);
                border-color: var(--ep-accent-hover);
            }
            
            /* Input fields */
            .stTextInput > div > div > input, 
            .stTextArea > div > div > textarea, 
            .stSelectbox > div > div > div {
                background-color: var(--ep-surface) !important;
                color: var(--ep-text) !important;
                border: 1px solid var(--ep-border) !important;
                border-radius: 8px !important;
                box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
            }
            
            .stTextInput > div > div > input:focus, 
            .stTextArea > div > div > textarea:focus, 
            .stSelectbox > div > div > div:focus {
                border-color: var(--ep-accent) !important;
                box-shadow: 0 0 0 1px var(--ep-accent) !important;
            }
            
            /* File Uploader */
            .stFileUploader > div > div {
                background-color: var(--ep-surface-2);
                border: 1px dashed var(--ep-border);
                border-radius: 12px;
                padding: 2rem;
            }
            .stFileUploader > div > div:hover {
                border-color: var(--ep-accent);
            }
            
            /* Remove standard st info/warning/success/error backgrounds to replace with industrial look */
            div[data-testid="stAlert"] {
                background-color: var(--ep-surface);
                border: 1px solid var(--ep-border);
                color: var(--ep-text);
                border-radius: 8px;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            }
            
            /* Industrial styling for success/error/warning alerts */
            div[data-testid="stAlert"]:has(> div > div > p:contains("✓")),
            div[data-testid="stAlert"]:has(> div > div > p:contains("PASS")) {
                border-left: 4px solid var(--ep-success);
            }
            
            div[data-testid="stAlert"]:has(> div > div > p:contains("REJECT")),
            div[data-testid="stAlert"]:has(> div > div > p:contains("DEFECT")) {
                border-left: 4px solid var(--ep-danger);
            }
            
            /* Clean up Expander */
            .streamlit-expanderHeader {
                background-color: var(--ep-surface) !important;
                color: var(--ep-text) !important;
                border: 1px solid var(--ep-border) !important;
                border-radius: 8px !important;
                box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
            }
            
            /* Generic Card Class */
            .ep-card {
                background-color: var(--ep-surface);
                border: 1px solid var(--ep-border);
                border-radius: 12px;
                padding: 1.5rem;
                margin-bottom: 1rem;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            }
            
            .ep-card-header {
                font-size: 0.8rem;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                color: var(--ep-muted);
                margin-bottom: 0.75rem;
                font-weight: 600;
            }
            
            .ep-metric-value {
                font-family: var(--ep-font);
                font-size: 2.5rem;
                font-weight: 600;
                color: var(--ep-text);
                line-height: 1.1;
            }
            
            .ep-badge {
                display: inline-block;
                padding: 0.25rem 0.75rem;
                font-size: 0.75rem;
                font-weight: 600;
                border-radius: 9999px; /* Pill shape */
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }
            
            .ep-badge.success { background-color: rgba(16, 185, 129, 0.1); color: var(--ep-success); border: 1px solid rgba(16, 185, 129, 0.2); }
            .ep-badge.warning { background-color: rgba(245, 158, 11, 0.1); color: var(--ep-warning); border: 1px solid rgba(245, 158, 11, 0.2); }
            .ep-badge.danger { background-color: rgba(239, 68, 68, 0.1); color: var(--ep-danger); border: 1px solid rgba(239, 68, 68, 0.2); }
            .ep-badge.neutral { background-color: var(--ep-surface-2); color: var(--ep-muted); border: 1px solid var(--ep-border); }
            
            /* Custom HR */
            hr {
                border-top: 1px solid var(--ep-border);
                margin: 2rem 0;
            }

            /* Custom Radio Buttons for Wizard Cards */
            div.row-widget.stRadio > div {
                flex-direction: row;
                gap: 1rem;
                flex-wrap: wrap;
            }
            
            div.row-widget.stRadio > div > label {
                background-color: var(--ep-surface);
                border: 1px solid var(--ep-border);
                border-radius: 12px;
                padding: 1.5rem;
                flex: 1;
                min-width: 200px;
                cursor: pointer;
                transition: all 0.2s ease;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            }
            
            div.row-widget.stRadio > div > label:hover {
                border-color: var(--ep-accent);
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            }
            
            div.row-widget.stRadio > div > label[data-baseweb="radio"] > div:first-child {
                display: none; /* Hide the actual radio circle */
            }

            /* Wizard Step Bar */
            .ep-wizard {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                padding: 1rem;
                background-color: var(--ep-surface);
                border: 1px solid var(--ep-border);
                border-radius: 12px;
                margin-bottom: 2rem;
                overflow-x: auto;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            }
            
            .ep-step {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                font-size: 0.9rem;
                font-weight: 500;
                color: var(--ep-muted);
                white-space: nowrap;
            }
            
            .ep-step.active {
                color: var(--ep-text);
                font-weight: 600;
            }
            
            .ep-step.completed {
                color: var(--ep-success);
            }
            
            .ep-step-separator {
                color: var(--ep-border);
            }
        </style>
    """, unsafe_allow_html=True)

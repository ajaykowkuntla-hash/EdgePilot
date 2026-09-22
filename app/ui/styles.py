import streamlit as st

def apply_global_styles():
    st.markdown("""
        <style>
            :root {
                --ep-bg: #0B0F14;
                --ep-surface: #111820;
                --ep-surface-2: #161F29;
                --ep-border: #26313D;
                --ep-text: #F4F7FA;
                --ep-muted: #8B98A7;
                --ep-accent: #00E5FF;
                --ep-success: #00E676;
                --ep-warning: #FFC400;
                --ep-danger: #FF1744;
                
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
                max-width: 1440px !important;
            }
            
            /* Overriding default metric */
            div[data-testid="stMetricValue"] {
                font-family: var(--ep-mono);
            }
            
            /* Buttons */
            div.stButton > button:first-child {
                background-color: var(--ep-surface-2);
                color: var(--ep-text);
                border: 1px solid var(--ep-border);
                border-radius: 4px;
                padding: 0.5rem 1rem;
                font-family: var(--ep-font);
                font-weight: 500;
                transition: all 0.2s ease-in-out;
            }
            
            div.stButton > button:first-child:hover {
                border-color: var(--ep-accent);
                color: var(--ep-accent);
            }
            
            /* Primary Button */
            div.stButton > button[kind="primary"] {
                background-color: var(--ep-accent);
                color: #000000;
                border: 1px solid var(--ep-accent);
            }
            
            div.stButton > button[kind="primary"]:hover {
                background-color: #00B8CC;
                border-color: #00B8CC;
                color: #000000;
            }
            
            /* Input fields */
            .stTextInput > div > div > input, 
            .stTextArea > div > div > textarea, 
            .stSelectbox > div > div > div {
                background-color: var(--ep-surface-2) !important;
                color: var(--ep-text) !important;
                border: 1px solid var(--ep-border) !important;
                border-radius: 4px !important;
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
                border-radius: 8px;
            }
            .stFileUploader > div > div:hover {
                border-color: var(--ep-accent);
            }
            
            /* Remove standard st info/warning/success/error backgrounds to replace with industrial look */
            div[data-testid="stAlert"] {
                background-color: var(--ep-surface-2);
                border: 1px solid var(--ep-border);
                color: var(--ep-text);
                border-radius: 4px;
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
                background-color: var(--ep-surface-2) !important;
                color: var(--ep-text) !important;
                border: 1px solid var(--ep-border) !important;
                border-radius: 4px !important;
            }
            
            /* Generic Card Class to be used with st.markdown */
            .ep-card {
                background-color: var(--ep-surface);
                border: 1px solid var(--ep-border);
                border-radius: 6px;
                padding: 1.5rem;
                margin-bottom: 1rem;
            }
            
            .ep-card-header {
                font-size: 0.75rem;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                color: var(--ep-muted);
                margin-bottom: 0.5rem;
                font-weight: 600;
            }
            
            .ep-metric-value {
                font-family: var(--ep-mono);
                font-size: 2rem;
                font-weight: 400;
                color: var(--ep-text);
            }
            
            .ep-badge {
                display: inline-block;
                padding: 0.25rem 0.5rem;
                font-size: 0.75rem;
                font-weight: 600;
                border-radius: 4px;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }
            
            .ep-badge.success { background-color: rgba(0, 230, 118, 0.1); color: var(--ep-success); border: 1px solid rgba(0, 230, 118, 0.2); }
            .ep-badge.warning { background-color: rgba(255, 196, 0, 0.1); color: var(--ep-warning); border: 1px solid rgba(255, 196, 0, 0.2); }
            .ep-badge.danger { background-color: rgba(255, 23, 68, 0.1); color: var(--ep-danger); border: 1px solid rgba(255, 23, 68, 0.2); }
            .ep-badge.neutral { background-color: rgba(139, 152, 167, 0.1); color: var(--ep-muted); border: 1px solid rgba(139, 152, 167, 0.2); }
            
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
                background-color: var(--ep-surface-2);
                border: 1px solid var(--ep-border);
                border-radius: 6px;
                padding: 1.5rem;
                flex: 1;
                min-width: 200px;
                cursor: pointer;
                transition: all 0.2s ease;
            }
            
            div.row-widget.stRadio > div > label:hover {
                border-color: var(--ep-muted);
            }
            
            div.row-widget.stRadio > div > label[data-baseweb="radio"] > div:first-child {
                display: none; /* Hide the actual radio circle */
            }
            
            /* Workaround for selected radio state using Streamlit's aria-checked attribute if possible, otherwise rely on st.radio functionality */

            /* Wizard Step Bar */
            .ep-wizard {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                padding: 1rem;
                background-color: var(--ep-surface);
                border: 1px solid var(--ep-border);
                border-radius: 6px;
                margin-bottom: 2rem;
                overflow-x: auto;
            }
            
            .ep-step {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                font-size: 0.85rem;
                font-weight: 500;
                color: var(--ep-muted);
                white-space: nowrap;
            }
            
            .ep-step.active {
                color: var(--ep-accent);
            }
            
            .ep-step.completed {
                color: var(--ep-success);
            }
            
            .ep-step-separator {
                color: var(--ep-border);
            }
        </style>
    """, unsafe_allow_html=True)

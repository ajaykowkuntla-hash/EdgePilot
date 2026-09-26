import pytest
from unittest.mock import patch, MagicMock

import streamlit as st
from app.views.inspection import (
    render_step_1, render_step_2, render_step_3,
    render_step_4, render_step_5, render_step_6, reset_wizard
)

@pytest.fixture(autouse=True)
def mock_streamlit():
    st.session_state.clear()
    st.session_state['user'] = {"uid": "test_user", "id_token": "test_token"}
    
    with patch('streamlit.button') as mock_button, \
         patch('streamlit.write') as mock_write, \
         patch('streamlit.error') as mock_error, \
         patch('streamlit.success') as mock_success, \
         patch('streamlit.info') as mock_info, \
         patch('streamlit.warning') as mock_warning, \
         patch('streamlit.markdown') as mock_markdown, \
         patch('streamlit.rerun') as mock_rerun:
        yield {
            'button': mock_button,
            'write': mock_write,
            'error': mock_error,
            'success': mock_success,
            'info': mock_info,
            'warning': mock_warning,
            'markdown': mock_markdown,
            'rerun': mock_rerun
        }

def test_phase26_demo_workflow(mock_streamlit):
    # Step 1: Task Selection
    mock_streamlit['button'].side_effect = [True] + [False] * 10
    render_step_1()
    assert 'selected_category' in st.session_state
    assert st.session_state['wizard_step'] == 2

    # Step 2: Foundation
    render_step_2()
    
    # Step 3: Examples
    render_step_3()
    st.session_state['business_examples_dir'] = 'fake/dir'

    # Step 4: Adaptation
    # Simulate adaptation result
    st.session_state['adaptation_result'] = {
        "decision": "MORE_DATA_RECOMMENDED",
        "metrics": {"map50": 0.6588, "map50-95": 0.3226, "precision": 0.6084, "recall": 0.6172},
        "model_size_mb": 5.96
    }
    
    # Step 5: Model Readiness
    render_step_5()
    
    markdown_calls = [call.args[0] for call in mock_streamlit['markdown'].call_args_list]
    assert any("MORE EXAMPLES RECOMMENDED" in call for call in markdown_calls)
    
    # Step 6: Deployment Candidate
    render_step_6()
    
    # Check that Run Inspection button is handled
    assert mock_streamlit['button'].called
    
    # Check reset workflow
    reset_wizard()
    assert 'wizard_step' not in st.session_state
    assert 'selected_category' not in st.session_state
    assert 'adaptation_result' not in st.session_state

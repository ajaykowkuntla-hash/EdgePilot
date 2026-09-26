import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_st():
    with patch('app.views.inspection.st') as st_mock:
        state = {}
        st_mock.session_state = state
        st_mock.button.return_value = False
        
        def columns_side_effect(num):
            if isinstance(num, list):
                return [MagicMock() for _ in num]
            return [MagicMock() for _ in range(num)]
        st_mock.columns.side_effect = columns_side_effect
        
        yield st_mock

def test_task_to_foundation_selection(mock_st):
    from app.views.inspection import render_step_1, render_step_2
    
    with patch('app.views.inspection.ModelRegistry') as registry_mock:
        registry_mock.return_value.registry = {
            "categories": {
                "product_defect": {
                    "name": "Product Defect Inspection",
                    "model": "yolov8n",
                    "dataset": "NEU-DET"
                }
            }
        }
        
        mock_st.button.return_value = True
        render_step_1()
        assert mock_st.session_state.get('selected_category') == "product_defect"
        
        render_step_2()
        mock_st.write.assert_any_call("**Dataset:** NEU-DET")

def test_uploaded_examples_to_adaptation_input(mock_st):
    from app.views.inspection import render_step_3
    import os
    
    mock_file = MagicMock()
    mock_file.getbuffer.return_value = b"dummy content"
    mock_st.file_uploader.return_value = mock_file
    
    with patch('app.views.inspection.zipfile.ZipFile'), \
         patch('builtins.open'), \
         patch('app.views.inspection.os.makedirs'), \
         patch('app.views.inspection.os.remove'), \
         patch('app.views.inspection.shutil.rmtree'):
         
        mock_st.session_state['selected_task_example'] = 'test_task'
        render_step_3()
        assert 'business_examples_dir' in mock_st.session_state
        assert 'business_examples' in mock_st.session_state['business_examples_dir']

def test_adaptation_result_to_business_decision_supported(mock_st):
    from app.views.inspection import render_step_5, render_step_6
    
    mock_st.session_state['adaptation_result'] = {
        "decision": "ADAPTATION_SUPPORTED",
        "metrics": {"map50": 0.8},
        "model_size_mb": 6.0
    }
    
    render_step_5()
    # It should render the success block
    
    render_step_6()
    mock_st.success.assert_called_with("Model ready for deployment validation.")

def test_adaptation_result_insufficient_more_examples(mock_st):
    from app.views.inspection import render_step_5, render_step_6
    
    mock_st.session_state['adaptation_result'] = {
        "decision": "MORE_DATA_RECOMMENDED",
        "metrics": {"map50": 0.65},
        "model_size_mb": 6.0
    }
    
    render_step_5()
    
    render_step_6()
    mock_st.info.assert_called_with("Provide more representative examples and evaluate again.")

def test_no_fake_success_states(mock_st):
    from app.views.inspection import render_step_4
    
    with patch('app.views.inspection.AdaptationEngine') as engine_mock, \
         patch('app.views.inspection.os.path.exists', return_value=True):
         
        engine_mock.return_value.adapt_and_evaluate.return_value = {
            "decision": "MORE_DATA_RECOMMENDED",
            "metrics": {"map50": 0.5}
        }
        
        mock_st.session_state['is_adapting'] = True
        mock_st.session_state['selected_task_example'] = 'task_1'
        mock_st.session_state['business_examples_dir'] = 'dummy/path'
        
        with patch('app.views.inspection.glob.glob', return_value=['dummy.jpg']):
            render_step_4()
            
        engine_mock.return_value.adapt_and_evaluate.assert_called_once()
        assert mock_st.session_state['adaptation_result']['decision'] == "MORE_DATA_RECOMMENDED"
        assert mock_st.session_state['is_adapting'] == False

def test_missing_foundation_adaptation_does_not_start(mock_st):
    from app.views.inspection import render_step_4
    
    with patch('app.views.inspection.AdaptationEngine') as engine_mock, \
         patch('app.views.inspection.os.path.exists', return_value=False):
         
        mock_st.session_state['is_adapting'] = True
        mock_st.session_state['selected_task_example'] = 'task_1'
        mock_st.session_state['business_examples_dir'] = 'dummy/path'
        
        render_step_4()
        
        # Should not have called engine
        engine_mock.return_value.adapt_and_evaluate.assert_not_called()
        # Should show error
        mock_st.error.assert_called_with("Foundation dataset is unavailable for this task.")
        # Should disable adapting flag
        assert mock_st.session_state['is_adapting'] == False

def test_mock_foundation_only_in_tests():
    # Verify that 'mock_foundation' string is NOT anywhere in inspection.py anymore
    with open('app/views/inspection.py', 'r') as f:
        content = f.read()
        assert "datasets/mock_foundation" not in content, "Mock foundation generation leaked into production code!"

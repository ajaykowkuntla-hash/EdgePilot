import os
import shutil
import pytest
import yaml
from app.core.adaptation_engine import AdaptationEngine

@pytest.fixture
def mock_foundation_data(tmp_path):
    f_dir = tmp_path / "foundation"
    f_dir.mkdir()
    images_train = f_dir / "images" / "train"
    images_val = f_dir / "images" / "val"
    labels_train = f_dir / "labels" / "train"
    labels_val = f_dir / "labels" / "val"
    
    for p in [images_train, images_val, labels_train, labels_val]:
        p.mkdir(parents=True)
        
    # Add dummy files
    for i in range(10):
        (images_train / f"f_img_{i}.jpg").touch()
        (labels_train / f"f_img_{i}.txt").touch()
        (images_val / f"f_val_{i}.jpg").touch()
        (labels_val / f"f_val_{i}.txt").touch()
        
    yaml_path = f_dir / "data.yaml"
    with open(yaml_path, 'w') as f:
        yaml.dump({
            "train": "images/train",
            "val": "images/val",
            "names": ["class0"],
            "nc": 1
        }, f)
        
    return str(yaml_path)

@pytest.fixture
def mock_business_examples(tmp_path):
    b_dir = tmp_path / "business"
    b_dir.mkdir()
    
    images = []
    labels = []
    
    for i in range(5):
        img = b_dir / f"biz_{i}.jpg"
        lbl = b_dir / f"biz_{i}.txt"
        img.touch()
        lbl.touch()
        images.append(str(img))
        labels.append(str(lbl))
        
    return {"images": images, "labels": labels}

def test_no_eval_leakage(mock_foundation_data, mock_business_examples, tmp_path):
    # Test that business examples are placed ONLY in train, never in val
    engine = AdaptationEngine("test_task")
    engine.base_dir = str(tmp_path / "adaptation")
    
    combined_yaml = engine._create_combined_dataset(mock_foundation_data, mock_business_examples)
    combined_dir = os.path.dirname(combined_yaml)
    
    val_images = os.listdir(os.path.join(combined_dir, "images", "val"))
    val_labels = os.listdir(os.path.join(combined_dir, "labels", "val"))
    
    # Assert business examples are NOT in val
    for img in mock_business_examples["images"]:
        base_name = os.path.basename(img)
        assert base_name not in val_images
        assert f"biz_{base_name}" not in val_images
        
    # Assert they ARE in train
    train_images = os.listdir(os.path.join(combined_dir, "images", "train"))
    assert any(img.startswith("biz_") for img in train_images)
    
def test_correct_example_counts(mock_foundation_data, mock_business_examples, tmp_path):
    engine = AdaptationEngine("test_task")
    engine.base_dir = str(tmp_path / "adaptation")
    
    combined_yaml = engine._create_combined_dataset(mock_foundation_data, mock_business_examples)
    combined_dir = os.path.dirname(combined_yaml)
    
    # Foundation had 10 train. Biz had 5. Total = 15.
    train_images = os.listdir(os.path.join(combined_dir, "images", "train"))
    assert len(train_images) == 15
    
    # Foundation had 10 val.
    val_images = os.listdir(os.path.join(combined_dir, "images", "val"))
    assert len(val_images) == 10

def test_adaptation_decision_logic():
    engine = AdaptationEngine("test_task")
    
    # Case 1: Clear improvement (>= 2%)
    baseline = {"map50": 0.50}
    
    # Mocking the train/evaluate methods
    class DummyAutoML:
        def train(self, *args, **kwargs): return "model.pt", 10.0, None
        def evaluate(self, *args, **kwargs): return {"map50": 0.53}
        
    engine.automl = DummyAutoML()
    engine._create_combined_dataset = lambda x, y: "dummy.yaml"
    
    # We must patch os.path.getsize for model size
    import unittest.mock
    with unittest.mock.patch('os.path.getsize', return_value=1024*1024*10):
        res = engine.adapt_and_evaluate("dummy", {}, baseline)
        assert res["decision"] == "ADAPTATION_SUPPORTED"
        assert round(res["improvement"], 2) == 0.03
        
        # Case 2: Similar (-2% to +2%)
        engine.automl.evaluate = lambda *a, **k: {"map50": 0.51}
        res = engine.adapt_and_evaluate("dummy", {}, baseline)
        assert res["decision"] == "MORE_DATA_RECOMMENDED"
        
        # Case 3: Decreased (<= -2%)
        engine.automl.evaluate = lambda *a, **k: {"map50": 0.45}
        res = engine.adapt_and_evaluate("dummy", {}, baseline)
        assert res["decision"] == "ADAPTATION_NOT_SUPPORTED"

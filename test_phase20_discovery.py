import pytest
from app.core.dataset_discovery import DatasetDiscoveryEngine
from app.core.registry import ModelRegistry

def test_registry_unmodified():
    registry = ModelRegistry()
    assert registry.registry.get("categories", {}).get("product_defect", {}).get("model") == "yolov8n", "Registry mapping must remain unchanged."

def test_discovery_engine_mock():
    engine = DatasetDiscoveryEngine(use_mock=True)
    candidates = engine.search_candidates("Packaging Inspection")
    assert len(candidates) > 0
    
    c = candidates[0]
    assert c["name"] == "Packaging / Box Inspection"
    assert c["source"] == "Mock Source"
    assert c["task_type"] == "Object Detection"
    assert c["license"] == "CC BY 4.0"
    assert c["status"] == "approved", "Mock explicitly returns approved"

def test_compatibility_filtering():
    engine = DatasetDiscoveryEngine(use_mock=False)
    
    # Test unknown license
    c1 = engine._apply_compatibility_filters({
        "task_type": "Object Detection",
        "license": "Unknown",
        "status": "review_required"
    }, "Test")
    assert c1["status"] == "license_unknown"
    
    # Test non-commercial license
    c2 = engine._apply_compatibility_filters({
        "task_type": "Object Detection",
        "license": "CC BY-NC 4.0",
        "status": "review_required"
    }, "Test")
    assert c2["status"] == "incompatible"

    # Test good license
    c3 = engine._apply_compatibility_filters({
        "task_type": "Object Detection",
        "license": "MIT",
        "status": "review_required"
    }, "Test")
    assert c3["status"] == "review_required", "Should not auto-approve, requires review"
    
    # Test bad task type
    c4 = engine._apply_compatibility_filters({
        "task_type": "Image Classification",
        "license": "MIT",
        "status": "review_required"
    }, "Test")
    assert c4["status"] == "incompatible"

def test_no_candidate_returns_empty():
    engine = DatasetDiscoveryEngine(use_mock=True)
    # Mock source only responds to "packaging"
    candidates = engine.search_candidates("Super Rare Defect Inspection")
    assert len(candidates) == 0

def test_external_source_never_auto_approved():
    # Even if we use mock=False and ping HF, it should never return "approved"
    engine = DatasetDiscoveryEngine(use_mock=False)
    # Force a mock candidate through the normal filter
    c = engine._apply_compatibility_filters({
        "task_type": "Object Detection",
        "license": "MIT",
        "status": "review_required"
    }, "Test")
    assert c["status"] != "approved", "External sources must never be auto-approved without manual review"

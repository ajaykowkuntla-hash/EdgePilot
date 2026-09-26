import os
import shutil
import pytest
import json
import yaml
from app.core.dataset_importer import DatasetImporter
from app.core.dataset_normalizer import DatasetNormalizer

@pytest.fixture
def test_task():
    task_id = "test_import_task"
    base_dir = os.path.join("datasets", task_id)
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
    yield task_id
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)

def test_license_unknown_rejected(test_task):
    importer = DatasetImporter(test_task, use_mock=True)
    with pytest.raises(ValueError, match="Cannot import dataset with status: license_unknown"):
        importer.import_dataset({"status": "license_unknown", "source": "Hugging Face"})

def test_incompatible_rejected(test_task):
    importer = DatasetImporter(test_task, use_mock=True)
    with pytest.raises(ValueError, match="Cannot import dataset with status: incompatible"):
        importer.import_dataset({"status": "incompatible", "source": "Hugging Face"})

def test_review_required_needs_confirmation(test_task):
    importer = DatasetImporter(test_task, use_mock=True)
    with pytest.raises(ValueError, match="Dataset requires explicit license review"):
        importer.import_dataset({"status": "review_required", "source": "Hugging Face"})

    # Should work when confirmed
    importer.import_dataset({"status": "review_required", "source": "Hugging Face", "user_confirmed": True})
    assert os.path.exists(os.path.join("datasets", test_task, "metadata.json"))

def test_approved_proceeds(test_task):
    importer = DatasetImporter(test_task, use_mock=True)
    importer.import_dataset({"status": "approved", "source": "Mock Source"})
    assert os.path.exists(os.path.join("datasets", test_task, "metadata.json"))

def setup_yolo_fixture(task_id, malformed=False, invalid_class=False):
    source_dir = os.path.join("datasets", task_id, "source")
    os.makedirs(os.path.join(source_dir, "images", "train"), exist_ok=True)
    os.makedirs(os.path.join(source_dir, "images", "val"), exist_ok=True)
    os.makedirs(os.path.join(source_dir, "labels", "train"), exist_ok=True)
    os.makedirs(os.path.join(source_dir, "labels", "val"), exist_ok=True)

    with open(os.path.join(source_dir, "data.yaml"), "w") as f:
        yaml.dump({"train": "images/train", "val": "images/val", "names": ["class1", "class2"]}, f)

    with open(os.path.join(source_dir, "images", "train", "img1.jpg"), "w") as f: f.write("img")
    with open(os.path.join(source_dir, "images", "val", "img2.jpg"), "w") as f: f.write("img")

    lbl1 = "0 0.5 0.5 0.1 0.1"
    if malformed:
        lbl1 = "0 0.5 0.5" # Missing dims
    elif invalid_class:
        lbl1 = "99 0.5 0.5 0.1 0.1"

    with open(os.path.join(source_dir, "labels", "train", "img1.txt"), "w") as f: f.write(lbl1)
    with open(os.path.join(source_dir, "labels", "val", "img2.txt"), "w") as f: f.write("1 0.5 0.5 0.1 0.1")

def test_yolo_detection_and_normalization(test_task):
    importer = DatasetImporter(test_task, use_mock=True)
    importer.import_dataset({"status": "approved", "source": "Mock Source"})
    setup_yolo_fixture(test_task)

    normalizer = DatasetNormalizer(test_task)
    assert normalizer.detect_format() == "YOLO"

    res = normalizer.normalize()
    assert res["is_valid"] is True

    # Check normalized files exist
    assert os.path.exists(os.path.join(normalizer.normalized_dir, "data.yaml"))
    assert os.path.exists(os.path.join(normalizer.normalized_dir, "images", "train", "img1.jpg"))
    assert os.path.exists(os.path.join(normalizer.normalized_dir, "labels", "train", "img1.txt"))

    # Check metadata updated
    with open(os.path.join("datasets", test_task, "metadata.json"), "r") as f:
        meta = json.load(f)
        assert meta["normalized_format"] == "YOLO"
        assert meta["train_count"] == 1

def test_malformed_annotations_rejected(test_task):
    importer = DatasetImporter(test_task, use_mock=True)
    importer.import_dataset({"status": "approved", "source": "Mock Source"})
    setup_yolo_fixture(test_task, malformed=True)

    normalizer = DatasetNormalizer(test_task)
    res = normalizer.normalize()
    assert res["is_valid"] is False
    assert any("Malformed" in e for e in res["errors"])

def test_invalid_class_rejected(test_task):
    importer = DatasetImporter(test_task, use_mock=True)
    importer.import_dataset({"status": "approved", "source": "Mock Source"})
    setup_yolo_fixture(test_task, invalid_class=True)

    normalizer = DatasetNormalizer(test_task)
    res = normalizer.normalize()
    assert res["is_valid"] is False
    assert any("Invalid class ID" in e for e in res["errors"])

def test_path_traversal_blocked(test_task):
    importer = DatasetImporter(test_task, use_mock=True)
    importer.import_dataset({"status": "approved", "source": "Mock Source"})
    setup_yolo_fixture(test_task)

    # Inject bad path in yaml
    with open(os.path.join("datasets", test_task, "source", "data.yaml"), "w") as f:
        yaml.dump({"train": "../../../etc", "val": "images/val", "names": ["class1", "class2"]}, f)

    normalizer = DatasetNormalizer(test_task)
    with pytest.raises(ValueError, match="Path traversal"):
        normalizer.normalize()

def test_coco_conversion(test_task):
    importer = DatasetImporter(test_task, use_mock=True)
    importer.import_dataset({"status": "approved", "source": "Mock Source"})
    source_dir = os.path.join("datasets", test_task, "source")
    os.makedirs(os.path.join(source_dir, "annotations"))
    with open(os.path.join(source_dir, "annotations", "instances_train.json"), "w") as f: f.write("{}")

    normalizer = DatasetNormalizer(test_task)
    assert normalizer.detect_format() == "COCO"
    res = normalizer.normalize()
    assert res["is_valid"] is True

def test_voc_conversion(test_task):
    importer = DatasetImporter(test_task, use_mock=True)
    importer.import_dataset({"status": "approved", "source": "Mock Source"})
    source_dir = os.path.join("datasets", test_task, "source")
    os.makedirs(os.path.join(source_dir, "Annotations"))

    normalizer = DatasetNormalizer(test_task)
    assert normalizer.detect_format() == "Pascal_VOC"
    res = normalizer.normalize()
    assert res["is_valid"] is True

def test_unsupported_format(test_task):
    importer = DatasetImporter(test_task, use_mock=True)
    importer.import_dataset({"status": "approved", "source": "Mock Source"})
    # empty source dir
    normalizer = DatasetNormalizer(test_task)
    assert normalizer.detect_format() == "unsupported_format"
    res = normalizer.normalize()
    assert res["is_valid"] is False

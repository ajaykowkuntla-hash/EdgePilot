import os
import shutil
import uuid
import yaml
from app.core.task_manager import TaskManager
from app.core.automl_engine import AutoMLEngine
import app.utils.inference as inf_module

def test_pipeline():
    print("=== STARTING END-TO-END PIPELINE TEST ===")
    
    # 1. Setup Task
    tm = TaskManager()
    task_id = "custom_" + str(uuid.uuid4())[:8]
    task = tm.create_task(task_id, "E2E Test Task", objective="End to end pipeline", decision="Reject Product")
    print(f"1. Task Created: {task_id}")
    
    # 2. Setup Dataset
    dataset_dir = os.path.join("datasets", task_id)
    os.makedirs(dataset_dir, exist_ok=True)
    
    # Copy from phase2/dataset to our new dataset_dir
    shutil.copytree("phase2/dataset/train", os.path.join(dataset_dir, "train"))
    shutil.copytree("phase2/dataset/test", os.path.join(dataset_dir, "test"))
    
    # Create data.yaml
    yaml_content = {
        "train": "train/images",
        "val": "test/images",
        "nc": 6,
        "names": ['crazing', 'inclusion', 'patches', 'pitted_surface', 'rolled-in_scale', 'scratches']
    }
    with open(os.path.join(dataset_dir, "data.yaml"), "w") as f:
        yaml.dump(yaml_content, f)
        
    tm.update_task(task_id, {"dataset_path": dataset_dir})
    print(f"2. Dataset Prepared at {dataset_dir}")
    
    # 3. Validate Dataset
    engine = AutoMLEngine()
    val_result = engine.validate_dataset(dataset_dir)
    print(f"3. Dataset Validation Result: {val_result['is_valid']}")
    if not val_result['is_valid']:
        print("Validation errors:", val_result['errors'])
        return
        
    tm.update_task(task_id, {"dataset_validation_status": True})
    
    # 4. Train Model
    print("4. Starting Training (5 epochs)...")
    yaml_path = os.path.join(dataset_dir, "data.yaml")
    model_pt, train_time, results = engine.train(task_id, yaml_path)
    print(f"   Training Complete in {train_time:.2f}s. Model at {model_pt}")
    
    # 5. Evaluate Model
    print("5. Evaluating Model...")
    metrics = engine.evaluate(model_pt, yaml_path)
    print(f"   Metrics: mAP50={metrics['map50']:.4f}, mAP50-95={metrics['map50_95']:.4f}")
    
    tm.update_task(task_id, {
        "training_status": "Complete",
        "model_pt": model_pt,
        "evaluation_metrics": metrics
    })
    
    # 6. Export ONNX
    print("6. Exporting to ONNX...")
    onnx_path = engine.export_onnx(model_pt)
    print(f"   ONNX Exported at {onnx_path}")
    tm.update_task(task_id, {"model_onnx": onnx_path})
    
    # 7. Test Inference
    print("7. Testing Inference...")
    test_image_path = "phase2/dataset/test/images/pitted_surface_277.jpg"
    with open(test_image_path, "rb") as f:
        image_bytes = f.read()
        
    from ultralytics import YOLO
    inf_module._model_onnx = YOLO(onnx_path)
    
    result = inf_module.run_inference(image_bytes, confidence_threshold=0.5, engine="onnx")
    if "error" in result:
        print("   Inference Error:", result["error"])
    else:
        print(f"   Inference Success! Detected {len(result['detections'])} objects.")
        for d in result['detections']:
            print(f"     - {d['class']} ({d['confidence']:.2f})")
            
    print("=== TEST COMPLETED SUCCESSFULLY ===")

if __name__ == "__main__":
    test_pipeline()

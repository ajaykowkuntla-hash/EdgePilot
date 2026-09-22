from app.core.registry import ModelRegistry
from app.core.task_manager import TaskManager
from app.core.automl_engine import AutoMLEngine
import os

def main():
    registry = ModelRegistry()
    task_manager = TaskManager()
    engine = AutoMLEngine()

    # Step 1: Create the Task B representation
    task_id = "task_2_bottle_defect"
    template_id = "yolov8n_object_detection"
    dataset_path = os.path.abspath("phase9/dataset_b")
    
    task_manager.create_task(task_id, "Bottle Cap Defect Detection", template_id, dataset_path)
    
    # Step 2: Validate Data
    valid, data_yaml = engine.prepare_training_data(dataset_path)
    if not valid:
        print("Dataset validation failed:", data_yaml)
        return
        
    print(f"Data valid: {data_yaml}")
    
    # Step 3: Train
    template = registry.get_template(template_id)
    base_model = template["base_model"]
    
    print("Starting AutoML Training...")
    model_pt_path, train_time, results = engine.train_task(task_id, base_model, data_yaml)
    
    print(f"Training completed in {train_time:.1f}s")
    print(f"Model saved to {model_pt_path}")
    
    # Evaluate (already done inside train by Ultralytics, but we can extract metrics)
    metrics = results.results_dict
    map50 = metrics.get('metrics/mAP50(B)', 0.0)
    print(f"Validation mAP50: {map50:.4f}")
    
    # Step 4: Export to ONNX
    print("Exporting to ONNX...")
    onnx_path = engine.export_to_onnx(model_pt_path)
    print(f"Exported to {onnx_path}")
    
    # Update Task Manager
    task_manager.update_task_model(task_id, model_pt_path, onnx_path)
    
    # Step 5: Test Inference
    from app.utils.inference import run_inference
    # Find a test image in dataset_b
    test_img = os.path.join(dataset_path, "images", "val", "000000000139.jpg") # A sample from coco8
    if not os.path.exists(test_img):
        # Fallback to any val image
        val_imgs = os.listdir(os.path.join(dataset_path, "images", "val"))
        test_img = os.path.join(dataset_path, "images", "val", val_imgs[0])
        
    with open(test_img, "rb") as f:
        image_bytes = f.read()
        
    # Hack the inference.py to load THIS model temporarily
    from ultralytics import YOLO
    import app.utils.inference as inf
    inf._model_onnx = YOLO(onnx_path)
    
    inf_res = inf.run_inference(image_bytes, engine="onnx")
    print("\n--- Validation Image Inference ---")
    if "error" in inf_res:
        print("Inference error:", inf_res["error"])
    else:
        print(f"Inference Time: {inf_res['inference_time']:.1f} ms")
        for d in inf_res['detections']:
            print(f"Detected {d['class']} @ {d['confidence']:.4f}")

if __name__ == "__main__":
    main()

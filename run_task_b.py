import os
import time
from app.core.automl_engine import AutoMLEngine
from ultralytics import YOLO

def main():
    engine = AutoMLEngine()
    
    dataset_path = "/Users/ajaykowkuntla/Desktop/New Pro/app/data/deeppcb_subset"
    
    # 1. Prepare/Verify Data
    valid, data_yaml = engine.prepare_training_data(dataset_path)
    if not valid:
        print(f"Error: {data_yaml}")
        return
        
    print(f"Verified dataset at {data_yaml}")
    
    # 2. Train Task
    task_id = "task_b_deeppcb_experiment"
    print(f"Starting AutoML Training for Task: {task_id}")
    
    # We use YOLOv8-N as the template base model for edge deployment
    pt_path, train_time, results = engine.train_task(
        task_id=task_id, 
        template_base_model="yolov8n.pt", 
        data_yaml_path=data_yaml
    )
    
    print(f"\n--- Training Complete ---")
    print(f"Training Time: {train_time:.2f} seconds")
    print(f"PyTorch Model saved to: {pt_path}")
    
    pt_size = os.path.getsize(pt_path) / (1024 * 1024)
    print(f"PyTorch Model Size: {pt_size:.2f} MB")
    
    # Validation Metrics
    print(f"\n--- Validation Metrics ---")
    if hasattr(results, 'box') and hasattr(results.box, 'map50'):
        print(f"mAP@50: {results.box.map50:.4f}")
        print(f"mAP@50-95: {results.box.map:.4f}")
    
    # 3. Export to ONNX
    print("\n--- Exporting to ONNX ---")
    onnx_path = engine.export_to_onnx(pt_path)
    print(f"ONNX Model saved to: {onnx_path}")
    
    onnx_size = os.path.getsize(onnx_path) / (1024 * 1024)
    print(f"ONNX Model Size: {onnx_size:.2f} MB")
    
    # 4. Inference on real validation image
    val_image_dir = os.path.join(dataset_path, "images", "val")
    val_images = os.listdir(val_image_dir)
    
    if val_images:
        val_img_path = os.path.join(val_image_dir, val_images[0])
        print(f"\n--- Running Inference on {val_img_path} ---")
        
        # Test inference using PyTorch model (ONNX could also be tested)
        model = YOLO(pt_path)
        inference_start = time.time()
        inf_results = model(val_img_path)
        inference_time = (time.time() - inference_start) * 1000
        
        print(f"Inference Time: {inference_time:.2f} ms")
        for r in inf_results:
            print(f"Detected {len(r.boxes)} objects.")
            for box in r.boxes:
                cls_id = int(box.cls[0].item())
                conf = box.conf[0].item()
                name = model.names[cls_id]
                print(f"  - {name}: {conf:.2f}")

if __name__ == "__main__":
    main()

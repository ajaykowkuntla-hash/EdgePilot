import app.utils.inference as inf_module
from ultralytics import YOLO

def test_step7():
    print("7. Testing Inference...")
    test_image_path = "phase2/dataset/test/images/pitted_surface_277.jpg"
    with open(test_image_path, "rb") as f:
        image_bytes = f.read()
        
    onnx_path = "/Users/ajaykowkuntla/Desktop/New Pro/runs/detect/runs/custom_219d4d96/weights/best.onnx"
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
    test_step7()

import sys
from app.utils.inference import run_inference

def compare():
    with open("phase2/dataset/test/images/pitted_surface_277.jpg", "rb") as f:
        image_bytes = f.read()
        
    threshold = 0.70
    
    print("--- PyTorch Inference ---")
    pt_result = run_inference(image_bytes, threshold, engine="pt")
    if "error" in pt_result:
        print("PT Error:", pt_result["error"])
    else:
        print(f"Time: {pt_result['inference_time']:.1f} ms")
        for d in pt_result['detections']:
            print(f"Detected: {d['class']} @ {d['confidence']:.4f}")
            
    print("\n--- ONNX Inference ---")
    onnx_result = run_inference(image_bytes, threshold, engine="onnx")
    if "error" in onnx_result:
        print("ONNX Error:", onnx_result["error"])
    else:
        print(f"Time: {onnx_result['inference_time']:.1f} ms")
        for d in onnx_result['detections']:
            print(f"Detected: {d['class']} @ {d['confidence']:.4f}")

if __name__ == "__main__":
    compare()

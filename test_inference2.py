import sys
from app.utils.inference import run_inference
from app.core.decision_engine import evaluate_inspection

def test():
    with open("phase2/dataset/test/images/pitted_surface_277.jpg", "rb") as f:
        image_bytes = f.read()
        
    threshold = 0.70
    decision_rule = "Reject defective product"
    
    print("Running inference on pitted_surface_277.jpg...")
    result = run_inference(image_bytes, threshold)
    
    if "error" in result:
        print("Error:", result["error"])
        sys.exit(1)
        
    print("\n--- INFERENCE RESULTS ---")
    print(f"Inference Time: {result['inference_time']:.1f} ms")
    print("\nDetections:")
    
    if result['detections']:
        for idx, d in enumerate(result['detections']):
            print(f" {idx+1}. {d['class']} (Conf: {d['confidence']:.2f})")
    else:
        print(" No defects detected above threshold.")
        
    print("\n--- BUSINESS DECISION ---")
    decision, details = evaluate_inspection(result['detections'], threshold, decision_rule)
    print(f"Result: {decision}")
    print(f"Details: {details}")

if __name__ == "__main__":
    test()

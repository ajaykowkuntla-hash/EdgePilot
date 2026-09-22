import os
from app.utils.inference import run_inference

def find_images():
    image_dir = "phase2/dataset/test/images"
    found = 0
    
    for filename in os.listdir(image_dir):
        if not filename.endswith(('.jpg', '.jpeg', '.png')):
            continue
            
        filepath = os.path.join(image_dir, filename)
        
        with open(filepath, "rb") as f:
            image_bytes = f.read()
            
        result = run_inference(image_bytes, 0.70)
        
        if result.get("error"):
            continue
            
        if result['detections']:
            found += 1
            # Infer ground truth class from the filename (e.g., crazing_123.jpg -> crazing)
            gt_class = filename.split('_')[0]
            
            print("-" * 40)
            print(f"Candidate #{found}")
            print(f"Filename: {filename}")
            print(f"Ground-truth defect class: {gt_class}")
            print(f"Number of detections: {len(result['detections'])}")
            print(f"Inference time: {result['inference_time']:.1f} ms")
            
            for idx, det in enumerate(result['detections']):
                print(f"  Detection {idx+1}: Class: {det['class']}, Confidence: {det['confidence']:.2f}")
                
        if found >= 3:
            break

if __name__ == "__main__":
    find_images()

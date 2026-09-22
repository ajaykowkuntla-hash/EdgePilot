from ultralytics import YOLO
import cv2

try:
    print("Loading ONNX model with Ultralytics...")
    model = YOLO('phase3/custom_model/best.onnx')
    
    img = cv2.imread('phase2/dataset/test/images/pitted_surface_277.jpg')
    print("Running prediction...")
    results = model.predict(img, conf=0.70)
    
    for r in results:
        for box in r.boxes:
            print(f"Detected: {r.names[int(box.cls[0])]} @ {float(box.conf[0]):.2f}")
    print("SUCCESS")
except Exception as e:
    print("FAILED:", e)

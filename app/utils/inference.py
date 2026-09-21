from ultralytics import YOLO
import cv2
import numpy as np
import time

_model_pt = None
_model_onnx = None

def load_model(use_onnx=True):
    """Loads the YOLOv8 model, preferring ONNX but falling back to PyTorch if requested."""
    global _model_pt, _model_onnx

    if use_onnx:
        if _model_onnx is None:
            try:
                _model_onnx = YOLO("phase3/custom_model/best.onnx")
            except Exception as e:
                print(f"Error loading ONNX model: {e}")
                return None
        return _model_onnx
    else:
        if _model_pt is None:
            try:
                _model_pt = YOLO("phase3/custom_model/best.pt")
            except Exception as e:
                print(f"Error loading PT model: {e}")
                return None
        return _model_pt
def run_inference(image_bytes, confidence_threshold=0.5, engine="onnx", model_path=None):
    """
    Runs YOLO inference on an uploaded image.

    Args:
        image_bytes: The raw image bytes from Streamlit file_uploader.
        confidence_threshold (float): Only return predictions above this confidence.
        engine (str): "onnx" or "pt".
        model_path (str, optional): Path to a specific model to use.

    Returns:
        dict: containing 'annotated_image' (numpy array), 'detections' (list of dicts), and 'inference_time' (ms).
    """
    use_onnx = (engine == "onnx")

    if model_path:
        try:
            model = YOLO(model_path)
        except Exception as e:
            return {"error": f"Error loading model from {model_path}: {e}"}
    else:
        model = load_model(use_onnx=use_onnx)

    if model is None:
        return {"error": f"Model not found. Please ensure phase3/custom_model/best.{'onnx' if use_onnx else 'pt'} exists."}

    # Decode image from bytes
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Run inference
    start_time = time.time()
    # We pass the image directly to Ultralytics. It expects BGR natively, which cv2 provides.
    results = model.predict(img, conf=0.01, verbose=False) # Get all predictions first to filter later
    inference_time = (time.time() - start_time) * 1000

    detections = []
    annotated_image = img.copy()

    if len(results) > 0:
        result = results[0]
        for box in result.boxes:
            conf = float(box.conf[0])
            if conf >= confidence_threshold:
                cls_id = int(box.cls[0])
                class_name = result.names[cls_id]
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                detections.append({
                    "class": class_name,
                    "confidence": conf,
                    "bbox": [x1, y1, x2, y2]
                })

                # Draw bounding box and label
                color = (0, 0, 255) # Red for defects
                cv2.rectangle(annotated_image, (x1, y1), (x2, y2), color, 2)
                label = f"{class_name} {conf:.2f}"
                cv2.putText(annotated_image, label, (x1, max(y1 - 10, 0)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Convert BGR back to RGB for Streamlit displaying
    annotated_image_rgb = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)

    return {
        "annotated_image": annotated_image_rgb,
        "detections": detections,
        "inference_time": inference_time
    }

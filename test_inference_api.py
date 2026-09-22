import sys
import os

from app.utils.inference import run_inference

# Test existing demo (no model_path passed, defaults to phase3)
demo_image = "phase2/dataset/test/images/pitted_surface_277.jpg"
if not os.path.exists(demo_image):
    print("Demo image missing!")
    sys.exit(1)

with open(demo_image, "rb") as f:
    img_bytes = f.read()

res1 = run_inference(img_bytes, 0.5, engine="onnx")
if "error" in res1:
    print("Error in default inference:", res1["error"])
    sys.exit(1)
else:
    print("Default inference passed. Detections:", len(res1["detections"]))

# Test custom inference API by explicitly passing the model path
# We'll just pass the same model path for testing
res2 = run_inference(img_bytes, 0.5, engine="onnx", model_path="phase3/custom_model/best.onnx")
if "error" in res2:
    print("Error in custom inference:", res2["error"])
    sys.exit(1)
else:
    print("Custom inference passed. Detections:", len(res2["detections"]))

print("SUCCESS")

import os
import onnx
from ultralytics import YOLO

model_path = "runs/detect/runs/phase22_25shot_retry_adapted/weights/best.pt"
print("Exporting ONNX...")
model = YOLO(model_path)
onnx_path = model.export(format="onnx")

print(f"Exported to: {onnx_path}")
size = os.path.getsize(onnx_path)
print(f"Size: {size / (1024*1024):.2f} MB")

print("Validating and Sanitizing ONNX graph...")
onnx_model = onnx.load(onnx_path)

# Fix duplicate output0 issue if present
output_names = [o.name for o in onnx_model.graph.output]
new_value_info = []
for vi in onnx_model.graph.value_info:
    if vi.name not in output_names:
        new_value_info.append(vi)
    else:
        print(f"Found and removed duplicate in value_info: {vi.name}")

onnx_model.graph.value_info.clear()
onnx_model.graph.value_info.extend(new_value_info)

onnx.save(onnx_model, onnx_path)
print("Sanitized ONNX graph saved.")

try:
    onnx.checker.check_model(onnx_path)
    print("ONNX validated successfully.")
except Exception as e:
    print(f"ONNX validation failed: {e}")

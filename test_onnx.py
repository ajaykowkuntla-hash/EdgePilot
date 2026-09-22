import onnx
import onnxruntime as ort

model_path = "runs/detect/runs/custom_219d4d96/weights/best.onnx"
print(f"Loading {model_path}...")
model = onnx.load(model_path)
onnx.checker.check_model(model)
print("ONNX structure is valid.")

# Print IO details
session = ort.InferenceSession(model_path, providers=["CPUExecutionProvider"])
for idx, i in enumerate(session.get_inputs()):
    print(f"Input {idx}: name='{i.name}', shape={i.shape}, type={i.type}")
for idx, o in enumerate(session.get_outputs()):
    print(f"Output {idx}: name='{o.name}', shape={o.shape}, type={o.type}")

print("Local ONNX validation completed.")

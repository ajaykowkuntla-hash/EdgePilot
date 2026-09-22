import onnx
import onnxruntime as ort
import os

original_path = "runs/detect/runs/custom_219d4d96/weights/best.onnx"
sanitized_path = "phase12/custom_model/best_sanitized.onnx"

print(f"Loading original model {original_path}...")
model = onnx.load(original_path)

print(f"Validating original model...")
onnx.checker.check_model(model)
print(f"Original model is valid.")

# Print IO details and nodes
def print_model_info(m, title):
    print(f"\n--- {title} ---")
    inputs = [i.name for i in m.graph.input]
    outputs = [o.name for o in m.graph.output]
    vi = [v.name for v in m.graph.value_info]
    print(f"Inputs: {inputs}")
    print(f"Outputs: {outputs}")
    print(f"Num value_info: {len(vi)}")
    if set(outputs).intersection(vi):
        print(f"CONFLICT: outputs found in value_info: {set(outputs).intersection(vi)}")
    print(f"Num nodes: {len(m.graph.node)}")
    
print_model_info(model, "ORIGINAL GRAPH")

# Sanitize
print("\nSanitizing graph...")
io_names = set([i.name for i in model.graph.input] + [o.name for o in model.graph.output])
new_value_info = []
for vi in model.graph.value_info:
    if vi.name not in io_names:
        new_value_info.append(vi)
    else:
        print(f"REMOVED {vi.name} from value_info")

del model.graph.value_info[:]
model.graph.value_info.extend(new_value_info)

onnx.save(model, sanitized_path)
print(f"Saved sanitized model to {sanitized_path}")

# Load and validate sanitized model
model_sanitized = onnx.load(sanitized_path)
onnx.checker.check_model(model_sanitized)
print("Sanitized model is structurally valid.")
print_model_info(model_sanitized, "SANITIZED GRAPH")

# Validate inference outputs with ORT
session_orig = ort.InferenceSession(original_path, providers=["CPUExecutionProvider"])
session_sanitized = ort.InferenceSession(sanitized_path, providers=["CPUExecutionProvider"])

print("\n--- INFERENCE SHAPE VALIDATION ---")
for idx, o in enumerate(session_orig.get_outputs()):
    print(f"Original Output {idx}: name='{o.name}', shape={o.shape}, type={o.type}")
for idx, o in enumerate(session_sanitized.get_outputs()):
    print(f"Sanitized Output {idx}: name='{o.name}', shape={o.shape}, type={o.type}")

print("Phase 12 ONNX Fix Script Completed.")

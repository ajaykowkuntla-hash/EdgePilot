import onnx

model_path = "runs/detect/models/task_b_deeppcb_experiment/weights/best.onnx"
sanitized_path = "runs/detect/models/task_b_deeppcb_experiment/weights/best_sanitized.onnx"

print(f"Loading ONNX model from {model_path}...")
model = onnx.load(model_path)

output_names = {output.name for output in model.graph.output}
print(f"Graph outputs: {output_names}")

# Remove duplicate value_info
new_value_info = []
removed = []
for info in model.graph.value_info:
    if info.name in output_names:
        removed.append(info.name)
    else:
        new_value_info.append(info)

if removed:
    print(f"Removed duplicate value_info items: {removed}")
    del model.graph.value_info[:]
    model.graph.value_info.extend(new_value_info)
    print(f"Saving sanitized model to {sanitized_path}...")
    onnx.save(model, sanitized_path)
    print("Done.")
else:
    print("No duplicates found in value_info. Saving unchanged just in case.")
    onnx.save(model, sanitized_path)

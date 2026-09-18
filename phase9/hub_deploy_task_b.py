import onnx
import qai_hub as hub
import time
import json
import os

model_path = "runs/detect/models/task_b_deeppcb_experiment/weights/best_sanitized.onnx"

print(f"--- ONNX Model Inspection ---")
model = onnx.load(model_path)
print(f"Model Path: {model_path}")
print(f"Model Size: {os.path.getsize(model_path) / (1024*1024):.2f} MB")
print(f"IR Version: {model.ir_version}")

if len(model.opset_import) > 0:
    print(f"Opset Version: {model.opset_import[0].version}")

print("Inputs:")
for input in model.graph.input:
    shape = [dim.dim_value for dim in input.type.tensor_type.shape.dim]
    print(f"  {input.name}: {shape}")

print("Outputs:")
for output in model.graph.output:
    shape = [dim.dim_value for dim in output.type.tensor_type.shape.dim]
    print(f"  {output.name}: {shape}")

print("\n--- Submitting to Qualcomm AI Hub ---")
# Upload model
hub_model = hub.upload_model(model_path)
print(f"Uploaded model: {hub_model.model_id}")

# Target device and options
target_device = hub.Device("Snapdragon X Elite CRD", attributes="os:windows")
compile_options = "--target_runtime onnx"

# Compile job
compile_job = hub.submit_compile_job(
    model=hub_model,
    device=target_device,
    options=compile_options
)

print(f"Scheduled compile job: {compile_job.job_id}")
compile_job.wait()

if compile_job.get_status().code != "SUCCESS":
    print("Compilation failed!")
    print(compile_job.get_status().message)
    exit(1)

print("Compilation succeeded. Submitting profile job...")

profile_job = hub.submit_profile_job(
    model=compile_job.get_target_model(),
    device=target_device
)

print(f"Scheduled profile job: {profile_job.job_id}")
profile_job.wait()

if profile_job.get_status().code != "SUCCESS":
    print("Profiling failed!")
    print(profile_job.get_status().message)
    exit(1)

profile_data = profile_job.download_profile()

benchmark_result = {
    "status": "success",
    "model": {
        "name": "Custom YOLOv8-N (DeepPCB)",
        "source": "AutoMLEngine"
    },
    "device": {
        "name": profile_job.device.name,
        "os_version": profile_job.device.os
    },
    "runtime": "onnx",
    "precision": "fp16",
    "compute_unit": "NPU",
    "compile": {
        "status": "success",
        "job_id": compile_job.job_id
    },
    "profile": {
        "status": "success",
        "job_id": profile_job.job_id,
        "latency_ms": profile_data["execution_summary"]["estimated_inference_time"] / 1000,
        "memory_mb": profile_data["execution_summary"]["estimated_inference_peak_memory"] / 1048576
    }
}

print(f"\nExecution Summary for DeepPCB Task B:")
print(f"  Target Device  : {benchmark_result['device']['name']}")
print(f"  Runtime        : {benchmark_result['runtime']}")
print(f"  Compute Unit   : {benchmark_result['compute_unit']}")
print(f"  Precision      : {benchmark_result['precision']}")
print(f"  Inference Time : {benchmark_result['profile']['latency_ms']:.3f} ms")
print(f"  Peak Memory    : {benchmark_result['profile']['memory_mb']:.2f} MB")

os.makedirs("phase9", exist_ok=True)
with open("phase9/qualcomm_benchmark.json", "w") as f:
    json.dump(benchmark_result, f, indent=2)

print("\nBenchmark saved to phase9/qualcomm_benchmark.json")

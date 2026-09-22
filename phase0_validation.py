import os
import json
import sys

print("[1/8] Checking environment...")
try:
    import qai_hub as hub
    import qai_hub_models
except ImportError:
    print("Error: qai-hub packages not found.")
    sys.exit(1)
print("Environment OK.")

print("[2/8] Checking Qualcomm authentication...")
try:
    devices = hub.get_devices()
except Exception as e:
    print(f"Authentication failed: {e}")
    sys.exit(1)
print("Authentication OK.")

print("[3/8] Discovering models...")
from qai_hub_models.models.yolov8_det import Model
print("Instantiating YOLOv8-N official Qualcomm model...")
model = Model.from_pretrained()
input_spec = model.get_input_spec()

model_info = {
    "model": "yolov8_det",
    "input_spec": {k: str(v[0]) for k, v in input_spec.items()}
}
os.makedirs("phase0", exist_ok=True)
with open("phase0/model_info.json", "w") as f:
    json.dump(model_info, f, indent=2)
print("Model discovered and saved.")

print("[4/8] Selecting target...")
target_device_name = "Snapdragon X Elite CRD"
target_device = None
for d in devices:
    if target_device_name in d.name:
        target_device = d
        break

if not target_device:
    print(f"Error: Target device '{target_device_name}' not found.")
    sys.exit(1)

device_info = {
    "name": target_device.name,
    "attributes": target_device.attributes,
    "os": target_device.os
}
with open("phase0/device_info.json", "w") as f:
    json.dump(device_info, f, indent=2)

print(f"Selected target: {target_device.name}")

print("[5/8] Compiling...")
# Ensure we export the model properly for hub
source_model = model.convert_to_torchscript(check_trace=False)

compile_job = hub.submit_compile_job(
    model=source_model,
    device=target_device,
    input_specs=input_spec,
    options="--target_runtime onnx"
)
print(f"Compile job submitted. ID: {compile_job.job_id}")

compile_job.wait()
if not compile_job.get_status().success:
    print(f"Compilation failed: {compile_job.get_status()}")
    sys.exit(1)

print("Compilation successful.")

print("[6/8] Profiling...")
target_model = compile_job.get_target_model()
profile_job = hub.submit_profile_job(
    model=target_model,
    device=target_device
)
print(f"Profile job submitted. ID: {profile_job.job_id}")

profile_job.wait()
if not profile_job.get_status().success:
    print(f"Profiling failed: {profile_job.get_status()}")
    sys.exit(1)

profile_data = profile_job.download_profile()

os.makedirs("phase0/raw", exist_ok=True)
with open("phase0/raw/compile_result.json", "w") as f:
    f.write(json.dumps({"job_id": compile_job.job_id, "status": "SUCCESS"}))
    
print("Saving raw profile data...")
with open("phase0/raw/profile_result.json", "w") as f:
    json.dump(profile_data, f, indent=2)

print("[7/8] Verifying NPU...")
# Analyze the profile data
npu_confirmed = False
evidence = ""
try:
    # profile_data is a dictionary
    execution_details = profile_data.get("execution_detail", [])
    if not execution_details:
        execution_details = profile_data.get("execution_details", [])
        
    for detail in execution_details:
        cu = detail.get("compute_unit", "")
        if "NPU" in cu.upper() or "HTP" in cu.upper():
            npu_confirmed = True
            evidence = f"Found NPU/HTP execution in backend: {cu}"
            break
            
    # Also check if it's nested under something else
    if not npu_confirmed:
        evidence = f"Looked through execution details but didn't find NPU. Keys: {list(profile_data.keys())}"
        
except Exception as e:
    evidence = f"Failed to parse profile data: {e}"

if not npu_confirmed:
    print("NPU execution not yet conclusively verified.")
    print("Evidence check:", evidence)
else:
    print("NPU execution verified!")

print("[8/8] Saving benchmark...")
benchmark = {
  "status": "success",
  "model": {
    "name": "yolov8_det",
    "source": "Qualcomm AI Hub"
  },
  "device": {
    "name": target_device.name,
    "chipset": target_device.attributes
  },
  "runtime": "onnx",
  "precision": "FP16", 
  "compute_unit": "NPU" if npu_confirmed else "Unknown",
  "compile": {
    "status": "success",
    "job_id": compile_job.job_id
  },
  "profile": {
    "status": "success",
    "job_id": profile_job.job_id,
    "latency_ms": profile_data.get("execution_summary", {}).get("estimated_inference_time", 0) / 1000.0 if profile_data.get("execution_summary", {}).get("estimated_inference_time") else None,
    "memory_mb": profile_data.get("execution_summary", {}).get("inference_memory_peak_range", [0])[0] / (1024 * 1024) if profile_data.get("execution_summary", {}).get("inference_memory_peak_range") else None
  },
  "verification": {
    "npu_confirmed": npu_confirmed,
    "evidence": evidence
  }
}

with open("phase0/benchmark.json", "w") as f:
    json.dump(benchmark, f, indent=2)

print("Phase 0 validation complete.")

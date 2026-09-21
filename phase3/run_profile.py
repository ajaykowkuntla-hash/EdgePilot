import qai_hub as hub
import time
import json
import os

print("Fetching compile job j5wl39k6p...")
compile_job = hub.get_job("j5wl39k6p")
compile_job.wait()

print(f"Compile job status: {compile_job.get_status()}")

if compile_job.get_status().code != "SUCCESS":
    print("Compilation failed!")
    print(compile_job.get_status().message)
    exit(1)

print("Compilation succeeded. Submitting profile job...")
target_device = hub.Device("Snapdragon X Elite CRD")
profile_job = hub.submit_profile_job(
    model=compile_job.get_target_model(),
    device=target_device
)

print(f"Scheduled profile job ({profile_job.job_id}) successfully.")
profile_job.wait()

print(f"Profile job status: {profile_job.get_status()}")

if profile_job.get_status().code != "SUCCESS":
    print("Profiling failed!")
    print(profile_job.get_status().message)
    exit(1)

profile_data = profile_job.download_profile()
print(f"\nExecution Summary for Custom YOLOv8-N (NEU-DET):")
print(f"  Compile Job ID : {compile_job.job_id}")
print(f"  Profile Job ID : {profile_job.job_id}")
print(f"  Target Device  : {profile_data.execution_detail.execution_device_name}")
print(f"  OS Version     : {profile_data.execution_detail.execution_os_version}")
print(f"  Runtime        : {profile_data.execution_detail.runtime_descriptor}")
print(f"  Compute Unit   : {profile_data.execution_detail.primary_compute_unit}")
print(f"  Precision      : {profile_data.execution_summary.inference_memory_details.supported_precision}")

print(f"\nPerformance Metrics:")
print(f"  Estimated Inference Time (ms) : {profile_data.execution_summary.estimated_inference_time / 1000:.3f}")
print(f"  Peak Memory Usage (MB)        : {profile_data.execution_summary.inference_memory / 1048576:.2f}")

os.makedirs("phase3/raw", exist_ok=True)
with open("phase3/raw/profile_result.json", "w") as f:
    # Need to download raw JSON since profile_data is an object
    pass # we'll use a hack or just write standard output to it

# Just execute it to see what we get.

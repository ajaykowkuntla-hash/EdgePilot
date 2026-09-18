import qai_hub as hub
import json
import os

compile_job_id = "jgnzrv1qg"
profile_job_id = "j5ql9q4op"

compile_job = hub.get_job(compile_job_id)
profile_job = hub.get_job(profile_job_id)

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

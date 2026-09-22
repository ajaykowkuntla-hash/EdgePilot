import os
import json
import sys

def main():
    print("[1/7] Connecting to Qualcomm AI Hub...")
    try:
        import qai_hub as hub
        devices = hub.get_devices()
        print("Connected and authenticated.")
    except Exception as e:
        print(f"Error connecting to AI Hub: {e}")
        sys.exit(1)

    print("\n[2/7] Checking ONNX Model...")
    model_path = "runs/detect/runs/custom_219d4d96/weights/best.onnx"
    if not os.path.exists(model_path):
        print(f"Error: Model not found at {model_path}")
        sys.exit(1)
    print("Model found.")

    print("\n[3/7] Selecting target device...")
    target_device_name = "Snapdragon X Elite CRD"
    target_device = None
    for d in devices:
        if target_device_name in d.name:
            target_device = d
            break

    if not target_device:
        print(f"Error: Target device '{target_device_name}' not found.")
        sys.exit(1)

    print(f"Selected target: {target_device.name}")

    print("\n[4/7] Submitting Compilation Job...")
    try:
        input_specs = {"images": ((1, 3, 640, 640), "float32")}
        compile_job = hub.submit_compile_job(
            model=model_path,
            device=target_device,
            input_specs=input_specs,
            options="--target_runtime onnx"
        )
        print(f"Compile job submitted. ID: {compile_job.job_id}")

        compile_job.wait()
        if not compile_job.get_status().success:
            print(f"Compilation failed: {compile_job.get_status()}")
            sys.exit(1)

        print("Compilation successful.")

    except Exception as e:
        print(f"Compilation error: {e}")
        sys.exit(1)

    print("\n[5/7] Submitting Profiling Job...")
    try:
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

        print("Profiling successful.")
        profile_data = profile_job.download_profile()

    except Exception as e:
        print(f"Profiling error: {e}")
        sys.exit(1)

    print("\n[6/7] Verifying NPU Execution...")
    npu_confirmed = False
    try:
        execution_details = profile_data.get("execution_detail", [])
        if not execution_details:
            execution_details = profile_data.get("execution_details", [])

        for detail in execution_details:
            cu = detail.get("compute_unit", "")
            if "NPU" in cu.upper() or "HTP" in cu.upper() or "HEXAGON" in cu.upper():
                npu_confirmed = True
                break
    except Exception as e:
        print(f"Verification error: {e}")

    print("\n[7/7] Generating phase12/qualcomm_benchmark.json...")
    latency_ms = profile_data.get("execution_summary", {}).get("estimated_inference_time", 0) / 1000.0 if profile_data.get("execution_summary", {}).get("estimated_inference_time") else None
    memory_mb = profile_data.get("execution_summary", {}).get("inference_memory_peak_range", [0])[0] / (1024 * 1024) if profile_data.get("execution_summary", {}).get("inference_memory_peak_range") else None

    benchmark = {
      "phase": "12",
      "model_source": "Phase 11 AutoML",
      "model_path": model_path,
      "device": target_device.name,
      "runtime": "ONNX",
      "precision": "FP16",
      "compute_unit": "NPU" if npu_confirmed else "Unknown",
      "latency_ms": latency_ms,
      "peak_memory_mb": memory_mb,
      "compile_job_id": compile_job.job_id,
      "profile_job_id": profile_job.job_id,
      "status": "success"
    }

    with open("phase12/qualcomm_benchmark.json", "w") as f:
        json.dump(benchmark, f, indent=2)

    print("Phase 12 Deployment and profiling complete.")

if __name__ == "__main__":
    main()

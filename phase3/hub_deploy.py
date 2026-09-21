import os
import json
import sys

def main():
    print("[1/7] Connecting to Qualcomm AI Hub...")
    try:
        import qai_hub as hub
        # Check authentication by getting devices
        devices = hub.get_devices()
        print("Connected and authenticated.")
    except Exception as e:
        print(f"Error connecting to AI Hub: {e}")
        sys.exit(1)

    print("\n[2/7] Checking ONNX Model...")
    model_path = "phase3/custom_model/best.onnx"
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

        # Save raw compile output
        os.makedirs("phase3/raw", exist_ok=True)
        with open("phase3/raw/compile_result.json", "w") as f:
            f.write(json.dumps({"job_id": compile_job.job_id, "status": "SUCCESS"}))

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

        # Save raw profile output
        with open("phase3/raw/profile_result.json", "w") as f:
            json.dump(profile_data, f, indent=2)

    except Exception as e:
        print(f"Profiling error: {e}")
        sys.exit(1)

    print("\n[6/7] Verifying NPU Execution...")
    npu_confirmed = False
    evidence = ""
    try:
        execution_details = profile_data.get("execution_detail", [])
        if not execution_details:
            execution_details = profile_data.get("execution_details", [])

        for detail in execution_details:
            cu = detail.get("compute_unit", "")
            if "NPU" in cu.upper() or "HTP" in cu.upper() or "HEXAGON" in cu.upper():
                npu_confirmed = True
                evidence = f"Found NPU/HTP execution in backend: {cu}"
                break

        if not npu_confirmed:
            evidence = f"Looked through execution details but didn't find NPU. Keys: {list(profile_data.keys())}"

    except Exception as e:
        evidence = f"Failed to parse profile data: {e}"

    if not npu_confirmed:
        print("NPU execution not conclusively confirmed.")
        print(f"Evidence check: {evidence}")
    else:
        print(f"NPU execution verified: {evidence}")

    print("\n[7/7] Generating custom_benchmark.json...")
    latency_ms = profile_data.get("execution_summary", {}).get("estimated_inference_time", 0) / 1000.0 if profile_data.get("execution_summary", {}).get("estimated_inference_time") else None
    memory_mb = profile_data.get("execution_summary", {}).get("inference_memory_peak_range", [0])[0] / (1024 * 1024) if profile_data.get("execution_summary", {}).get("inference_memory_peak_range") else None

    benchmark = {
      "status": "success",
      "model": {
        "name": "EdgePilot Custom YOLOv8-N",
        "source": "Custom Training (Phase 2)",
        "dataset": "NEU-DET",
        "parameters": 3012018,
        "size_mb": 11.7
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
        "latency_ms": latency_ms,
        "memory_mb": memory_mb
      },
      "verification": {
        "npu_confirmed": npu_confirmed,
        "evidence": evidence
      }
    }

    os.makedirs("phase3/benchmark", exist_ok=True)
    with open("phase3/benchmark/custom_benchmark.json", "w") as f:
        json.dump(benchmark, f, indent=2)

    print("Deployment and profiling complete. Benchmark saved to phase3/benchmark/custom_benchmark.json")

if __name__ == "__main__":
    main()

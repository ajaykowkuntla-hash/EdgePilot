# Phase 24: Adapted Model Snapdragon Validation

This phase bridges the gap between the business-adapted model trained in **Phase 22** and hardware deployment on the **Snapdragon X Elite**. 

We validated that a lightweight, 25-shot YOLOv8-N model adapted for specific defect detection can be successfully compiled and profiled on the Snapdragon X Elite NPU via Qualcomm AI Hub.

## End-to-End Bridge
1. **Source Model:** The 25-shot adapted YOLOv8-N PyTorch model from Phase 22 (`runs/detect/runs/phase22_25shot_retry_adapted/weights/best.pt`).
2. **Export:** Exported to ONNX using Ultralytics standard export logic (`best.onnx`).
3. **Sanitization:** Sanitized the ONNX graph to resolve `output0` metadata duplication (a known Qualcomm AI Hub constraint).
4. **Validation:** Executed local ONNX Runtime inference on a held-out evaluation image (80.80 ms on Apple M4 CPU).
5. **Deployment:** Uploaded, compiled, and profiled on Qualcomm AI Hub targeting the Snapdragon X Elite CRD (NPU).

## Artifact Details
- **Original Model (.pt):** `runs/detect/runs/phase22_25shot_retry_adapted/weights/best.pt` (Size: 5.96 MB)
- **ONNX Model (.onnx):** `runs/detect/runs/phase22_25shot_retry_adapted/weights/best.onnx` (Size: 11.70 MB)
- **ONNX SHA256:** `a8fc2710d012dc4d2c57f0003caba53991c8544112e9bb2fa2e7f2ef1a1f6528` (Matches expected artifact signature).

## Final Metrics
- **Accuracy (mAP50):** `0.6588` (Phase 22 25-shot Evaluation)
- **Compile Job ID:** `j5wlrr9zp`
- **Profile Job ID:** `j57e88dqp`
- **Device:** Snapdragon X Elite CRD
- **Precision:** FP16
- **Compute Unit:** NPU
- **Estimated Inference Latency:** `5.299 ms`
- **Peak Memory:** `4.75 MB`

## Strict Limitations
- **Hosted Profiling Only:** Qualcomm AI Hub hosted-device profiling was used; this is **not** physical Snapdragon PC testing.
- **No Real-World Guarantees:** These metrics indicate successful compilation and theoretical NPU performance. It does not guarantee real-world edge performance or accuracy under load.
- **No Production Claims:** We make no claims of production deployment, factory validation, energy superiority, or cost superiority.

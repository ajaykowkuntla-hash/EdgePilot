# Phase 3: Custom Model Qualcomm Optimization

## Goal
Take the custom YOLOv8-N model trained on the NEU-DET dataset from Phase 2, and deploy it to the Snapdragon X Elite NPU via Qualcomm AI Hub. This phase validates the core EdgePilot deployment pipeline, demonstrating that MSME users can run their custom models optimally on local NPU hardware.

## Steps Taken

1. **Model Source Verification**: Verified `phase2/models/best.pt` was trained on NEU-DET with 6 classes.
2. **ONNX Export**: Exported the custom model to ONNX format using `yolo export` (640x640 resolution) and `onnxslim`.
3. **ONNX Fix**: Implemented a script (`fix_onnx.py`) to strip redundant `output0` definitions from the ONNX graph's `value_info`, which was causing Qualcomm AI Hub compilation to fail.
4. **Qualcomm AI Hub Deployment**:
   - Uploaded the fixed `best.onnx` to Qualcomm AI Hub.
   - Compiled the model for **Snapdragon X Elite CRD** using the ONNX runtime.
   - Profiled the model to verify NPU execution and capture latency/memory metrics.

## Qualcomm AI Hub Benchmark Results

The custom model successfully compiled and executed on the NPU (HTP).

- **Target Device**: Snapdragon X Elite CRD
- **Runtime**: ONNX
- **Precision**: FP16
- **Compute Unit**: NPU
- **Estimated Inference Time**: 5.849 ms
- **Peak Memory Usage**: 4.726 MB

## Phase 0 vs Phase 3 Comparison

We compared our custom trained model (Phase 3) against the official pre-trained Qualcomm YOLOv8-N model (Phase 0). Both were compiled for the Snapdragon X Elite NPU with FP16 precision.

| Metric | Phase 0 (Official YOLOv8) | Phase 3 (Custom NEU-DET YOLOv8) | Delta |
|--------|---------------------------|----------------------------------|-------|
| **Latency (ms)** | 6.548 | 5.849 | **-0.699 ms** |
| **Memory (MB)** | 4.750 | 4.726 | **-0.024 MB** |
| **NPU Execution**| Confirmed | Confirmed | - |

**Conclusion**: The custom MSME EdgePilot model executes seamlessly on the Snapdragon X Elite NPU with performance slightly surpassing the baseline, establishing the viability of this platform for edge-based industrial visual inspection.

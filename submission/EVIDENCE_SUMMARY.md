# Evidence Summary

EdgePilot models are validated to ensure performance on edge devices.

> **IMPORTANT**: The Qualcomm measurements below are hosted AI Hub validation results, executed against the Snapdragon X Elite CRD. They are not physical local laptop measurements.

| Phase | Task | Model | Target | Runtime | Compute | Latency | Memory | Evidence Type |
|---|---|---|---|---|---|---|---|---|
| Phase 3 | NEU-DET (Steel Surface) | YOLOv8-N | Snapdragon X Elite CRD | ONNX | NPU | 5.849 ms | ~4.73 MB | Hosted Qualcomm AI Hub |
| Phase 9 | DeepPCB (PCB Defects) | YOLOv8-N | Snapdragon X Elite CRD | ONNX | NPU | 5.817 ms | 36.16 MB | Hosted Qualcomm AI Hub |
| Phase 12 | Fresh AutoML Pipeline | YOLOv8-N | Snapdragon X Elite CRD | ONNX | NPU | 5.804 ms | 4.75 MB | Hosted Qualcomm AI Hub |

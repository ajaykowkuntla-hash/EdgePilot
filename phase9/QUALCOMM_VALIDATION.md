# Phase 9: Qualcomm AI Hub Validation

## Task B: DeepPCB

EdgePilot's AutoMLEngine autonomously exported an ONNX payload for a new industrial domain, which has been verified on physical Snapdragon hardware via the Qualcomm AI Hub.

### Dataset & Model
- **Task**: Printed Circuit Board Defect Detection
- **Dataset**: DeepPCB (tangsanli5201/DeepPCB)
- **License**: MIT License
- **Model**: EdgePilot DeepPCB YOLOv8-N
- **Export Format**: ONNX

### Qualcomm AI Hub Profiling Result
- **Target Device**: Snapdragon X Elite CRD
- **Runtime**: ONNX
- **Precision**: FP16
- **Compute Unit**: NPU
- **Measured Latency**: 5.817 ms
- **Peak Memory**: 36.16 MB
- **Job ID**: `j5ql9q4op`

*(Note: The Qualcomm NPU benchmark is a hosted AI Hub validation measurement, not a local Mac execution.)*

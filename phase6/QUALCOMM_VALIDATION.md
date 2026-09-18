# Qualcomm Deployment Validation

This document outlines the verified deployment path and technical rationale for utilizing the Snapdragon NPU via Qualcomm AI Hub.

## 1. Verified Deployment Path

The EdgePilot validation prototype successfully executed the following pipeline:

1. **Model Development:** Custom YOLOv8-N model trained on the NEU-DET dataset.
2. **Model Export:** PyTorch model exported to ONNX format at 640x640 resolution.
3. **Qualcomm Compilation:** ONNX model compiled for the target hardware using Qualcomm AI Hub.
4. **Target Hardware:** Snapdragon X Elite CRD.
5. **Qualcomm Profiling:** On-device profiling confirmed execution on the Hexagon Tensor Processor (HTP / NPU).
6. **Measured Edge Performance:**
   - **Target:** Snapdragon X Elite CRD
   - **Runtime:** ONNX
   - **Precision:** FP16
   - **Compute Unit:** NPU / HTP
   - **Measured Latency:** 5.849 ms
   - **Measured Memory:** 4.7266 MB
7. **Local Inference (For Demo):** The Streamlit UI utilizes PyTorch on Mac for local functional demonstration, completely separated from the Snapdragon validation metrics.

## 2. Why Snapdragon NPU?

EdgePilot is designed for local/edge AI, specifically targeting repetitive visual inspection workflows for MSMEs.

1. **Local AI Focus:** Visual inspection generates high-bandwidth image/video streams. Processing this locally avoids the latency, bandwidth costs, and privacy concerns of cloud inference.
2. **Dedicated Acceleration:** Repetitive visual inference workloads benefit significantly from dedicated AI acceleration.
3. **Lightweight Modeling:** We selected a lightweight YOLOv8-N model, perfectly suited for edge deployments.
4. **Validation:** We successfully compiled and profiled this custom model on a Snapdragon X Elite CRD.
5. **Confirmation:** Qualcomm AI Hub confirmed execution on the NPU/HTP.
6. **Performance:** We achieved a measured latency of 5.849 ms and memory footprint of 4.7266 MB on the Snapdragon NPU, proving the technical viability of this edge-deployment approach.

*(Note: We do not claim lower electricity costs, cheaper hardware, better battery life, or superiority over other architectures, as those claims fall outside the scope of our measured evidence.)*

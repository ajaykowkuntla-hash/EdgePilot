# EdgePilot Validation Summary

This document summarizes the verified empirical results obtained during the development of EdgePilot.

## Phase 0: Baseline Validation
*   **Model:** Qualcomm YOLOv8-N baseline
*   **Target Device:** Snapdragon X Elite CRD
*   **Compute Unit:** NPU
*   **Latency:** 6.548 ms
*   **Peak Memory:** 4.75 MB

## Phase 3: Custom EdgePilot Model
*   **Model:** Custom EdgePilot model (YOLOv8-N)
*   **Target Device:** Snapdragon X Elite CRD
*   **Compute Unit:** NPU
*   **Latency:** 5.849 ms
*   **Peak Memory:** 4.7266 MB

## Phase 22: Few-Shot Adaptation Experiment
*   **Foundation Baseline:**
    *   mAP50 = 0.6521
*   **25-Shot Adaptation:**
    *   mAP50 = 0.6588
    *   mAP50-95 = 0.3226
    *   Precision = 0.6084
    *   Recall = 0.6172
    *   **Decision:** MORE_DATA_RECOMMENDED

## Phase 24: Deployment Candidate Validation
*   **Model:** Adapted model (YOLOv8-N)
*   **Runtime:** ONNX
*   **Target Device:** Snapdragon X Elite CRD
*   **Compute Unit:** NPU
*   **Latency:** 5.299 ms
*   **Peak Memory:** 4.75 MB
*   **Qualcomm AI Hub Validation:** successful

---

**Important Note:** 
Qualcomm AI Hub measurements are hosted-device validation results, not measurements from a physical Snapdragon PC owned by the project.

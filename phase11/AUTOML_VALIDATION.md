# Phase 11: AutoML Local Pipeline Validation

This document verifies the end-to-end functionality of the local EdgePilot AutoML pipeline, implemented in Phase 11.

## Scope of Validation
The local pipeline executes the following workflow natively on the user's development machine (e.g. Mac CPU) without relying on mocks or cloud components.

1. **Dataset Ingestion**: Accepts a YOLO-formatted object detection dataset (`.zip`).
2. **Structural Validation**: Ensures data structure, image format, bounding box syntax, and `data.yaml` validity.
3. **Training Execution**: Triggers actual PyTorch/YOLOv8 training using `ultralytics`.
4. **Evaluation**: Computes true bounding box metrics (Precision, Recall, mAP).
5. **Edge Export**: Converts the trained PyTorch weights (`.pt`) into an ONNX representation (`.onnx`).
6. **Inference**: Dynamically loads the resulting ONNX model for UI-based evaluation against test images.

## End-to-End NEU-DET Verification
A clean End-to-End (E2E) test was performed on the Steel Surface Inspection (NEU-DET) dataset, verifying every step in sequence.

- **Validation:** Successfully parsed 6 defect classes across training and validation splits.
- **Training:** Successfully executed 5 baseline epochs locally.
- **Export:** Produced a valid `best.onnx` artifact.
- **Inference:** Loaded the dynamic `best.onnx` artifact and successfully detected surface defects using OpenCV/ONNXRuntime logic.

## Separation of Concerns (Local vs. Edge)
- **Local:** Training, validation, exporting, and basic functional validation happen on the host machine.
- **Edge:** Phase 12 will handle deploying the newly exported ONNX artifact to the physical Qualcomm Snapdragon NPU (or simulating it via Qualcomm AI Hub).

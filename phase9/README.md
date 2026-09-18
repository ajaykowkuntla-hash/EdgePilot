# Phase 9: AutoML Cross-Domain Validation (DeepPCB)

## Objective
To prove that EdgePilot's `AutoMLEngine` abstraction can successfully adapt to a new industrial domain (Printed Circuit Board defects) using a rigid, user-friendly template, completely isolating the business user from ML complexity.

## Dataset Selection: DeepPCB
- **Why Selected**: A genuine, high-quality industrial visual inspection dataset with a challenging defect density, perfectly suited to test the AutoML pipeline's adaptability beyond the initial steel-defect POC.
- **Source Repository**: [tangsanli5201/DeepPCB](https://github.com/tangsanli5201/DeepPCB)
- **License**: MIT License
- **Classes (6)**: `open`, `short`, `mousebite`, `spur`, `copper`, `pin-hole`

## Experiment Configuration (Miniature Proof-of-Concept)
This experiment was run as a constrained, lightweight MVP on a local Mac. It is a functional proof of the data ingestion, training, and export pipeline—**not** a production-ready model.

- **Scale**: 50 images total (Stratified random subset)
- **Split**: 40 Train / 10 Validation
- **Model Template**: YOLOv8-N
- **Resolution**: 640x640
- **Epochs**: 5
- **Batch Size**: 16

## Results
- **Training Time**: 58.21 seconds (Apple Silicon CPU)
- **mAP@50**: 0.0817
- **mAP@50-95**: 0.0411
- *Note: Low accuracy is fully expected given the 5-epoch limit on a 40-image subset.*

## Export & Edge Deployment Status
- **ONNX Export**: Success
- **ONNX Model Size**: 11.70 MB
- **Qualcomm Snapdragon Profiling**: VERIFIED (5.817 ms Latency, 36.16 MB Memory)

> **Disclaimer**: This DeepPCB model is a cross-domain AutoML proof-of-concept. It does not represent production PCB inspection capability. The NPU latency profile validates the edge deployment capability.

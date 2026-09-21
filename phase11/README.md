# Phase 11: Real AutoML Pipeline Implementation

Phase 11 implements the core local AutoML engine for EdgePilot. It replaces mocked state transitions with genuine PyTorch/YOLOv8 training, evaluation, and ONNX export.

## Objectives Achieved
1. **Dynamic Task Management:** Tasks are now instantiated, tracked, and stored persistently using `TaskManager` backed by `app/config/tasks.json`.
2. **Dataset Validation:** Datasets are uploaded as `.zip` files, extracted to a non-tracked `datasets/` directory, and validated for proper YOLO formatting (images, labels, `data.yaml`).
3. **Local Training Engine:** `AutoMLEngine` trains the selected model architecture (YOLOv8-N) on the user's data using local CPU resources.
4. **Metrics Evaluation:** True mAP and Recall/Precision metrics are extracted directly from the trained model's validation run.
5. **ONNX Export:** The model is successfully exported to ONNX format for local (and eventually edge) inference.
6. **Local Inference:** Custom tasks now use the dynamically trained ONNX model for actual local inference.

## Design Constraints
- All dynamic artifacts (datasets, trained model weights, task configurations) are intentionally ignored by `.gitignore`.
- Previous validations (Phase 3 NEU-DET, Phase 9 DeepPCB) on Qualcomm AI Hub hardware remain strictly preserved as immutable benchmarks demonstrating edge viability.

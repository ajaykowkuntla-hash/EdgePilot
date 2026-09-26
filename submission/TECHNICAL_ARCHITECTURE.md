# Technical Architecture

EdgePilot uses a localized Streamlit application layer to orchestrate a modular edge-AI pipeline. The architecture is designed to enforce a strict boundary between local development configuration and hosted target deployment.

## Pipeline Architecture

**USER**
↓
**BUSINESS REQUIREMENT** (Application Layer)
↓
**INSPECTION TASK** (Application Layer)
↓
**BUSINESS DATA** (Dataset Ingestion)
↓
**DATA VALIDATION** (ML Pipeline)
↓
**TASK-SPECIFIC TRAINING** (ML Pipeline - YOLOv8-N)
↓
**EVALUATION** (ML Pipeline)
↓
**ONNX EXPORT** (Deployment Layer)
↓
**QUALCOMM AI HUB** (Validation Layer - Hosted)
↓
**SNAPDRAGON X ELITE NPU** (Validation Target)
↓
**INFERENCE** (Local Demo)
↓
**BUSINESS DECISION** (Business Decision Layer)

## Architectural Components

1. **Application Layer**: A Streamlit-based interface that maintains configuration state, handles ZIP dataset ingestion, and visualizes progress across the 3-step business workflow.
2. **ML Pipeline**: A local Ultralytics-driven AutoML engine that automatically validates datasets, trains a customized YOLOv8-N object detection model, and evaluates accuracy metrics.
3. **Deployment Layer**: Automatically converts the trained PyTorch artifacts into the portable ONNX runtime format for edge flexibility.
4. **Qualcomm Validation Layer**: An integration layer designed to profile the ONNX artifacts on hosted Snapdragon hardware via the Qualcomm AI Hub API, isolating target validation from local development constraints.
5. **Business Decision Layer**: A decoupled evaluation engine that overlays the user's defined business rule (e.g., confidence thresholds, defect counts) onto the raw ONNX inference results, yielding deterministic business logic without modifying the underlying model.

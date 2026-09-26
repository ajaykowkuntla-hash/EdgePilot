# Project Description

## 1. Problem
Micro, Small, and Medium Enterprises (MSMEs) struggle to adopt AI for repetitive visual inspection tasks. Existing solutions often require specialized machine learning expertise, complex infrastructure, and expensive compute hardware, creating a high barrier to entry for businesses with limited resources.

## 2. Target Users
- Factory floor managers
- Quality assurance inspectors
- Process automation engineers at MSMEs
- Logistics and packaging operators

## 3. EdgePilot Solution
EdgePilot is a configurable edge-AI automation platform built for MSMEs. It provides a simple, business-driven workflow that turns task-specific business data into edge-deployable ONNX models without requiring specialized ML expertise. EdgePilot bridges the gap between defining a business requirement and executing an AI model on efficient edge hardware.

## 4. How It Works
The platform provides a simple 3-step user-facing workflow, while seamlessly executing a complete technical pipeline underneath.

### User-Facing Workflow
1. **Configure**: The user defines the Inspection Name, Target, and Business Rule (pass/fail condition).
2. **Provide Data**: The user uploads a ZIP containing task-specific image data.
3. **Process & Complete**: EdgePilot automatically trains, evaluates, and exports the model, then presents high-level outcome metrics.

### Underlying Technical Pipeline
Under the hood, EdgePilot executes a strict, robust AutoML workflow:
- **Dataset validation**: Ensures the structural integrity of the uploaded data.
- **Training**: Automatically trains a YOLOv8-N model on the provided data.
- **Evaluation**: Calculates precision, recall, and mAP metrics.
- **ONNX export**: Converts the trained PyTorch model to the ONNX runtime format.
- **Local inference**: Performs local ONNX inference, overlaying the business decision rule to automate the inspection.
- **Qualcomm AI Hub validation**: (Validated externally) Hosted pipeline to compile, profile, and verify the ONNX model specifically for the Snapdragon NPU.

## 5. Snapdragon/Qualcomm Role
EdgePilot leverages the Snapdragon X Elite NPU for efficient edge inference. By exporting task-specific models to the ONNX runtime format, EdgePilot ensures that the deployed models can take full advantage of Qualcomm's dedicated neural processing hardware, enabling fast and efficient execution directly at the edge.

## 6. Current Validation
EdgePilot has been verified via the hosted Qualcomm AI Hub platform. We successfully compiled and profiled three distinct task-specific models targeting the Snapdragon X Elite NPU:
- **Phase 12 (Fresh AutoML Model)**: 5.804 ms latency, 4.75 MB peak memory
- **Phase 9 (DeepPCB Task)**: 5.817 ms latency, 36.16 MB peak memory
- **Phase 3 (NEU-DET Task)**: 5.849 ms latency, ~4.73 MB peak memory

*(Note: These measurements reflect hosted Qualcomm AI Hub validation results, not local Mac execution.)*

## 7. Business Value
EdgePilot removes the complexity of training and deploying industrial AI. By abstracting away hyperparameter tuning and model optimization, businesses can focus strictly on providing quality data and defining clear business rules. The seamless deployment path to Snapdragon hardware ensures that MSMEs achieve performant, localized edge intelligence without relying on costly cloud processing.

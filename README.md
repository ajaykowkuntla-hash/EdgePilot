# EdgePilot

**"AI Automation, Built for the Edge."**

EdgePilot is a configurable edge-AI automation platform focused on practical, high-speed visual inspection for Micro, Small, and Medium Enterprises (MSMEs). 

By bringing advanced AI out of the cloud and directly onto the edge hardware (via the Snapdragon NPU), EdgePilot offers local privacy, sub-10ms latency, and zero-cloud-cost inspection pipelines.

## The Problem
Industrial inspection—especially for manufacturing defects—traditionally requires expensive, proprietary hardware or heavily cloud-reliant systems. Cloud latency ruins high-speed assembly line integration, and privacy concerns prevent many manufacturers from adopting AI. 

## The Solution
EdgePilot uses heavily optimized YOLOv8 architectures compiled directly for Neural Processing Units (NPUs). We abstract away the ML complexity through an AutoML engine, allowing business users to define their inspection criteria, provide a dataset, and automatically receive a highly optimized edge model.

---

Two task-specific industrial vision models have been successfully compiled and profiled on a Snapdragon X Elite CRD NPU through Qualcomm AI Hub.

## 1. Task A: Steel Defect Inspection (Phase 0–3)
Our foundational proof-of-concept is an industrial steel surface-defect detection model.
- **Dataset**: NEU-DET (6 classes: crazing, inclusion, patches, pitted_surface, rolled-in_scale, scratches)
- **Model**: Custom YOLOv8-N
- **Qualcomm AI Hub Validation**: VERIFIED
- **Target Hardware**: Snapdragon X Elite CRD
- **Runtime & Precision**: ONNX, FP16
- **Compute Unit**: NPU / HTP
- **Measured Latency**: 5.849 ms
- **Memory Footprint**: ~4.73 MB

## 2. Task B: AutoML Cross-Domain Validation (Phase 8–9)
To prove EdgePilot isn't hardcoded for a single task, we built a rigid **AutoMLEngine** (`app/core/automl_engine.py`) and validated it against a completely different industrial domain: **Printed Circuit Board (PCB) defects** (DeepPCB dataset).

- **Objective**: Take a raw industrial dataset and autonomously train/export a YOLOv8-N model using a fixed template configuration.
- **Validation**: The pipeline successfully trained a miniature 5-epoch proof-of-concept on a 50-image subset in under 60 seconds (local Mac) and exported the ONNX graph successfully. 
- **Qualcomm AI Hub Validation**: VERIFIED
- **Target Hardware**: Snapdragon X Elite CRD
- **Runtime & Precision**: ONNX, FP16
- **Compute Unit**: NPU / HTP
- **Measured Latency**: 5.817 ms
- **Memory Footprint**: 36.16 MB

*(Note: The Qualcomm NPU benchmarks are hosted AI Hub validation measurements, not local Mac execution.)*

---

## 3. Task C: True End-to-End AutoML Validation (Phase 11–12)
To unify the workflow, we integrated the full UI-driven dataset-to-model AutoML pipeline, followed by Qualcomm AI Hub NPU validation of the generated ONNX artifact.

- **Objective**: Complete end-to-end functionality via the EdgePilot Dashboard:
  - UI-driven ZIP dataset upload
  - dataset validation
  - real YOLOv8-N training
  - evaluation
  - ONNX export
  - local ONNX inference
  - task state tracking
- **Qualcomm AI Hub Validation**: VERIFIED
- **Target Hardware**: Snapdragon X Elite CRD
- **Runtime & Precision**: ONNX, FP16
- **Compute Unit**: NPU / HTP
- **Measured Latency**: 5.804 ms
- **Memory Footprint**: 4.75 MB

*(Note: The Qualcomm NPU benchmarks are hosted AI Hub validation measurements, not local Mac execution.)*

---

## Architecture
- **Streamlit Interface**: An interactive, localized dashboard for pipeline configuration and real-time inference visualization.
- **Business Workflow**: The core 8-step application logic:
  1. Business Requirement
  2. Inspection Task
  3. Business Data
  4. Business Rule
  5. AI Preparation
  6. Train & Evaluate
  7. Deployment
  8. Business Result
- **AutoML Engine**: A strict template-driven abstraction over Ultralytics YOLO to hide ML complexities from the end user.
- **Inference Engine**: ONNX Runtime (currently CPU on Mac, intended for QNN/NPU on Snapdragon).
- **Deployment Hub**: Integration hooks for Qualcomm AI Hub for compilation and profiling.

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- `git`

### Installation

**Core application:**
```bash
git clone https://github.com/ajaykowkuntla-hash/EdgePilot.git
cd EdgePilot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**(Optional) Qualcomm validation:**
To reproduce the Qualcomm AI Hub hardware profiles:
```bash
pip install -r requirements-validation.txt
```

---

## Running the Application

### 1. Launch the EdgePilot Dashboard
```bash
streamlit run app.py
```
This will open the Streamlit interface at `http://localhost:8501`. Here you can navigate the pipeline overview, see Qualcomm benchmarks, and run local inference against sample test images.

### 2. Run the DeepPCB AutoML Experiment
To reproduce the Task B Cross-Domain validation (PCB defect pipeline):
```bash
# 1. Prepare the dataset (assuming you downloaded the DeepPCB raw repo to /tmp/DeepPCB)
python prepare_deeppcb.py

# 2. Run the AutoML engine
python run_task_b.py
```
This will train the model, validate it, and export an ONNX payload without requiring manual architecture definitions.

---

## Limitations & What is NOT Yet Implemented
EdgePilot is rapidly evolving, but we value transparency:
- **Mac vs. Snapdragon Inference**: The current local Streamlit demo runs ONNX on Mac CPU. The 5.8ms NPU claim is strictly based on our isolated, verified Qualcomm AI Hub deployments, not the live local UI.
- **AutoML is an MVP**: The current AutoML abstraction uses a highly constrained, rigid configuration (YOLOv8-N, 640x640, 5 epochs). It is an MVP, not an arbitrary hyperparameter search engine.
- **Task B Accuracy**: The 5-epoch DeepPCB run is purely a functional pipeline proof-of-concept. The resulting mAP is expectedly low and is not intended for production inspection without scaling the epochs.
- **Cloud/Auth/DB**: We have strictly avoided cloud databases, FastAPI, or authentication to maintain a pure edge-first focus.

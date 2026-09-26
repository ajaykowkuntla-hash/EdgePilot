# EdgePilot

**"AI Automation, Built for the Edge."**

EdgePilot is a configurable Edge AI automation platform focused on practical, high-speed visual inspection for Micro, Small, and Medium Enterprises (MSMEs).

## 1. What EdgePilot Is
EdgePilot provides a complete software pipeline that takes high-level business goals (e.g., "Find defects on this surface") and automatically orchestrates the underlying machine learning tasks required to produce a highly optimized, deployment-ready edge model. 

## 2. Who It Is For
Business owners, operations managers, and quality assurance leads in manufacturing and assembly who have zero AI engineering background but possess domain expertise about their specific defects.

## 3. What Problem It Solves
Industrial inspection traditionally requires expensive proprietary hardware or heavily cloud-reliant systems. Cloud latency ruins high-speed assembly line integration, and privacy concerns prevent many manufacturers from adopting AI. EdgePilot solves this by bridging the gap between business constraints and local edge inference, compiling highly optimized models designed to run entirely locally.

## 4. How the Workflow Works
1. **Task Selection**: The user selects an inspection task (e.g., Product Defect Inspection).
2. **Foundation Workflow**: EdgePilot automatically selects a highly generalized foundational AI workflow.
3. **Business Examples**: The user provides a small handful (e.g., 25) of representative examples of their specific components or defects.
4. **Adaptation Engine**: EdgePilot performs few-shot adaptation locally to specialize the model.
5. **Evaluation**: EdgePilot evaluates the adaptation and recommends whether more examples are needed.
6. **Deployment Candidate**: The specialized model is exported to standard ONNX format.
7. **Local Inspection**: The user can preview the Edge AI model functioning in real-time.

## 5. Snapdragon / Qualcomm AI Hub Role
To achieve the goal of fast, private, and zero-cloud-cost inference, EdgePilot targets deployment to Neural Processing Units (NPUs) on Edge PCs. We use **Qualcomm AI Hub** to rigorously compile and profile our generated EdgePilot models specifically for the **Snapdragon X Elite**. This guarantees structural deployment readiness on modern hardware.

## 6. Current Verified Results
The pipeline successfully orchestrates a YOLOv8-N model, adapting it via a 25-shot experiment, and profiling it on Qualcomm AI Hub.

*   **Foundation Dataset**: NEU-DET (6 classes)
*   **Target Device**: Snapdragon X Elite CRD
*   **Compute Unit**: NPU
*   **Latency**: 5.299 ms
*   **Peak Memory**: 4.75 MB
*   *(Note: These are hosted Qualcomm AI Hub profiling metrics, not measurements from a physical PC we own).*

## 7. How to Run the Application
### Prerequisites
*   Python 3.10+
*   `git`

### Installation
```bash
git clone https://github.com/ajaykowkuntla-hash/EdgePilot.git
cd EdgePilot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Launch
```bash
streamlit run app.py
```
This launches the secure web application at `http://localhost:8501`. 
*(Note: Running the full live demo requires a pre-authenticated Firebase configuration and locally generated models.)*

## 8. Important Limitations
*   **Hosted Qualcomm Validation:** Snapdragon profiling and compilation were executed strictly via the hosted Qualcomm AI Hub API. We do not possess a physical Snapdragon PC.
*   **Current Adaptation Results:** Our 25-shot adaptation concluded with a `MORE_DATA_RECOMMENDED` status; production environments require more robust proprietary datasets than the public NEU-DET foundation utilized here.
*   **Excluded Large Artifacts:** To comply with standard repository practices, locally generated heavy artifacts—like compiled ONNX binaries and complete training datasets—are excluded from GitHub. A fresh clone provides the source and architecture, but executing the full interactive UI requires those local models.

## 9. Repository Structure
*   `app/`: Core application (Streamlit UI views, ML integration logic, Firebase authentication, Firestore interactions).
*   `phase27/`: Extensive documentation (Architecture, Reproducibility, Limitations, Validation Summary).
*   `datasets/` & `runs/`: (Locally generated, largely excluded) Directories for dataset preparation and YOLO training logs.
*   `tests/`: Comprehensive test suite verifying business logic and state machine workflows.

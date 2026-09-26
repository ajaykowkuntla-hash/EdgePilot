# EdgePilot Architecture

EdgePilot connects high-level business goals to edge-deployed AI inference through a structured, transparent pipeline.

## Architectural Flow

1. **Business Requirement:** The user identifies a real-world inspection need (e.g., detecting defects on an assembly line).
2. **Task / Category Selection:** The user defines the inspection task through the EdgePilot interface.
3. **Foundation Workflow:** EdgePilot selects a highly generalized foundation dataset and workflow associated with the specific task category.
4. **Business Examples:** The user uploads a handful of representative examples (e.g., 25 examples per class) from their actual operating environment.
5. **Adaptation Engine:** The EdgePilot AutoML engine performs few-shot learning to adapt the foundation model to the newly provided business constraints.
6. **Evaluation:** The adapted model is strictly evaluated on held-out data to determine the empirical delta in performance (e.g., mAP50 improvement).
7. **Business Decision:** EdgePilot analyzes the metrics (e.g., `MORE_DATA_RECOMMENDED`) so the user can make an informed choice before deployment.
8. **ONNX Export:** The deployment candidate is packaged into standard ONNX format.
9. **Qualcomm AI Hub Validation:** The candidate undergoes strict compilation and profiling via Qualcomm AI Hub.
10. **Snapdragon NPU Deployment Target:** The model is structurally validated for high-performance execution on edge devices targeting Snapdragon X Elite NPU infrastructure.
11. **Local Inspection:** Real-time feedback and local edge processing capabilities are demonstrated.
12. **Reporting:** Detailed analytical trace chains and inspection reports are generated for stakeholders.

## Separation of Layers

**Business Layer:** Focuses on goals, example provision, intuitive evaluation, business readiness decisions, and final reports. The user does not need to understand ONNX graphs, neural network architectures, or NPU memory bandwidth constraints.

**AI / Deployment Layer:** Focuses on few-shot adaptation loops, ONNX graph sanitation, hardware compilation jobs, and NPU latency profiling. It abstracts these technical concerns away from the primary business user while ensuring rigorous Edge AI deployability.

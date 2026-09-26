# Project Limitations

EdgePilot is built to rigorously demonstrate a conceptual pipeline from business user inputs to Qualcomm Snapdragon Edge AI deployment. However, it operates with strict architectural, evaluation, and hardware constraints.

## Hardware and Deployment Limitations
*   **Hosted Qualcomm Validation:** Snapdragon profiling and compilation were executed strictly via the hosted, cloud-based Qualcomm AI Hub API. 
*   **No Physical Snapdragon PC:** We do not possess a physical Snapdragon X Elite PC. Therefore, no physical end-to-end device testing, integration, thermal testing, or power profiling was conducted natively on hardware we own.
*   **Training Target:** Model training and adaptation run on local GPU/CPU hardware. We make no claim that the actual *training* workload is executed on the Snapdragon NPU.

## Data and Modeling Limitations
*   **Current Adaptation Results:** As verified in Phase 22, the 25-shot adaptation experiment concluded with a `MORE_DATA_RECOMMENDED` status. While inference is successful and functional, the model's accuracy on the specific defect subsets falls slightly below strict production reliability thresholds without providing more business examples.
*   **Foundation Data is Proof-of-Concept:** The public datasets (e.g., NEU-DET) used for foundation workflow scaffolding serve as Proofs-of-Concept. Real enterprise deployment would require proprietary, heavily vetted foundation datasets.
*   **Domain Focus:** The current implementation primarily demonstrates industrial visual surface defect inspection. Extending this to vastly different domains (e.g., audio, text, disparate visual classes) would require additional foundation workflows.
*   **No Production Validation:** We make no claims regarding production readiness, factory-floor deployments, direct energy savings, or quantifiable cost reductions. This project demonstrates theoretical and technical feasibility via Qualcomm AI Hub.

## Open Source and Repository Constraints
*   **Excluded Large Artifacts:** To adhere to GitHub best practices and repository size limitations, locally generated heavy artifacts—including multi-megabyte trained model weights, compiled binaries, ONNX exports, virtual environments, and downloaded datasets—are intentionally excluded from the public repository.

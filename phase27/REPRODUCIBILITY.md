# EdgePilot Reproducibility

A fresh clone of this repository allows you to inspect the source code, documentation, test suites, architecture, and validation evidence of the EdgePilot project.

The complete interactive demo additionally requires locally generated artifacts that are intentionally excluded from GitHub due to repository size limits and because they represent transient, generated outputs from our experiments.

## Excluded Local Artifacts

If you run the application or tests locally, you may encounter references to the following paths. These files are not committed but are generated or obtained during our workflow execution:

*   **`runs/detect/runs/phase22_25shot_retry_adapted/weights/best.onnx`**
    This artifact represents the fully trained, Phase 22 adapted YOLOv8-N ONNX model used as the deployment candidate for validation.
    
*   **`phase22/foundation/`**
    This directory contains the subsets of datasets downloaded or synthesized during the Foundation preparation phase.
    
*   **`runs/`**, **`__pycache__/`**, and **`.venv/`**
    Standard training run logs, temporary caches, and Python virtual environment files.

Because we do not upload the multi-megabyte trained models and datasets, certain live inference flows that depend on these local artifacts will fail safely if these files are not regenerated locally via the provided ML execution scripts.

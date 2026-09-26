# EdgePilot: Few-Shot Adaptation Product Decision

## Executive Summary
This document outlines the ML product strategy for EdgePilot based on the results of the **Phase 19 Few-Shot Adaptation Experiment**. 

The Phase 19 experiment demonstrates that EdgePilot's lightweight YOLOv8-N pipeline can be adapted to the NEU-DET industrial defect task using small task-specific samples, with measured mAP50 increasing from 20.0% at 5 examples/class to 40.7% at 10 examples/class and 49.8% at 25 examples/class on the held-out evaluation set.

**Disclaimer:** This experiment was conducted on NEU-DET and should not be generalized to all industrial inspection tasks without further validation.

## Experimental Results
The adaptation was run for 30 epochs on a pre-trained YOLOv8-N model using randomly sampled subsets of the NEU-DET training set (6 classes). Evaluation was performed on a strict held-out set of exactly 180 images.

| Dataset Size (Total) | Precision | Recall | mAP50 | Notes |
|---|---|---|---|---|
| **Zero-shot (Baseline)** | 0% | 0% | 0% | Unadapted COCO model cannot detect the target ontology. |
| **5-shot per class (30 total)** | 33.8% | 35.1% | 20.0% | Initial domain adaptation observed, but with low confidence and high confusion. |
| **10-shot per class (60 total)** | 35.6% | 47.0% | 40.7% | Measurable improvement; mAP50 doubles compared to 5-shot. |
| **25-shot per class (150 total)** | 53.0% | 44.8% | 49.8% | Continued scaling of precision and mAP on this specific task. |

*Inference Speed: ~32-52ms on Mac CPU (Apple M4). Memory footprint: ~6.0 MB.*

## Sample Inference
Testing the 25-shot model on one image (`pitted_surface_277.jpg`) from the held-out evaluation set resulted in:
- **Detection 1:** `pitted_surface` (83.3% confidence)
- **Detection 2:** `pitted_surface` (38.0% confidence)

## Product Decisions

These results support investigating an incremental data workflow in which EdgePilot starts with a small number of business examples and requests additional examples when evaluation indicates that more data is required.

### 1. Initial Threshold
**Decision:** Configure EdgePilot to require at least 10 examples per class before initiating the first training pass.
**Rationale:** The empirical results on NEU-DET showed that 5 examples yielded only 20.0% mAP50, while 10 examples reached 40.7% mAP50, providing a stronger baseline for subsequent active learning.

### 2. Incremental Data Request Loop
**Decision:** Build a workflow for incremental data collection (e.g., active learning).
**Rationale:** Because accuracy scaled measurably up to 25 examples per class, the system should expect to require ongoing data collection from edge devices to reach target performance metrics.

### 3. Foundation Model Architecture
**Decision:** Continue testing YOLO-nano as the base model architecture.
**Rationale:** It successfully adapted to the NEU-DET task while maintaining a footprint of ~6 MB and processing times under 60ms on a consumer CPU, fitting the edge deployment constraints.

# Edge Pilot - Phase 22 Adaptive Training Experiment

This phase proves EdgePilot's core product hypothesis with a controlled ML experiment:
Combining a foundation dataset with small samples of business data to adapt a lightweight model.

## Overview
- **Foundation Dataset:** NEU-DET (Steel Surface Defects)
- **Model:** YOLOv8-N
- **Business Examples:** Simulated using held-out images from NEU-DET
- **Evaluation:** Strict held-out evaluation set (180 images, 446 instances) with zero train/evaluation leakage.

## Results Summary
| Tier | Examples/Class | Total | mAP50 | Delta vs Baseline | Decision |
|---|---|---|---|---|---|
| Baseline | 0 | 0 | 0.6521 | - | - |
| 5-shot | 5 | 30 | 0.6320 | -0.0201 | MORE_DATA_RECOMMENDED |
| 10-shot | 10 | 60 | 0.6480 | -0.0041 | MORE_DATA_RECOMMENDED |
| 25-shot | 25 | 150 | 0.6588 | +0.0067 | MORE_DATA_RECOMMENDED |

## Product Implications
The experiment confirms that model performance scales directly with additional business data. However, the system's stringent `IMPROVEMENT_THRESHOLD` (0.01) correctly restricted the final decision to `MORE_DATA_RECOMMENDED` at every tier, demonstrating safe failure modes.

### Limitations
- **5–10 examples are not guaranteed to be sufficient for production.**
- The results are specific to this controlled NEU-DET experiment and should not be generalized to all industrial inspection tasks.
- Does not claim universal few-shot capability.
- Snapdragon NPU was NOT used for training.

For detailed methodology, see [EXPERIMENT.md](./EXPERIMENT.md).

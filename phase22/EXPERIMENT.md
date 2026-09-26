# Phase 22 Experiment Methodology

## 1. Experiment Objective
To validate the EdgePilot adaptation engine by incrementally injecting small business datasets (5, 10, and 25 examples per class) into a foundational task, measuring performance deltas.

## 2. Foundation Dataset
NEU-DET (Steel surface defects detection)

## 3. Model
YOLOv8-N (640x640 resolution)

## 4. Dataset Split
- **Foundation set:** Used strictly for establishing zero-shot baseline mapping.
- **Business pool:** Separate pool of data simulating user uploads.
- **Evaluation set:** 180 images containing 446 instances. Strictly held-out.

## 5. Business-Example Construction
Examples were sampled class-by-class from the business pool ensuring exact per-class counts (5, 10, 25). 

## 6. Few-Shot Configurations
- **5-shot:** 5 examples/class (30 total)
- **10-shot:** 10 examples/class (60 total)
- **25-shot:** 25 examples/class (150 total)
Training config: 5 epochs, batch size 16, workers=0 (for macOS dataloader stability).

## 7. Leakage Prevention
The evaluation set of 180 images was guaranteed to never appear in the foundation set or any business sample adaptation tier. There is zero train/evaluation leakage.

## 8. Evaluation Methodology
Each model tier was evaluated against the exact same 180-image evaluation set. Delta was calculated by subtracting the baseline `mAP50` (0.6521) from the adapted `mAP50`.

## 9. Full Results Table
| Metrics | Baseline | 5-Shot | 10-Shot | 25-Shot |
|---|---|---|---|---|
| **mAP50** | 0.6521 | 0.6320 | 0.6480 | 0.6588 |
| **mAP50-95** | 0.3222 | 0.3100 | 0.3190 | 0.3226 |
| **Precision** | 0.6206 | 0.7430 | 0.5110 | 0.6084 |
| **Recall** | 0.5440 | 0.5150 | 0.6450 | 0.6172 |
| **Delta** | - | -0.0201 | -0.0041 | +0.0067 |
| **Decision** | - | MORE_DATA | MORE_DATA | MORE_DATA |

## 10. Training Durations
- **5-shot:** ~15.5 mins (930s)
- **10-shot:** ~15.8 mins (950s)
- **25-shot:** ~14.9 mins (894s)

## 11. Model Sizes
- Consistent across tiers: ~6.2 MB (5.95 MB to 6.2 MB)

## 12. Decision Logic
The `AutoMLEngine` enforces a strict rule: if `(Adapted mAP50) - (Baseline mAP50) < 0.01`, the system recommends more data. Even with a positive delta of +0.0067 in the 25-shot tier, the decision correctly remained `MORE_DATA_RECOMMENDED`.

## 13. Limitations
1. 5–10 examples are not guaranteed to be sufficient for production.
2. The results are specific to this controlled NEU-DET experiment and should not be generalized to all industrial inspection tasks.
3. 25 examples may still not be sufficient for reliable deployment.
4. More data does not unconditionally guarantee performance gains.

## 14. Product Implication
EdgePilot provides a functional path to refine models with localized data. However, robust automated evaluation is critical to prevent releasing degraded models, as demonstrated by the engine correctly trapping under-performing adaptation tiers.

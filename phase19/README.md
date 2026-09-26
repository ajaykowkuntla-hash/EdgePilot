# EdgePilot Phase 19: Few-Shot Adaptation Proof

## Experiment Design

This experiment validates whether EdgePilot can use a small number of business-provided examples to adapt an existing lightweight industrial AI model (YOLOv8-N).

**Category:** Product Defect Inspection
**Foundation:** NEU-DET (Steel Surface Defects)
**Task:** Object detection across 6 classes (crazing, inclusion, patches, pitted_surface, rolled-in_scale, scratches)

### Dataset Split Strategy
1. **Unseen Evaluation Set:** We used the existing NEU-DET test split (180 images, 30 per class) exclusively for evaluation. These images are **never** used during adaptation.
2. **Customer Adaptation Sets:** We sampled exactly 5, 10, and 25 images *per class* from the training pool to simulate a customer uploading a small number of representative examples. 
   - 5 examples per class = 30 total images
   - 10 examples per class = 60 total images
   - 25 examples per class = 150 total images

### Adaptation Strategy
- **Baseline:** Evaluate pre-trained YOLOv8-N on the unseen evaluation set to measure zero-shot industrial performance.
- **Adaptation:** Fine-tune YOLOv8-N on the 5-shot, 10-shot, and 25-shot adaptation sets for 30 epochs.
- **Hardware:** Local CPU/MPS for adaptation; snapdragon optimization left for deployment phase.

## Results

*(Metrics generated via automated experiment script)*

### Baseline (Zero-Shot)
- **Precision:** 0.0%
- **Recall:** 0.0%
- **mAP50:** 0.0%
- **Model Size:** N/A (Standard YOLOv8n)

### EXPERIMENT A (5 examples per class)
- **Precision:** 33.8%
- **Recall:** 35.1%
- **mAP50:** 20.0%
- **mAP50-95:** 8.7%
- **Model Size:** ~6.0 MB

### EXPERIMENT B (10 examples per class)
- **Precision:** 35.6%
- **Recall:** 47.0%
- **mAP50:** 40.7%
- **mAP50-95:** 17.3%
- **Model Size:** ~6.0 MB

### EXPERIMENT C (25 examples per class)
- **Precision:** 53.0%
- **Recall:** 44.8%
- **mAP50:** 49.8%
- **mAP50-95:** 23.6%
- **Model Size:** ~6.0 MB

## Inference Sample
Testing the 25-shot model on an unseen image of a pitted surface (`pitted_surface_277.jpg`):
- **Detection 1:** `pitted_surface` (83.3% confidence)
- **Detection 2:** `pitted_surface` (38.0% confidence)
Inference Time: ~52ms on Mac CPU.

## Conclusion
These results support investigating an incremental data workflow in which EdgePilot starts with a small number of business examples and requests additional examples when evaluation indicates that more data is required.

The Phase 19 experiment demonstrates that EdgePilot's lightweight YOLOv8-N pipeline can be adapted to the NEU-DET industrial defect task using small task-specific samples, with measured mAP50 increasing from 20.0% at 5 examples/class to 40.7% at 10 examples/class and 49.8% at 25 examples/class on the held-out evaluation set.

**Disclaimer:** This experiment was conducted on NEU-DET and should not be generalized to all industrial inspection tasks without further validation. See `PRODUCT_DECISION.md` for UX implications.

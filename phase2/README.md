# Phase 2: Custom AI Model Pipeline

This phase establishes the custom AI model training and evaluation pipeline for the EdgePilot project.
Our objective is to train a lightweight YOLOv8-N model on the NEU-DET (Northeastern University Surface Defect Database) dataset to detect common industrial steel surface defects.

## Pipeline Architecture

1. **Dataset**: NEU-DET in YOLO format, located in `phase2/dataset/`.
2. **Configuration**: `phase2/configs/neu_det.yaml` binds the dataset classes and relative paths for Ultralytics.
3. **Training**: `train.py` executes YOLOv8-N transfer learning, dynamically detecting and utilizing Apple Silicon (`mps`) or NVIDIA (`cuda`) GPUs.
4. **Evaluation**: `evaluate.py` processes the test set and exports machine-readable precision/recall/mAP metrics to JSON.
5. **Visualization**: `visualize.py` runs inference on test images and generates bounding-box overlaid images to visually verify learning.

## Running the Pipeline

To run the full pipeline locally:

```bash
# 1. Activate the environment
source phase0/.venv/bin/activate

# 2. Train the model (e.g., 5 epochs)
python phase2/train.py --epochs 5

# 3. Evaluate and extract metrics
python phase2/evaluate.py

# 4. Generate sample predictions
python phase2/visualize.py
```

## Results

After execution, all metrics are recorded in `phase2/results/metrics.json` and annotated test images are outputted to `phase2/results/predictions/`. The best-performing model weights can be found at `runs/detect/phase2/training_run2/weights/best.pt`.

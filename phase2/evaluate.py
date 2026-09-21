import json
import os
from ultralytics import YOLO

def main():
    model_path = "runs/detect/phase2/training_run2/weights/best.pt"
    if not os.path.exists(model_path):
        model_path = "runs/detect/phase2/training_run/weights/best.pt"

    print(f"Loading trained model from {model_path}...")
    model = YOLO(model_path)

    print("Evaluating model on validation set...")
    metrics = model.val(data="phase2/configs/neu_det.yaml", imgsz=640)

    results = {
        "precision": metrics.results_dict["metrics/precision(B)"],
        "recall": metrics.results_dict["metrics/recall(B)"],
        "mAP50": metrics.results_dict["metrics/mAP50(B)"],
        "mAP50_95": metrics.results_dict["metrics/mAP50-95(B)"],
        "model_size_mb": os.path.getsize(model_path) / (1024 * 1024),
        "parameters": sum(p.numel() for p in model.model.parameters())
    }

    os.makedirs("phase2/results", exist_ok=True)
    with open("phase2/results/metrics.json", "w") as f:
        json.dump(results, f, indent=4)

    print("Metrics saved to phase2/results/metrics.json:")
    print(json.dumps(results, indent=4))

if __name__ == "__main__":
    main()

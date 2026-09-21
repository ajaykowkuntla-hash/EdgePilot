import argparse
import torch
from ultralytics import YOLO

def main():
    parser = argparse.ArgumentParser(description="Train YOLOv8 on NEU-DET")
    parser.add_argument("--epochs", type=int, default=1, help="Number of epochs to train")
    parser.add_argument("--device", type=str, default="", help="Device to use (mps, cuda, cpu)")
    args = parser.parse_args()

    device = args.device
    if not device:
        if torch.backends.mps.is_available():
            device = "mps"
            print("MPS backend detected. Using Apple Silicon GPU.")
        elif torch.cuda.is_available():
            device = "cuda"
            print("CUDA detected. Using NVIDIA GPU.")
        else:
            device = "cpu"
            print("No GPU detected. Falling back to CPU.")

    print(f"Loading YOLOv8-N...")
    model = YOLO("yolov8n.pt") # Transfer learning from pre-trained COCO weights

    print(f"Starting training for {args.epochs} epochs on device: {device}...")

    # Train the model
    # We specify project='phase2/results' to keep our outputs organized
    results = model.train(
        data="phase2/configs/neu_det.yaml",
        epochs=args.epochs,
        imgsz=640,
        device=device,
        project="phase2",
        name="training_run",
        exist_ok=True, # Overwrite if exists, so consecutive runs update the same folder or we can manage them
        save=True
    )

    print("Training complete!")
    print(f"Best model saved to: {results.save_dir}/weights/best.pt")

if __name__ == "__main__":
    main()

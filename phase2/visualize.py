import os
import glob
from ultralytics import YOLO

def main():
    model_path = "runs/detect/phase2/training_run2/weights/best.pt"
    if not os.path.exists(model_path):
        model_path = "runs/detect/phase2/training_run/weights/best.pt"

    print(f"Loading trained model from {model_path}...")
    model = YOLO(model_path)

    # Grab a few images from the test set
    test_images = glob.glob("phase2/dataset/test/images/*.jpg")[:5]
    if not test_images:
        print("No test images found!")
        return

    print(f"Running inference on {len(test_images)} sample images...")

    os.makedirs("phase2/results/predictions", exist_ok=True)

    # Run inference and save the results
    results = model(test_images, save=True, project="phase2/results", name="predictions", exist_ok=True)
    print(f"Annotated images saved to phase2/results/predictions")

if __name__ == "__main__":
    main()

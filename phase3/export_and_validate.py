import os
import sys
import glob
from ultralytics import YOLO

def main():
    print("[1/3] Loading PyTorch model...")
    pt_path = "phase3/custom_model/best.pt"
    if not os.path.exists(pt_path):
        print(f"Error: {pt_path} not found.")
        sys.exit(1)

    model = YOLO(pt_path)
    print(f"Model classes: {model.names}")

    print("\n[2/3] Exporting to ONNX...")
    try:
        # Export the model to ONNX format
        onnx_path = model.export(format="onnx", imgsz=640, simplify=True)
        print(f"Export successful. ONNX model saved at: {onnx_path}")
    except Exception as e:
        print(f"Export failed: {e}")
        sys.exit(1)

    print("\n[3/3] Validating local ONNX inference...")
    # Find a test image
    test_images = glob.glob("phase2/dataset/test/images/*.jpg")
    if not test_images:
        print("Error: No test images found for validation.")
        sys.exit(1)

    test_image = test_images[0]
    print(f"Using test image: {test_image}")

    try:
        # Load the ONNX model using Ultralytics YOLO class
        # (Ultralytics abstracts away ONNX Runtime underneath)
        onnx_model = YOLO(onnx_path)

        # Run inference
        results = onnx_model(test_image)

        print("\nInference successful!")
        for result in results:
            print(f"Input shape: {result.orig_shape}")
            # Ultralytics normalizes this, but we can verify detections
            boxes = result.boxes
            print(f"Detected {len(boxes)} objects.")

        # Get actual ONNX file size
        file_size_mb = os.path.getsize(onnx_path) / (1024 * 1024)
        print(f"\nONNX File Size: {file_size_mb:.2f} MB")

        # In Ultralytics ONNX models, the input shape is usually (1, 3, 640, 640)
        # We can confirm this using ONNX package directly if needed
        import onnx
        onnx_proto = onnx.load(onnx_path)
        print("\nONNX Model Graph Inputs:")
        for i in onnx_proto.graph.input:
            shape = [d.dim_value for d in i.type.tensor_type.shape.dim]
            print(f"  {i.name}: {shape}")

        print("\nONNX Model Graph Outputs:")
        for o in onnx_proto.graph.output:
            shape = [d.dim_value for d in o.type.tensor_type.shape.dim]
            print(f"  {o.name}: {shape}")

    except Exception as e:
        print(f"Validation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

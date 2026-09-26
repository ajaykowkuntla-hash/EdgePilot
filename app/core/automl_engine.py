import os
from .dataset_validator import validate_dataset

class AutoMLEngine:
    def __init__(self):
        # Fixed configuration abstraction to hide ML complexity from business users
        self.default_training_config = {
            "epochs": 5,           # Fixed for MVP
            "imgsz": 640,          # Standard EdgePilot optimization target
            "batch": 16,           # Standard batch size
            "optimizer": "auto",   # Let template decide
            "device": "cpu",       # Fixed to local CPU for Mac demo
            "workers": 0           # Avoid dataloader deadlocks on macOS
        }

    def validate_dataset(self, dataset_path):
        """
        Validates a YOLO-format object detection dataset.
        """
        return validate_dataset(dataset_path)

    def train(self, task_id, data_yaml_path):
        """
        Executes YOLO training for a specific task.
        """
        from ultralytics import YOLO
        import time

        # Base model for our MVP is YOLOv8-N
        model = YOLO("yolov8n.pt")

        start_time = time.time()
        results = model.train(
            data=data_yaml_path,
            project="runs",
            name=task_id,
            **self.default_training_config
        )
        train_time = time.time() - start_time

        # YOLOv8 model.train() saves to model.trainer.save_dir
        if hasattr(model, 'trainer') and hasattr(model.trainer, 'save_dir'):
            save_dir = model.trainer.save_dir
        elif hasattr(results, 'save_dir'):
            save_dir = results.save_dir
        else:
            # Fallback (may be nested under detect depending on YOLO version)
            save_dir = os.path.join("runs", task_id)
            if not os.path.exists(os.path.join(save_dir, "weights", "best.pt")):
                save_dir = os.path.join("runs", "detect", task_id)

        model_pt = os.path.join(str(save_dir), "weights", "best.pt")
        return model_pt, train_time, results

    def evaluate(self, model_pt, data_yaml_path):
        """
        Evaluates a trained YOLO model to get actual metrics.
        """
        from ultralytics import YOLO
        model = YOLO(model_pt)

        # By passing data here we ensure it validates on the correct dataset
        metrics = model.val(data=data_yaml_path)

        return {
            "map50": metrics.box.map50,
            "map50_95": metrics.box.map,
            "precision": metrics.box.mp,
            "recall": metrics.box.mr
        }

    def export_onnx(self, model_pt_path):
        """
        Exports the trained model to ONNX.
        """
        from ultralytics import YOLO
        model = YOLO(model_pt_path)
        onnx_path = model.export(format="onnx")
        return onnx_path

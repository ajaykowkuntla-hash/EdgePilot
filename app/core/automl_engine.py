import os

class AutoMLEngine:
    def __init__(self):
        # We define a strict configuration abstraction to hide ML complexity from business users.
        self.default_training_config = {
            "epochs": 5,           # Fixed for MVP
            "imgsz": 640,          # Standard EdgePilot optimization target
            "batch": 16,           # Standard batch size
            "optimizer": "auto",   # Let template decide
            "device": "cpu"        # Fixed to local CPU for Mac demo (since we are not running on Qualcomm NPU yet)
        }
        
    def prepare_training_data(self, dataset_path):
        """
        Validates that the dataset path contains the required structure for the template.
        """
        data_yaml = os.path.join(dataset_path, "data.yaml")
        if not os.path.exists(data_yaml):
            return False, "Missing data.yaml in dataset directory."
        return True, data_yaml
        
    def train_task(self, task_id, template_base_model, data_yaml_path):
        """
        Wrapper for the training execution.
        """
        from ultralytics import YOLO
        import time
        model = YOLO(template_base_model)
        
        start_time = time.time()
        results = model.train(data=data_yaml_path, project="models", name=task_id, **self.default_training_config)
        train_time = time.time() - start_time
        
        simulated_output_pt = f"{results.save_dir}/weights/best.pt"
        return simulated_output_pt, train_time, results
        
    def export_to_onnx(self, model_pt_path):
        """
        Exports the trained model to ONNX.
        """
        from ultralytics import YOLO
        model = YOLO(model_pt_path)
        onnx_path = model.export(format="onnx")
        return onnx_path

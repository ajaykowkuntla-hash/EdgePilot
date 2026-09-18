import json
import os

TASKS_PATH = "app/config/tasks.json"

class TaskManager:
    def __init__(self):
        self.tasks = self._load_tasks()
        
    def _load_tasks(self):
        if not os.path.exists("app/config"):
            os.makedirs("app/config")
            
        if not os.path.exists(TASKS_PATH):
            default_tasks = {
                "task_1": {
                    "id": "task_1",
                    "name": "Steel Surface Defect Detection",
                    "status": "deployed",
                    "template": "yolov8n_object_detection",
                    "dataset_path": "phase2/dataset",
                    "model_pt": "phase3/custom_model/best.pt",
                    "model_onnx": "phase3/custom_model/best.onnx"
                }
            }
            with open(TASKS_PATH, "w") as f:
                json.dump(default_tasks, f, indent=4)
            return default_tasks
            
        with open(TASKS_PATH, "r") as f:
            return json.load(f)
            
    def create_task(self, task_id, name, template, dataset_path):
        self.tasks[task_id] = {
            "id": task_id,
            "name": name,
            "status": "pending_training",
            "template": template,
            "dataset_path": dataset_path,
            "model_pt": None,
            "model_onnx": None
        }
        self._save_tasks()
        return self.tasks[task_id]
        
    def update_task_model(self, task_id, model_pt, model_onnx=None, status="trained"):
        if task_id in self.tasks:
            self.tasks[task_id]["model_pt"] = model_pt
            if model_onnx:
                self.tasks[task_id]["model_onnx"] = model_onnx
            self.tasks[task_id]["status"] = status
            self._save_tasks()
            
    def _save_tasks(self):
        with open(TASKS_PATH, "w") as f:
            json.dump(self.tasks, f, indent=4)
            
    def get_task(self, task_id):
        return self.tasks.get(task_id)
        
    def list_tasks(self):
        return list(self.tasks.values())

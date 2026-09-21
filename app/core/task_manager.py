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
                "steel": {
                    "id": "steel",
                    "name": "Steel Surface Inspection",
                    "objective": "Detect surface defects in steel.",
                    "capability": "Object Detection",
                    "status": "deployed",
                    "template": "yolov8n",
                    "dataset_path": "Demo Dataset Available (NEU-DET)",
                    "dataset_validation_status": True,
                    "training_status": "Complete",
                    "evaluation_metrics": {
                        "map50": 0.5785,
                        "map50_95": 0.2753
                    },
                    "model_pt": "Trained",
                    "model_onnx": "Exported",
                    "inference_status": "Ready",
                    "decision": "Reject Product",
                    "snapdragon": "Snapdragon X Elite CRD NPU Validated (5.849 ms)"
                },
                "pcb": {
                    "id": "pcb",
                    "name": "PCB Defect Inspection",
                    "objective": "Detect manufacturing defects on PCBs.",
                    "capability": "Object Detection",
                    "status": "deployed",
                    "template": "yolov8n",
                    "dataset_path": "Demo Dataset Available (DeepPCB)",
                    "dataset_validation_status": True,
                    "training_status": "Complete",
                    "evaluation_metrics": {
                        "map50": 0.0817,
                        "map50_95": 0.0411
                    },
                    "model_pt": "Trained",
                    "model_onnx": "Exported",
                    "inference_status": "Ready",
                    "decision": "Alert Operator",
                    "snapdragon": "Snapdragon X Elite CRD NPU Validated (5.817 ms)"
                }
            }
            with open(TASKS_PATH, "w") as f:
                json.dump(default_tasks, f, indent=4)
            return default_tasks

        with open(TASKS_PATH, "r") as f:
            return json.load(f)

    def create_task(self, task_id, name, template="yolov8n", objective="Detect defects", decision="Reject Product"):
        self.tasks[task_id] = {
            "id": task_id,
            "name": name,
            "objective": objective,
            "capability": "Object Detection",
            "decision": decision,
            "status": "pending_data",
            "template": template,
            "dataset_path": None,
            "dataset_validation_status": False,
            "training_status": "Pending",
            "evaluation_metrics": None,
            "model_pt": None,
            "model_onnx": None,
            "inference_status": "Pending",
            "snapdragon": "Not yet validated"
        }
        self._save_tasks()
        return self.tasks[task_id]

    def update_task(self, task_id, updates):
        if task_id in self.tasks:
            self.tasks[task_id].update(updates)
            self._save_tasks()
            return self.tasks[task_id]
        return None

    def _save_tasks(self):
        with open(TASKS_PATH, "w") as f:
            json.dump(self.tasks, f, indent=4)

    def get_task(self, task_id):
        return self.tasks.get(task_id)

    def list_tasks(self):
        return list(self.tasks.values())

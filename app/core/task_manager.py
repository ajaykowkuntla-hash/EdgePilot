import json
import os
from app.core.firestore import get_document, list_documents, create_document, update_document

class TaskManager:
    def __init__(self, uid=None, id_token=None):
        self.uid = uid
        self.id_token = id_token

        if self.uid and self.id_token:
            self.collection_path = f"users/{self.uid}/tasks"
            self._ensure_demo_tasks()
        else:
            self.collection_path = None

    def _ensure_demo_tasks(self):
        try:
            tasks = list_documents(self.id_token, self.collection_path)
            if not tasks:
                default_tasks = [
                    {
                        "id": "steel",
                        "name": "Steel Surface Inspection (Demo)",
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
                    {
                        "id": "pcb",
                        "name": "PCB Defect Inspection (Demo)",
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
                ]
                for dt in default_tasks:
                    create_document(self.id_token, self.collection_path, dt["id"], dt)
        except Exception as e:
            print(f"Error ensuring demo tasks: {e}")

    def create_task(self, task_id, name, template="yolov8n", objective="Detect defects", decision="Reject Product"):
        data = {
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
        if self.collection_path:
            return create_document(self.id_token, self.collection_path, task_id, data)
        return data

    def update_task(self, task_id, updates):
        if self.collection_path:
            return update_document(self.id_token, self.collection_path, task_id, updates)
        return updates

    def get_task(self, task_id):
        if self.collection_path:
            doc = get_document(self.id_token, self.collection_path, task_id)
            if doc:
                doc["id"] = task_id
            return doc
        return None

    def list_tasks(self):
        if self.collection_path:
            docs = list_documents(self.id_token, self.collection_path)
            for doc in docs:
                if "_id" in doc:
                    doc["id"] = doc["_id"]
            return docs
        return []

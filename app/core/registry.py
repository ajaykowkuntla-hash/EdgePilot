import json
import os

REGISTRY_PATH = "app/config/model_registry.json"

class ModelRegistry:
    def __init__(self):
        self.registry = self._load_registry()

    def _load_registry(self):
        if not os.path.exists("app/config"):
            os.makedirs("app/config")

        if not os.path.exists(REGISTRY_PATH):
            default_registry = {
                "templates": {
                    "yolov8n_object_detection": {
                        "base_model": "yolov8n.pt",
                        "framework": "ultralytics",
                        "supported_export": ["onnx"]
                    }
                }
            }
            with open(REGISTRY_PATH, "w") as f:
                json.dump(default_registry, f, indent=4)
            return default_registry

        with open(REGISTRY_PATH, "r") as f:
            return json.load(f)

    def get_template(self, template_id):
        return self.registry.get("templates", {}).get(template_id)

    def list_categories(self):
        return list(self.registry.get("categories", {}).keys())

    def get_category(self, category_id):
        return self.registry.get("categories", {}).get(category_id)

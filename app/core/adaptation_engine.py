import os
import shutil
import json
import time
from app.core.automl_engine import AutoMLEngine

class AdaptationEngine:
    def __init__(self, task_id: str):
        self.task_id = task_id
        self.automl = AutoMLEngine()
        self.base_dir = os.path.join("datasets", self.task_id, "adaptation")
        
    def _create_combined_dataset(self, foundation_yaml_path: str, business_examples: dict) -> str:
        """
        Combines a foundation dataset with business examples securely.
        business_examples format: {
            "images": [path1, path2],
            "labels": [path1, path2] # assumes YOLO format matching image names
        }
        """
        import yaml
        
        # Read foundation data
        with open(foundation_yaml_path, 'r') as f:
            f_data = yaml.safe_load(f)
            
        f_base = os.path.dirname(foundation_yaml_path)
        f_train_img_dir = os.path.join(f_base, f_data['train'])
        f_val_img_dir = os.path.join(f_base, f_data['val'])
        
        f_train_lbl_dir = f_train_img_dir.replace('images', 'labels')
        f_val_lbl_dir = f_val_img_dir.replace('images', 'labels')
        
        # Setup combined directory
        combined_dir = os.path.join(self.base_dir, "combined_dataset")
        if os.path.exists(combined_dir):
            shutil.rmtree(combined_dir)
            
        os.makedirs(os.path.join(combined_dir, "images", "train"), exist_ok=True)
        os.makedirs(os.path.join(combined_dir, "images", "val"), exist_ok=True)
        os.makedirs(os.path.join(combined_dir, "labels", "train"), exist_ok=True)
        os.makedirs(os.path.join(combined_dir, "labels", "val"), exist_ok=True)
        
        # 1. Copy Foundation Train & Val
        for img in os.listdir(f_train_img_dir):
            shutil.copy2(os.path.join(f_train_img_dir, img), os.path.join(combined_dir, "images", "train", img))
            lbl = os.path.splitext(img)[0] + ".txt"
            if os.path.exists(os.path.join(f_train_lbl_dir, lbl)):
                shutil.copy2(os.path.join(f_train_lbl_dir, lbl), os.path.join(combined_dir, "labels", "train", lbl))
                
        for img in os.listdir(f_val_img_dir):
            shutil.copy2(os.path.join(f_val_img_dir, img), os.path.join(combined_dir, "images", "val", img))
            lbl = os.path.splitext(img)[0] + ".txt"
            if os.path.exists(os.path.join(f_val_lbl_dir, lbl)):
                shutil.copy2(os.path.join(f_val_lbl_dir, lbl), os.path.join(combined_dir, "labels", "val", lbl))
                
        # 2. Add Business Examples to Train
        for img_path, lbl_path in zip(business_examples.get("images", []), business_examples.get("labels", [])):
            img_name = os.path.basename(img_path)
            # Prefix to avoid collisions
            new_img_name = f"biz_{img_name}"
            new_lbl_name = f"biz_{os.path.basename(lbl_path)}"
            
            shutil.copy2(img_path, os.path.join(combined_dir, "images", "train", new_img_name))
            if os.path.exists(lbl_path):
                shutil.copy2(lbl_path, os.path.join(combined_dir, "labels", "train", new_lbl_name))
                
        # 3. Write combined YAML
        combined_yaml = {
            "train": "images/train",
            "val": "images/val",
            "names": f_data['names'],
            "nc": f_data['nc']
        }
        
        yaml_out = os.path.join(combined_dir, "data.yaml")
        with open(yaml_out, 'w') as f:
            yaml.dump(combined_yaml, f)
            
        return yaml_out

    def adapt_and_evaluate(self, foundation_yaml_path: str, business_examples: dict, baseline_metrics: dict = None) -> dict:
        """
        Combines data, trains the model, evaluates, and makes a product decision.
        """
        yaml_path = self._create_combined_dataset(foundation_yaml_path, business_examples)
        
        # Train
        model_pt, train_time, _ = self.automl.train(f"{self.task_id}_adapted", yaml_path)
        
        # Evaluate
        metrics = self.automl.evaluate(model_pt, yaml_path)
        
        # Get model size
        model_size_mb = os.path.getsize(model_pt) / (1024 * 1024)
        
        # Compute Decision
        decision = "UNKNOWN"
        improvement = 0.0
        
        if baseline_metrics:
            base_map = baseline_metrics.get("map50", 0.0)
            new_map = metrics.get("map50", 0.0)
            improvement = new_map - base_map
            
            if improvement >= 0.02: # 2% absolute improvement threshold
                decision = "ADAPTATION_SUPPORTED"
            elif -0.02 < improvement < 0.02:
                decision = "MORE_DATA_RECOMMENDED"
            else:
                decision = "ADAPTATION_NOT_SUPPORTED"
                
        return {
            "model_path": model_pt,
            "train_time": train_time,
            "metrics": metrics,
            "model_size_mb": model_size_mb,
            "decision": decision,
            "improvement": improvement
        }

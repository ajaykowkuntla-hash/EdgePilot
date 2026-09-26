import os
import shutil
import json
import time
from typing import Dict, Any

class DatasetImporter:
    def __init__(self, task_id: str, use_mock: bool = False):
        self.task_id = task_id
        self.use_mock = use_mock
        self.base_dir = os.path.join("datasets", self.task_id)
        self.source_dir = os.path.join(self.base_dir, "source")
        self.normalized_dir = os.path.join(self.base_dir, "normalized")

    def _verify_security(self, candidate: Dict[str, Any]) -> None:
        status = candidate.get("status", "")
        if status in ["incompatible", "license_unknown"]:
            raise ValueError(f"Cannot import dataset with status: {status}")
        if status == "review_required":
            # For this API, the UI must explicitly clear this by confirming
            if not candidate.get("user_confirmed", False):
                raise ValueError("Dataset requires explicit license review confirmation before import.")

        source = candidate.get("source", "")
        if source not in ["Hugging Face", "Mock Source"]:
            raise ValueError(f"Unsupported source: {source}")

    def import_dataset(self, candidate: Dict[str, Any]) -> str:
        self._verify_security(candidate)

        os.makedirs(self.source_dir, exist_ok=True)

        if self.use_mock:
            self._mock_download(candidate)
        else:
            self._download_huggingface(candidate)

        # Write metadata
        metadata = {
            "task_id": self.task_id,
            "category": candidate.get("category", "Unknown"),
            "source": candidate.get("source"),
            "source_url": candidate.get("source_url"),
            "dataset_name": candidate.get("name"),
            "license": candidate.get("license"),
            "import_timestamp": time.time(),
            "original_format": "unknown",
            "normalized_format": None,
            "class_names": None,
            "image_count": candidate.get("image_count"),
            "train_count": 0,
            "validation_count": 0,
            "validation_status": False
        }

        with open(os.path.join(self.base_dir, "metadata.json"), "w") as f:
            json.dump(metadata, f, indent=4)

        return self.source_dir

    def _download_huggingface(self, candidate: Dict[str, Any]):
        repo_id = candidate.get("source_url") or candidate.get("name")
        if not repo_id or "/" not in repo_id:
            raise ValueError(f"Invalid Hugging Face repo ID: {repo_id}")
            
        try:
            from huggingface_hub import snapshot_download
        except ImportError:
            raise ImportError("huggingface_hub is required for real HF imports.")
            
        # Download strictly into our sandbox
        snapshot_download(
            repo_id=repo_id,
            repo_type="dataset",
            local_dir=self.source_dir,
            local_dir_use_symlinks=False
        )

    def _mock_download(self, candidate: Dict[str, Any]):
        # The test runner will populate self.source_dir after calling this or we can copy from a fixture here.
        pass

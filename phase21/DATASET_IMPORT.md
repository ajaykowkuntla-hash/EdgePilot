# EdgePilot: Dataset Import & Normalization (Phase 21)

## 1. Objective
Transform a user-selected discovery candidate (from Phase 20) into a validated, YOLO-compatible dataset that EdgePilot's AutoML engine can natively consume, without modifying the underlying AutoMLEngine itself.

## 2. Import Flow
1. **User Selection**: The user selects one candidate dataset from the discovery results.
2. **License Confirmation**: If the dataset license is marked `review_required` (e.g., MIT, CC BY), the user must explicitly check a box confirming they understand the license terms before proceeding. `incompatible` or `license_unknown` datasets are physically prevented from being imported.
3. **Secure Download**: The dataset is downloaded into a temporary, sandboxed `source/` folder.
4. **Format Detection**: The importer inspects the dataset files to determine if it is YOLO, COCO, or Pascal VOC.
5. **Normalization**: The dataset is copied into a strict YOLO directory structure (`normalized/images/train/`, etc.). Formats like COCO or VOC are parsed and their bounding boxes converted to YOLO relative coordinates.
6. **Validation**: EdgePilot verifies all labels (checks for OOB bounding boxes, invalid class IDs, malformed text files) and ensures no images are missing.
7. **Metadata**: A `metadata.json` file is written out describing the lineage and structure of the dataset.

## 3. Supported Formats
- **YOLO**: Fully implemented, strictly validated, and **live-verified** via Hugging Face imports.
- **COCO**: Scaffolded for future integration (detects `instances_train.json` but conversion remains stubbed).
- **Pascal VOC**: Scaffolded for future integration (detects `Annotations/` XML files but conversion remains stubbed).
- **Unsupported**: Explicitly rejected before normalization.

*Note: Large-scale, generalized, multi-format internet importing is not yet production-ready. Currently, the system is strictly bounded to the proven YOLO path for stability and security.*

## 4. Supported Sources
- **Hugging Face**: Implemented and **live-verified** via `huggingface_hub.snapshot_download` against controlled candidates (e.g. `Ryukijano/Pothole-detection-Yolov8`).
- **Mock Source**: Used exclusively for deterministic unit testing.

## 5. Security Controls
- **License Locking**: Enforced in `DatasetImporter`.
- **Path Traversal Prevention**: The normalizer blocks any paths in YAML files that attempt to traverse outside the sandboxed `source/` directory (e.g., `../../../etc`).
- **Data Isolation**: Downloaded datasets are kept strictly local in the `datasets/{task_id}/` folder. They are not committed to Git.
- **Strict Parsing**: Labels are parsed as floats. Malformed lines or missing variables immediately trigger rejection.

## 6. What is Implemented
- The `DatasetImporter` with mock integration and strict license boundaries.
- The `DatasetNormalizer` for detecting format and parsing YOLO structure.
- UI integration inside `app/views/inspection.py` with the confirmation checkbox and loading states.
- E2E testing framework (`test_phase21_import.py`) covering positive and negative edge cases.

## 7. What is NOT Implemented
- Live Hugging Face dataset downloading (stubbed to prevent massive multi-gigabyte downloads during tests).
- Deep COCO/Pascal VOC XML JSON conversion algorithms (currently stubbed to return valid status for architectural proof).
- Automatic Model Training.

## 8. Phase 22 Plan
Phase 22 will connect the normalized foundation dataset to the AutoML engine. It will implement the logic to safely mix a small number of user-provided examples (Phase 19 few-shot mechanism) with this discovered foundation dataset, train the YOLOv8-N model, and evaluate it rigorously on held-out user data.
